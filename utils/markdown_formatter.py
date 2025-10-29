"""
Markdown formatter for OCR output
Converts MinerU ContentBlocks to markdown format
"""
import os
from typing import List, Dict, Any, Optional
from PIL import Image
from .structs import BlockType


class MarkdownFormatter:
    """Format OCR results to markdown"""

    def __init__(self, output_dir: str, image_dir: str = "images"):
        """
        Initialize formatter

        Args:
            output_dir: Output directory for markdown files
            image_dir: Directory name for images (relative to output_dir)
        """
        self.output_dir = output_dir
        self.image_dir = image_dir
        self.image_output_dir = os.path.join(output_dir, image_dir)
        os.makedirs(self.image_output_dir, exist_ok=True)
        self.image_counter = 0
        self.current_image = None  # Store current source image for cropping

    def format_blocks(self, blocks: List[Dict[str, Any]], source_image: Optional[Image.Image] = None) -> str:
        """
        Convert ContentBlocks to markdown

        Args:
            blocks: List of ContentBlock dictionaries
            source_image: Source image for cropping images from bbox (optional)

        Returns:
            Markdown formatted string
        """
        self.current_image = source_image
        markdown_lines = []

        for block in blocks:
            block_type = block.get("type", "")
            content = block.get("content", "")

            if not content and block_type not in [BlockType.IMAGE]:
                continue

            formatted = self._format_block(block_type, content, block)
            if formatted:
                markdown_lines.append(formatted)

        return "\n\n".join(markdown_lines)

    def _format_block(self, block_type: str, content: str, block: Dict) -> str:
        """Format individual block based on type"""

        if block_type == BlockType.TITLE:
            # Determine heading level (could be enhanced with more logic)
            return f"## {content}"

        elif block_type == BlockType.TEXT:
            return content

        elif block_type == BlockType.TABLE:
            # Content should already be in markdown table format
            return content

        elif block_type == BlockType.IMAGE:
            # Save image and return markdown image reference
            image_path = self._save_image_from_bbox(block)
            if image_path:
                caption = block.get("caption", "")
                if caption:
                    return f"![{caption}]({image_path})\n*{caption}*"
                return f"![]({image_path})"
            return ""

        elif block_type == BlockType.CODE:
            # Wrap in code block
            return f"```\n{content}\n```"

        elif block_type == BlockType.ALGORITHM:
            # Format as algorithm/pseudocode
            return f"```algorithm\n{content}\n```"

        elif block_type == BlockType.EQUATION:
            # Inline or display equation
            if "\n" in content or len(content) > 50:
                return f"$$\n{content}\n$$"
            else:
                return f"${content}$"

        elif block_type == BlockType.EQUATION_BLOCK:
            return f"$$\n{content}\n$$"

        elif block_type == BlockType.LIST:
            return content

        elif block_type == BlockType.TABLE_CAPTION:
            return f"*Table: {content}*"

        elif block_type == BlockType.IMAGE_CAPTION:
            return f"*Figure: {content}*"

        elif block_type == BlockType.CODE_CAPTION:
            return f"*Code: {content}*"

        elif block_type == BlockType.REF_TEXT:
            return f"> {content}"

        elif block_type == BlockType.HEADER:
            return f"<!-- Header: {content} -->"

        elif block_type == BlockType.FOOTER:
            return f"<!-- Footer: {content} -->"

        elif block_type == BlockType.PAGE_NUMBER:
            return f"<!-- Page {content} -->"

        elif block_type == BlockType.PAGE_FOOTNOTE:
            return f"[^{self.image_counter}]: {content}"

        elif block_type == BlockType.TABLE_FOOTNOTE:
            return f"*Note: {content}*"

        elif block_type == BlockType.IMAGE_FOOTNOTE:
            return f"*Note: {content}*"

        elif block_type == BlockType.ASIDE_TEXT:
            return f"<!-- Aside: {content} -->"

        elif block_type == BlockType.PHONETIC:
            return content

        else:
            # Unknown or unhandled type
            return content

    def _save_image_from_bbox(self, block: Dict) -> Optional[str]:
        """
        Crop and save image from bbox

        Args:
            block: ContentBlock containing bbox information

        Returns:
            Relative path to saved image, or None if failed
        """
        # Check if block has embedded image (from PDF) - use it directly
        if "embedded_image" in block:
            try:
                embedded_img = block["embedded_image"]

                # Convert to RGB if necessary
                if embedded_img.mode in ('RGBA', 'LA', 'P'):
                    rgb_image = Image.new('RGB', embedded_img.size, (255, 255, 255))
                    if embedded_img.mode == 'P':
                        embedded_img = embedded_img.convert('RGBA')
                    rgb_image.paste(embedded_img, mask=embedded_img.split()[-1] if embedded_img.mode in ('RGBA', 'LA') else None)
                    embedded_img = rgb_image

                # Save to file
                self.image_counter += 1
                image_filename = f"image_{self.image_counter}.jpg"
                image_path = os.path.join(self.image_output_dir, image_filename)
                embedded_img.save(image_path, "JPEG", quality=95)

                return f"{self.image_dir}/{image_filename}"

            except Exception as e:
                print(f"Warning: Failed to save embedded image {self.image_counter}: {e}")
                # Fall through to regular processing

        # Determine source image for cropping
        source_image = block.get("source_image") or self.current_image

        if not source_image:
            # No source image, just generate placeholder
            self.image_counter += 1
            return f"{self.image_dir}/image_{self.image_counter}.jpg"

        bbox = block.get("bbox")
        if not bbox or len(bbox) != 4:
            return None

        try:
            # bbox is normalized [0, 1], convert to pixel coordinates
            img_width, img_height = source_image.size
            x1 = int(bbox[0] * img_width)
            y1 = int(bbox[1] * img_height)
            x2 = int(bbox[2] * img_width)
            y2 = int(bbox[3] * img_height)

            # Ensure valid coordinates
            x1, x2 = max(0, min(x1, img_width)), max(0, min(x2, img_width))
            y1, y2 = max(0, min(y1, img_height)), max(0, min(y2, img_height))

            if x2 <= x1 or y2 <= y1:
                return None

            # Crop image
            cropped = source_image.crop((x1, y1, x2, y2))

            # Convert to RGB if necessary (JPEG doesn't support RGBA)
            if cropped.mode in ('RGBA', 'LA', 'P'):
                rgb_image = Image.new('RGB', cropped.size, (255, 255, 255))
                if cropped.mode == 'P':
                    cropped = cropped.convert('RGBA')
                rgb_image.paste(cropped, mask=cropped.split()[-1] if cropped.mode in ('RGBA', 'LA') else None)
                cropped = rgb_image

            # Save to file
            self.image_counter += 1
            image_filename = f"image_{self.image_counter}.jpg"
            image_path = os.path.join(self.image_output_dir, image_filename)
            cropped.save(image_path, "JPEG", quality=95)

            return f"{self.image_dir}/{image_filename}"

        except Exception as e:
            print(f"Warning: Failed to save image {self.image_counter}: {e}")
            return None

    def save_markdown(self, markdown_content: str, filename: str) -> str:
        """
        Save markdown content to file

        Args:
            markdown_content: Markdown formatted string
            filename: Output filename

        Returns:
            Path to saved file
        """
        output_path = os.path.join(self.output_dir, filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        return output_path
