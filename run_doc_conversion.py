#!/usr/bin/env python3
"""
Document Conversion Tool using DeepSeek-OCR
Converts images and PDFs to Markdown or Word documents
"""

import asyncio
import argparse
import os
import sys
from pathlib import Path
from typing import Optional

import torch
if torch.version.cuda == '11.8':
    os.environ["TRITON_PTXAS_PATH"] = "/usr/local/cuda-11.8/bin/ptxas"

from PIL import Image, ImageOps
from vllm import AsyncLLMEngine, SamplingParams
from vllm.engine.arg_utils import AsyncEngineArgs

from utils.deepseek_parser import DeepSeekOCRParser
from utils.markdown_formatter import MarkdownFormatter
from utils.word_formatter import WordFormatter
from utils.pdf_processor import pdf_to_images, get_pdf_page_count
from utils.image_processor import load_image
from config import MODEL_PATH, OUTPUT_PATH


class DocumentConverter:
    """Convert images/PDFs to structured documents using DeepSeek-OCR"""

    def __init__(self, model_path: str, output_dir: str, output_format: str = "md",
                 gpu_id: str = "0"):
        """
        Initialize converter

        Args:
            model_path: Path to DeepSeek-OCR model
            output_dir: Output directory for converted documents
            output_format: Output format ("md" or "word")
            gpu_id: GPU device ID
        """
        self.model_path = model_path
        self.output_dir = output_dir
        self.output_format = output_format.lower()

        os.environ["CUDA_VISIBLE_DEVICES"] = gpu_id
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, "images"), exist_ok=True)

        # Initialize components
        self.parser = DeepSeekOCRParser()

        if self.output_format == "word":
            self.formatter = WordFormatter(output_dir)
        else:
            self.formatter = MarkdownFormatter(output_dir)

        self.engine = None

    async def initialize_engine(self):
        """Initialize vLLM engine"""
        print("Initializing DeepSeek-OCR engine...")
        engine_args = AsyncEngineArgs(
            model=self.model_path,
            max_model_len=8192,
            enforce_eager=False,
            trust_remote_code=True,
            tensor_parallel_size=1,
            gpu_memory_utilization=0.75,
        )
        self.engine = AsyncLLMEngine.from_engine_args(engine_args)
        print("Engine initialized successfully!")

    def load_image_with_exif(self, image_path: str) -> Image.Image:
        """Load image and handle EXIF orientation"""
        try:
            image = Image.open(image_path)
            corrected_image = ImageOps.exif_transpose(image)
            return corrected_image.convert('RGB')
        except Exception as e:
            print(f"Warning: Error loading image: {e}")
            try:
                return Image.open(image_path).convert('RGB')
            except:
                return None

    async def ocr_image(self, image: Image.Image, prompt: str = None) -> str:
        """
        Perform OCR on image

        Args:
            image: PIL Image object
            prompt: Custom prompt (default: grounding markdown conversion)

        Returns:
            OCR text output
        """
        if prompt is None:
            prompt = '<image>\n<|grounding|>Convert the document to markdown.'

        sampling_params = SamplingParams(
            temperature=0.0,
            max_tokens=8192,
            skip_special_tokens=False,
        )

        request_id = f"request-{id(image)}"

        # Prepare request
        if '<image>' in prompt:
            request = {
                "prompt": prompt,
                "multi_modal_data": {"image": image}
            }
        else:
            request = {"prompt": prompt}

        # Stream generation
        printed_length = 0
        final_output = ""

        async for request_output in self.engine.generate(
            request, sampling_params, request_id
        ):
            if request_output.outputs:
                full_text = request_output.outputs[0].text
                new_text = full_text[printed_length:]
                print(new_text, end='', flush=True)
                printed_length = len(full_text)
                final_output = full_text

        print()  # Newline after generation
        return final_output

    async def convert_image(self, image_path: str, output_name: Optional[str] = None) -> str:
        """
        Convert single image to document

        Args:
            image_path: Path to image file
            output_name: Output filename (without extension)

        Returns:
            Path to generated document
        """
        print(f"\n{'='*60}")
        print(f"Converting image: {image_path}")
        print(f"{'='*60}\n")

        # Load image
        image = self.load_image_with_exif(image_path)
        if image is None:
            raise ValueError(f"Failed to load image: {image_path}")

        # Perform OCR
        print("Running OCR...")
        ocr_output = await self.ocr_image(image)

        # Parse output
        print("\nParsing OCR output...")
        cleaned_markdown, blocks = self.parser.parse(ocr_output)

        # Save raw output for reference
        if output_name is None:
            output_name = Path(image_path).stem

        raw_output_path = os.path.join(self.output_dir, f"{output_name}_raw.mmd")
        with open(raw_output_path, 'w', encoding='utf-8') as f:
            f.write(ocr_output)
        print(f"Raw output saved to: {raw_output_path}")

        # Format and save document
        print(f"Formatting as {self.output_format.upper()}...")

        if self.output_format == "word":
            # Format to Word
            self.formatter.format_blocks(blocks, source_image=image)
            output_path = os.path.join(self.output_dir, f"{output_name}.docx")
            self.formatter.save(output_path)
            print(f"Word document saved to: {output_path}")
        else:
            # Format to Markdown
            markdown_content = self.formatter.format_blocks(blocks, source_image=image)
            output_path = os.path.join(self.output_dir, f"{output_name}.md")
            self.formatter.save_markdown(markdown_content, f"{output_name}.md")
            print(f"Markdown document saved to: {output_path}")

        return output_path

    async def convert_pdf(self, pdf_path: str, output_name: Optional[str] = None) -> str:
        """
        Convert PDF to document

        Args:
            pdf_path: Path to PDF file
            output_name: Output filename (without extension)

        Returns:
            Path to generated document
        """
        print(f"\n{'='*60}")
        print(f"Converting PDF: {pdf_path}")
        print(f"{'='*60}\n")

        # Convert PDF to images
        print("Converting PDF to images...")
        page_count = get_pdf_page_count(pdf_path)
        print(f"PDF has {page_count} page(s)")

        images = pdf_to_images(pdf_path, dpi=200)
        print(f"Converted {len(images)} pages to images")

        if output_name is None:
            output_name = Path(pdf_path).stem

        # Initialize combined output
        all_blocks = []
        all_markdown = []

        # Process each page
        for page_num, image in enumerate(images, 1):
            print(f"\n--- Processing page {page_num}/{len(images)} ---")

            # Perform OCR
            ocr_output = await self.ocr_image(image)

            # Parse output
            cleaned_markdown, blocks = self.parser.parse(ocr_output)

            # Add page separator
            if page_num > 1:
                all_blocks.append({
                    "type": "page_number",
                    "content": f"Page {page_num}",
                    "bbox": []
                })

            all_blocks.extend(blocks)
            all_markdown.append(cleaned_markdown)

        # Save combined raw output
        raw_output_path = os.path.join(self.output_dir, f"{output_name}_raw.mmd")
        with open(raw_output_path, 'w', encoding='utf-8') as f:
            f.write('\n\n---\n\n'.join(all_markdown))
        print(f"\nRaw output saved to: {raw_output_path}")

        # Format and save document
        print(f"Formatting as {self.output_format.upper()}...")

        if self.output_format == "word":
            # Use last image as source for any remaining image extractions
            self.formatter.format_blocks(all_blocks, source_image=images[-1] if images else None)
            output_path = os.path.join(self.output_dir, f"{output_name}.docx")
            self.formatter.save(output_path)
            print(f"Word document saved to: {output_path}")
        else:
            # Format to Markdown
            markdown_content = self.formatter.format_blocks(all_blocks,
                                                           source_image=images[-1] if images else None)
            output_path = os.path.join(self.output_dir, f"{output_name}.md")
            self.formatter.save_markdown(markdown_content, f"{output_name}.md")
            print(f"Markdown document saved to: {output_path}")

        return output_path


