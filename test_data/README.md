# Test Data Directory

This directory contains sample test files and expected outputs for the DeepSeek-OCR document conversion tool.

## Directory Structure

```
test_data/
├── input/                     # Sample input files
│   ├── ocr_demo.png          # Sample image (2.3MB)
│   ├── 2021年成都统计公报.pdf  # Statistical report (850KB)
│   ├── 2022年成都统计公报.pdf  # Statistical report (703KB)
│   └── DeepSeek_OCR_paper.pdf # Research paper (7.3MB)
│
└── output/                    # Sample conversion outputs
    ├── ocr_demo.md           # Markdown output
    ├── ocr_demo.docx         # Word output
    ├── 2021年成都统计公报.md   # Markdown output
    ├── images_ocr_demo/      # Extracted images for ocr_demo
    └── images_2021年成都统计公报/ # Extracted images for report
```

## Quick Start

### Test Single File Conversion

Convert an image to Markdown:
```bash
python run_doc_conversion.py test_data/input/ocr_demo.png -o test_output
```

Convert an image to Word:
```bash
python run_doc_conversion.py test_data/input/ocr_demo.png -f docx -o test_output
```

Convert a PDF to Markdown:
```bash
python run_doc_conversion.py test_data/input/2021年成都统计公报.pdf -o test_output
```

### Test Batch Processing

Convert all files in the input directory:
```bash
python run_doc_conversion.py test_data/input -o test_output
```

Convert to Word format:
```bash
python run_doc_conversion.py test_data/input -f docx -o test_output
```

## Sample Files Description

### Input Files

1. **ocr_demo.png** (2.3MB)
   - Complex document layout with multiple columns
   - Contains text, images, and formatting
   - Good for testing image OCR

2. **2021年成都统计公报.pdf** (850KB)
   - Multi-page statistical report (18 pages)
   - Contains tables, charts, and structured data
   - Tests PDF processing and table recognition

3. **2022年成都统计公报.pdf** (703KB)
   - Multi-page statistical report (17 pages)
   - Similar structure to 2021 report
   - Tests consistency across similar documents

4. **DeepSeek_OCR_paper.pdf** (7.3MB)
   - Research paper with complex formatting
   - Contains equations, figures, and references
   - Tests academic document processing

### Output Files

The `output/` directory contains sample conversion results demonstrating:
- Markdown format with LaTeX formulas
- Word document with proper formatting
- Extracted images organized in subdirectories
- Preserved document structure and content

## Expected Results

When processing the sample files, you should expect:

- **Processing Time**: 1-3 minutes per file depending on complexity
- **Image Quality**: Extracted images at 95% JPEG quality
- **Structure Preservation**: Titles, paragraphs, tables, and formulas maintained
- **Format Support**: Both .md and .docx formats work correctly

## Comparing Outputs

To verify your conversion results:

1. Compare your output with sample outputs in `test_data/output/`
2. Check that extracted images match in `images_*/` directories
3. Verify document structure and formatting are preserved

## Adding Your Own Test Files

To add custom test files:

```bash
# Copy your files to input directory
cp /path/to/your/file.pdf test_data/input/
cp /path/to/your/image.png test_data/input/

# Run conversion
python run_doc_conversion.py test_data/input -o my_output
```

## Notes

- Sample output files are provided for reference only
- Actual OCR results may vary slightly based on model version
- Large test files are tracked in git for easy sharing
- Processing times depend on GPU and system resources
