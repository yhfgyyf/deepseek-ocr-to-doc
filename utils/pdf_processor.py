"""
PDF processing utilities for OCR
"""
import fitz  # PyMuPDF
from PIL import Image
import io
from typing import List, Dict, Tuple


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


def extract_embedded_images(pdf_path: str) -> Tuple[Dict[int, List[Image.Image]], Dict[int, List[Tuple[float, float, float, float]]]]:
    """
    Extract embedded images directly from PDF pages

    This extracts the actual image objects embedded in the PDF,
    not screenshots of the rendered page. This preserves original
    image quality and content.

    Args:
        pdf_path: Path to PDF file

    Returns:
        Tuple of two dicts:
        - images_by_page: Dict mapping page_num (0-indexed) to list of PIL Images
        - bboxes_by_page: Dict mapping page_num to list of normalized bboxes (x0, y0, x1, y1)
    """
    images_by_page = {}
    bboxes_by_page = {}

    try:
        pdf_document = fitz.open(pdf_path)

        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            page_images = []
            page_bboxes = []

            # Get image list for this page
            image_list = page.get_images()

            for img_index, img_info in enumerate(image_list):
                try:
                    # Extract image
                    xref = img_info[0]
                    base_image = pdf_document.extract_image(xref)
                    image_bytes = base_image["image"]

                    # Convert to PIL Image
                    pil_image = Image.open(io.BytesIO(image_bytes))

                    # Convert to RGB if needed
                    if pil_image.mode not in ('RGB', 'L'):
                        pil_image = pil_image.convert('RGB')

                    # Get image bbox on page (normalized to 0-1 range)
                    # Find all instances of this image on the page
                    image_rects = page.get_image_rects(xref)
                    if image_rects:
                        # Use first rect if multiple instances
                        rect = image_rects[0]
                        page_width = page.rect.width
                        page_height = page.rect.height

                        # Normalize coordinates to 0-1 range
                        x0 = rect.x0 / page_width
                        y0 = rect.y0 / page_height
                        x1 = rect.x1 / page_width
                        y1 = rect.y1 / page_height

                        page_images.append(pil_image)
                        page_bboxes.append((x0, y0, x1, y1))
                    else:
                        # If no rect found, still save the image but without bbox
                        page_images.append(pil_image)
                        page_bboxes.append(None)

                except Exception as e:
                    print(f"Warning: Failed to extract image {img_index} from page {page_num + 1}: {e}")
                    continue

            if page_images:
                images_by_page[page_num] = page_images
                bboxes_by_page[page_num] = page_bboxes

        pdf_document.close()

    except Exception as e:
        raise ValueError(f"Failed to extract embedded images from PDF {pdf_path}: {e}")

    return images_by_page, bboxes_by_page
