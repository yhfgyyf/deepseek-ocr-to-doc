# Test Data Directory

This directory contains test data for the DeepSeek-OCR document conversion tool.

## Directory Structure

```
test_data/
├── images/          # Place test images here (JPG, PNG, TIFF, BMP)
├── pdfs/            # Place test PDF files here
└── mixed/           # Mixed images and PDFs for batch testing
```

## How to Add Test Files

1. **Add test images**:
   - Place JPG, PNG, TIFF, or BMP files in `test_data/images/`

2. **Add test PDFs**:
   - Place PDF files in `test_data/pdfs/`

3. **Mixed batch testing**:
   - Place both images and PDFs in `test_data/mixed/`

## Running Tests

### Single File Test
```bash
# Test with an image
python run_doc_conversion.py test_data/images/sample.png -o output

# Test with a PDF
python run_doc_conversion.py test_data/pdfs/document.pdf -f docx -o output
```

### Batch Directory Test
```bash
# Test batch processing
python run_doc_conversion.py test_data/mixed -o output

# Batch to Word format
python run_doc_conversion.py test_data/pdfs -f docx -o output
```

## Sample Test Data

You can obtain sample test data from:
- Public domain documents
- Your own scanned documents
- Screenshots of text-rich content
- Academic papers (with proper permissions)

## Note

- Large test files (PDFs, images) are excluded from git via `.gitignore`
- This keeps the repository size manageable
- Each developer can maintain their own local test data
