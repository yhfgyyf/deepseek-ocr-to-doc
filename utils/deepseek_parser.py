"""
DeepSeek-OCR output parser
Converts DeepSeek-OCR's markdown output with grounding tags to ContentBlocks
"""

import re
from typing import List, Dict, Tuple, Optional
from .structs import BlockType, ContentBlock


class DeepSeekOCRParser:
    """Parse DeepSeek-OCR output and convert to ContentBlocks"""

    def __init__(self):
        # Pattern to match <|ref|>type<|/ref|><|det|>coordinates<|/det|>
        self.ref_pattern = r'(<\|ref\|>(.*?)<\|/ref\|><\|det\|>(.*?)<\|/det\|>)'

    def parse(self, ocr_output: str) -> Tuple[str, List[Dict]]:
        """
        Parse DeepSeek-OCR output

        Args:
            ocr_output: Raw output from DeepSeek-OCR model

        Returns:
            Tuple of (cleaned_markdown, list of content blocks with metadata)
        """
        # Find all grounding references
        matches = re.findall(self.ref_pattern, ocr_output, re.DOTALL)

        # Separate image and other references
        image_refs = []
        other_refs = []

        for full_match, ref_type, det_coords in matches:
            if ref_type == 'image':
                image_refs.append((full_match, ref_type, det_coords))
            else:
                other_refs.append((full_match, ref_type, det_coords))

        # Start with the original output
        cleaned_markdown = ocr_output

        # Replace image references with markdown image syntax
        for idx, (full_match, ref_type, det_coords) in enumerate(image_refs):
            # Replace with markdown image reference
            cleaned_markdown = cleaned_markdown.replace(
                full_match,
                f'![image](images/image_{idx}.jpg)\n',
                1  # Replace only first occurrence
            )

        # Remove other grounding references (but keep the content structure)
        for full_match, ref_type, det_coords in other_refs:
            cleaned_markdown = cleaned_markdown.replace(full_match, '')

        # Clean up some common escape sequences
        cleaned_markdown = cleaned_markdown.replace('\\coloneqq', ':=')
        cleaned_markdown = cleaned_markdown.replace('\\eqqcolon', '=:')

        # Remove grounding markers
        cleaned_markdown = re.sub(r'<\|grounding\|>', '', cleaned_markdown)

        # Extract blocks from the cleaned markdown
        blocks = self._extract_blocks(cleaned_markdown, image_refs, other_refs)

        return cleaned_markdown, blocks

    def _extract_blocks(self, markdown: str, image_refs: List[Tuple],
                       other_refs: List[Tuple]) -> List[Dict]:
        """
        Extract content blocks from markdown

        Args:
            markdown: Cleaned markdown text
            image_refs: List of (full_match, type, coords) for images
            other_refs: List of (full_match, type, coords) for other elements

        Returns:
            List of ContentBlock dictionaries
        """
        blocks = []

        # Split by double newlines to get paragraphs
        paragraphs = markdown.split('\n\n')

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            # Check if it's an image
            if para.startswith('!['):
                # Extract image index from the markdown
                match = re.search(r'!\[.*?\]\(images/image_(\d+)\.jpg\)', para)
                if match:
                    idx = int(match.group(1))
                    if idx < len(image_refs):
                        _, ref_type, det_coords = image_refs[idx]
                        bbox = self._parse_bbox(det_coords)
                        blocks.append({
                            "type": BlockType.IMAGE,
                            "content": "",
                            "bbox": bbox
                        })
                continue

            # Check if it's a title (starts with ##)
            if para.startswith('##'):
                title_text = para.lstrip('#').strip()
                blocks.append({
                    "type": BlockType.TITLE,
                    "content": title_text,
                    "bbox": []
                })
                continue

            # Check if it's a code block
            if para.startswith('```'):
                code_content = para.strip('`').strip()
                blocks.append({
                    "type": BlockType.CODE,
                    "content": code_content,
                    "bbox": []
                })
                continue

            # Check if it's an equation block
            if para.startswith('$$'):
                equation_content = para.strip('$').strip()
                blocks.append({
                    "type": BlockType.EQUATION_BLOCK,
                    "content": equation_content,
                    "bbox": []
                })
                continue

            # Check if it's a table (contains |)
            if '|' in para and para.count('|') >= 2:
                blocks.append({
                    "type": BlockType.TABLE,
                    "content": para,
                    "bbox": []
                })
                continue

            # Default to text paragraph
            blocks.append({
                "type": BlockType.TEXT,
                "content": para,
                "bbox": []
            })

        return blocks

    def _parse_bbox(self, det_coords: str) -> List[float]:
        """
        Parse detection coordinates from DeepSeek-OCR output

        Args:
            det_coords: String containing coordinates, e.g., "[[x1, y1, x2, y2]]"

        Returns:
            Normalized bounding box [x1, y1, x2, y2] in range [0, 1]
        """
        try:
            # Parse the coordinate list
            coords_list = eval(det_coords)

            if not coords_list or not isinstance(coords_list, list):
                return []

            # Get first bbox (could be multiple)
            if isinstance(coords_list[0], list) and len(coords_list[0]) >= 4:
                bbox = coords_list[0][:4]
                # DeepSeek-OCR uses 0-999 normalized coordinates
                # Convert to 0-1 range for consistency
                return [coord / 999.0 for coord in bbox]

            return []
        except Exception as e:
            print(f"Warning: Could not parse bbox from '{det_coords}': {e}")
            return []

    def extract_images_from_refs(self, image_refs: List[Tuple],
                                source_image) -> Dict[int, str]:
        """
        Extract and save images from bounding boxes

        Args:
            image_refs: List of (full_match, type, coords) tuples
            source_image: PIL Image to crop from

        Returns:
            Dictionary mapping image index to saved file path
        """
        from PIL import Image
        import os

        saved_images = {}

        for idx, (_, ref_type, det_coords) in enumerate(image_refs):
            bbox = self._parse_bbox(det_coords)
            if not bbox or len(bbox) != 4:
                continue

            try:
                # Convert normalized bbox to pixel coordinates
                img_width, img_height = source_image.size
                x1 = int(bbox[0] * img_width)
                y1 = int(bbox[1] * img_height)
                x2 = int(bbox[2] * img_width)
                y2 = int(bbox[3] * img_height)

                # Crop and save
                cropped = source_image.crop((x1, y1, x2, y2))

                # Convert to RGB if necessary
                if cropped.mode in ('RGBA', 'LA', 'P'):
                    rgb_image = Image.new('RGB', cropped.size, (255, 255, 255))
                    if cropped.mode == 'P':
                        cropped = cropped.convert('RGBA')
                    rgb_image.paste(cropped, mask=cropped.split()[-1] if cropped.mode in ('RGBA', 'LA') else None)
                    cropped = rgb_image

                saved_images[idx] = cropped

            except Exception as e:
                print(f"Warning: Could not extract image {idx}: {e}")
                continue

        return saved_images
