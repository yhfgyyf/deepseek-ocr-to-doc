# Test Data Guide

[English](#english) | [中文](#chinese)

---

## English

This guide explains how to prepare test data for the document conversion tool.

### Supported File Types

The tool supports the following file formats:
- **Images**: JPG, JPEG, PNG, BMP, TIFF, TIF
- **Documents**: PDF

### Test Data Directory Structure

You can organize your test files in any directory structure. Here's a recommended layout:

```
test_data/
├── images/
│   ├── sample1.png
│   ├── sample2.jpg
│   └── document_scan.tiff
├── pdfs/
│   ├── report.pdf
│   └── paper.pdf
└── mixed/
    ├── image.png
    └── document.pdf
```

### Sample Test Commands

**Single file conversion:**
```bash
# Convert single image to Markdown
python run_doc_conversion.py test_data/images/sample1.png -o output

# Convert single PDF to Word
python run_doc_conversion.py test_data/pdfs/report.pdf -f docx -o output
```

**Batch directory conversion:**
```bash
# Convert all files in a directory to Markdown
python run_doc_conversion.py test_data/mixed -o output

# Convert all files in a directory to Word
python run_doc_conversion.py test_data/pdfs -f docx -o output
```

### Output Structure

For batch processing, the tool creates separate image subdirectories for each file:

```
output/
├── sample1.md
├── sample1_raw.mmd
├── images_sample1/
│   └── image_1.jpg
├── report.docx
├── report_raw.mmd
└── images_report/
    ├── image_1.jpg
    └── image_2.jpg
```

### Notes

- Large test files (PDFs, images) are excluded from git via `.gitignore`
- You can use your own test data by placing files in any directory
- The tool automatically handles filename conflicts with numeric suffixes

---

## Chinese

本指南说明如何为文档转换工具准备测试数据。

### 支持的文件类型

工具支持以下文件格式：
- **图片**: JPG, JPEG, PNG, BMP, TIFF, TIF
- **文档**: PDF

### 测试数据目录结构

您可以使用任何目录结构组织测试文件。推荐布局如下：

```
test_data/
├── images/
│   ├── sample1.png
│   ├── sample2.jpg
│   └── document_scan.tiff
├── pdfs/
│   ├── report.pdf
│   └── paper.pdf
└── mixed/
    ├── image.png
    └── document.pdf
```

### 测试命令示例

**单文件转换：**
```bash
# 将单个图片转换为Markdown
python run_doc_conversion.py test_data/images/sample1.png -o output

# 将单个PDF转换为Word
python run_doc_conversion.py test_data/pdfs/report.pdf -f docx -o output
```

**批量目录转换：**
```bash
# 将目录中所有文件转换为Markdown
python run_doc_conversion.py test_data/mixed -o output

# 将目录中所有文件转换为Word
python run_doc_conversion.py test_data/pdfs -f docx -o output
```

### 输出结构

对于批量处理，工具为每个文件创建独立的图片子目录：

```
output/
├── sample1.md
├── sample1_raw.mmd
├── images_sample1/
│   └── image_1.jpg
├── report.docx
├── report_raw.mmd
└── images_report/
    ├── image_1.jpg
    └── image_2.jpg
```

### 注意事项

- 大型测试文件（PDF、图片）通过`.gitignore`排除在git之外
- 您可以将文件放在任何目录中使用自己的测试数据
- 工具自动处理文件名冲突，添加数字后缀
