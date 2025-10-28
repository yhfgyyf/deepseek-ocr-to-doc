"""
PDF processing utilities for OCR
"""
import fitz  # PyMuPDF
from PIL import Image
import io
from typing import List


def pdf_to_images(pdf_path: str, dpi: int = 200) -> List[Image.Image]:
    """
    Convert PDF pages to images

    Args:
        pdf_path: Path to PDF file
        dpi: Resolution for rendering (default 200)

    Returns:
        List of PIL Image objects, one per page
    """
    images = []

    try:
        pdf_document = fitz.open(pdf_path)

        # Calculate zoom factor from DPI
        zoom = dpi / 72.0
        matrix = fitz.Matrix(zoom, zoom)

        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]

            # Render page to pixmap
            pixmap = page.get_pixmap(matrix=matrix, alpha=False)

            # Convert pixmap to PIL Image
            img_data = pixmap.tobytes("png")
            img = Image.open(io.BytesIO(img_data))

            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')

            images.append(img)

        pdf_document.close()

    except Exception as e:
        raise ValueError(f"Failed to process PDF {pdf_path}: {e}")

    return images


def get_pdf_page_count(pdf_path: str) -> int:
    """
    Get number of pages in PDF

    Args:
        pdf_path: Path to PDF file

    Returns:
        Number of pages
    """
    try:
        pdf_document = fitz.open(pdf_path)
        page_count = pdf_document.page_count
        pdf_document.close()
        return page_count
    except Exception as e:
        raise ValueError(f"Failed to open PDF {pdf_path}: {e}")
