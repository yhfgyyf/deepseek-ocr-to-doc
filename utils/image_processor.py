"""
Image processing utilities for OCR
"""
import base64
import io
from PIL import Image
from typing import Union


def load_image(image_path: str) -> Image.Image:
    """
    Load image from file path

    Args:
        image_path: Path to image file

    Returns:
        PIL Image object
    """
    try:
        image = Image.open(image_path)
        # Convert to RGB if needed
        if image.mode not in ('RGB', 'L'):
            image = image.convert('RGB')
        return image
    except Exception as e:
        raise ValueError(f"Failed to load image from {image_path}: {e}")


def image_to_base64(image: Union[str, Image.Image]) -> str:
    """
    Convert image to base64 string for API transmission

    Args:
        image: PIL Image object or path to image file

    Returns:
        Base64 encoded string
    """
    if isinstance(image, str):
        image = load_image(image)

    # Convert image to bytes
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()

    # Encode to base64
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    return img_base64


def resize_image_if_needed(image: Image.Image, max_size: int = 2048) -> Image.Image:
    """
    Resize image if it exceeds max size while maintaining aspect ratio

    Args:
        image: PIL Image object
        max_size: Maximum dimension size

    Returns:
        Resized PIL Image object
    """
    width, height = image.size
    if width <= max_size and height <= max_size:
        return image

    # Calculate new dimensions
    if width > height:
        new_width = max_size
        new_height = int(height * (max_size / width))
    else:
        new_height = max_size
        new_width = int(width * (max_size / height))

    return image.resize((new_width, new_height), Image.LANCZOS)
