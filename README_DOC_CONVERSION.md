# Document Conversion Feature

English | [简体中文](README_DOC_CONVERSION_ZH.md)

This feature converts images and PDFs to Markdown (.md) or Word (.docx) documents using DeepSeek-OCR.

## Features

- **Image to Document**: Convert JPG, PNG, TIFF, BMP images to structured documents
- **PDF to Document**: Convert multi-page PDFs to structured documents
- **Output Formats**: Markdown (.md) or Word (.docx)
- **Content Preservation**: Maintains titles, text, images, tables, and formulas
- **Math Formula Support**: Supports LaTeX math formulas in markdown format

## Requirements

- Python 3.9+
- Conda environment: `vllm-0.11`
- GPU: NVIDIA GPU with CUDA support
- Model: DeepSeek-OCR model

### Dependencies

The following packages are required (already installed in vllm-0.11):
- vllm >= 0.11.0 with DeepSeek-OCR support
  - **Important**: Requires [PR #27247](https://github.com/vllm-project/vllm/pull/27247) for native DeepSeek-OCR support
  - This PR adds `DeepseekOCRForCausalLM` to vLLM's supported models
- torch
- Pillow
- python-docx
- PyMuPDF (fitz)

## Usage

### Basic Usage

Convert image to Markdown:
```bash
python run_doc_conversion.py /path/to/image.jpg
```

Convert image to Word:
```bash
python run_doc_conversion.py /path/to/image.jpg -f docx
```

Convert PDF to Markdown:
```bash
python run_doc_conversion.py /path/to/document.pdf
```

### Command Line Options

```
usage: run_doc_conversion.py [-h] [-f {md,docx}]
                             [-o OUTPUT] [-m MODEL] [-g GPU] [-n NAME]
                             input_path

positional arguments:
  input_path            Path to input image or PDF file

options:
  -h, --help            Show this help message and exit
  -f, --format {md,docx}
                        Output format: md (Markdown) or docx (Word) (default: md)
  -o, --output OUTPUT   Output directory (default: /home/yyf/DeepSeek-OCR/output)
  -m, --model MODEL     Path to DeepSeek-OCR model
  -g, --gpu GPU         GPU device ID (default: 0)
  -n, --name NAME       Output filename (without extension)
```

### Examples

1. **Convert image to Markdown with custom output name**:
```bash
python run_doc_conversion.py test.png -n my_document
# Outputs: my_document.md and my_document_raw.mmd
```

2. **Convert PDF to Word document**:
```bash
python run_doc_conversion.py report.pdf -f docx -o ./results
# Outputs: ./results/report.docx
```

3. **Use specific GPU**:
```bash
python run_doc_conversion.py image.jpg -g 1
```

## Output Files

For each conversion, the following files are generated:

1. **Main Output**:
   - `{name}.md` (Markdown format) or `{name}.docx` (Word format)
   - Cleaned and formatted document

2. **Raw Output**:
   - `{name}_raw.mmd`
   - Original OCR output with grounding tags

3. **Images Directory**:
   - `images/image_*.jpg`
   - Extracted images from the document (if any)

## Document Structure

### Markdown Output

The generated Markdown includes:
- `## Titles` - Second-level headings
- Text paragraphs
- Images: `![](images/image_1.jpg)`
- Tables in Markdown format
- Code blocks: ` ```code``` `
- Equations: `$inline$` or `$$block$$`

### Word Output

The generated Word document includes:
- **Page Format**: A4 (21.0cm × 29.7cm)
- **Margins**: Top/Bottom 2.54cm, Left/Right 3.17cm
- **Fonts**:
  - Body text: 宋体 (SimSun) 10.5pt
  - Titles: 黑体 (SimHei) 14pt, Bold
- **Line Spacing**: 1.5x
- **Page Numbers**: Centered in footer
- **Embedded Images**: Automatically extracted and embedded
- **Tables**: Formatted with "Light Grid Accent 1" style
- **Code**: Monospace font (Consolas) with gray background

## Testing

Test with sample images:
```bash
# Test image conversion (Markdown)
python run_doc_conversion.py /path/to/your/image.png

# Test image conversion (Word)
python run_doc_conversion.py /path/to/your/image.png -f docx
```

Test with sample PDF:
```bash
# Test PDF conversion (this will take longer for multi-page PDFs)
python run_doc_conversion.py /path/to/your/document.pdf -f docx
```

## Architecture

```
run_doc_conversion.py          # Main entry point
├── utils/
│   ├── deepseek_parser.py     # DeepSeek-OCR output parser
│   ├── markdown_formatter.py  # Markdown formatter
│   ├── word_formatter.py      # Word document formatter
│   ├── pdf_processor.py       # PDF processing utilities
│   ├── image_processor.py     # Image processing utilities
│   └── structs.py             # Block type definitions
└── config.py                   # Configuration
```

### Processing Pipeline

```
Input (Image/PDF)
    ↓
[PDF] → Convert to images (PyMuPDF, 200 DPI)
    ↓
[OCR] → DeepSeek-OCR processing
    ↓
[Parse] → Extract content blocks with bbox
    ↓
[Format] → Generate Markdown or Word
    ↓
Output Document + Images
```

## Performance

- **Model Loading**: ~6-8 seconds
- **Image Processing**: ~10-15 seconds per image
- **GPU Memory**: ~6-7 GB (model + KV cache)
- **PDF Processing**: ~10-15 seconds per page

## Troubleshoptions

### Issue: "CUDA out of memory"
**Solution**:
- Reduce `gpu_memory_utilization` in config
- Use smaller images (resize before processing)
- Process fewer PDF pages at once

### Issue: "No module named 'fitz'"
**Solution**:
```bash
conda activate vllm-0.11
pip install PyMuPDF
```

### Issue: "No module named 'docx'"
**Solution**:
```bash
conda activate vllm-0.11
pip install python-docx
```

### Issue: Images not extracted
**Possible causes**:
- Source image not provided to formatter
- Invalid bbox coordinates
- Image region too small

**Check**: Verify that `images/` directory contains extracted images

## Development Notes

This implementation:
- Uses DeepSeek-OCR for high-quality OCR recognition
- Implements custom parsing for DeepSeek-OCR output format with grounding tags
- Provides independent BlockType definitions
- Supports both streaming output and structured document generation
- No external dependencies beyond standard Python packages

## Future Improvements

- [ ] Support for batch processing multiple files
- [ ] Parallel PDF page processing
- [ ] Enhanced table detection and formatting
- [ ] Improved equation rendering in Word
- [ ] Custom styling options for Word output
- [ ] Progress bar for multi-page PDF processing
- [ ] Support for more image formats (WebP, HEIC)

## License

This code is part of the DeepSeek-OCR project and follows the same license terms.