async def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Convert images/PDFs to Markdown or Word documents using DeepSeek-OCR"
    )
    parser.add_argument(
        "input_path",
        help="Path to input image or PDF file"
    )
    parser.add_argument(
        "-f", "--format",
        choices=["md", "docx"],
        default="md",
        help="Output format: md (Markdown) or docx (Word) (default: md)"
    )
    parser.add_argument(
        "-o", "--output",
        default=OUTPUT_PATH,
        help=f"Output directory (default: {OUTPUT_PATH})"
    )
    parser.add_argument(
        "-m", "--model",
        default=MODEL_PATH,
        help=f"Path to DeepSeek-OCR model (default: {MODEL_PATH})"
    )
    parser.add_argument(
        "-g", "--gpu",
        default="0",
        help="GPU device ID (default: 0)"
    )
    parser.add_argument(
        "-n", "--name",
        help="Output filename (without extension)"
    )

    args = parser.parse_args()

    # Validate input file
    if not os.path.exists(args.input_path):
        print(f"Error: Input file not found: {args.input_path}")
        sys.exit(1)

    # Normalize format
    output_format = "word" if args.format == "docx" else "md"

    # Initialize converter
    converter = DocumentConverter(
        model_path=args.model,
        output_dir=args.output,
        output_format=output_format,
        gpu_id=args.gpu
    )

    # Initialize engine
    await converter.initialize_engine()

    # Determine file type and convert
    input_path = Path(args.input_path)
    suffix = input_path.suffix.lower()

    try:
        if suffix == '.pdf':
            output_path = await converter.convert_pdf(str(input_path), args.name)
        elif suffix in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
            output_path = await converter.convert_image(str(input_path), args.name)
        else:
            print(f"Error: Unsupported file type: {suffix}")
            print("Supported types: .pdf, .jpg, .jpeg, .png, .bmp, .tiff")
            sys.exit(1)

        print(f"\n{'='*60}")
        print(f"✓ Conversion complete!")
        print(f"Output saved to: {output_path}")
        print(f"{'='*60}\n")

    except Exception as e:
        print(f"\nError during conversion: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
