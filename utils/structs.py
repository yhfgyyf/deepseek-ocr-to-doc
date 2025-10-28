"""
Data structures for document conversion
Defines block types and content structures without external dependencies
"""

class BlockType:
    """Content block types for document structure"""

    # Text blocks
    TEXT = "text"
    TITLE = "title"

    # Visual elements
    IMAGE = "image"
    TABLE = "table"

    # Code and equations
    CODE = "code"
    ALGORITHM = "algorithm"
    EQUATION = "equation"
    EQUATION_BLOCK = "equation_block"

    # Lists
    LIST = "list"

    # Captions
    TABLE_CAPTION = "table_caption"
    IMAGE_CAPTION = "image_caption"
    CODE_CAPTION = "code_caption"

    # References and metadata
    REF_TEXT = "ref_text"
    HEADER = "header"
    FOOTER = "footer"
    PAGE_NUMBER = "page_number"

    # Footnotes
    PAGE_FOOTNOTE = "page_footnote"
    TABLE_FOOTNOTE = "table_footnote"
    IMAGE_FOOTNOTE = "image_footnote"

    # Other
    ASIDE_TEXT = "aside_text"
    PHONETIC = "phonetic"


class ContentBlock:
    """
    Represents a content block in a document

    Attributes:
        type: BlockType constant indicating block type
        content: Text content of the block
        bbox: Bounding box coordinates [x1, y1, x2, y2] (normalized 0-999)
        metadata: Additional metadata (e.g., caption, language for code)
    """

    def __init__(self, block_type: str, content: str = "", bbox: list = None, **metadata):
        self.type = block_type
        self.content = content
        self.bbox = bbox or []
        self.metadata = metadata

    def to_dict(self):
        """Convert to dictionary format"""
        return {
            "type": self.type,
            "content": self.content,
            "bbox": self.bbox,
            **self.metadata
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary"""
        block_type = data.get("type", BlockType.TEXT)
        content = data.get("content", "")
        bbox = data.get("bbox", [])

        # Extract metadata (everything except type, content, bbox)
        metadata = {k: v for k, v in data.items() if k not in ["type", "content", "bbox"]}

        return cls(block_type, content, bbox, **metadata)
