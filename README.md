# DeepSeek-OCR Document Converter

[English](#english) | [中文](#chinese)

---

## English

A powerful document conversion tool that converts images and PDFs to Markdown or Word documents using DeepSeek-OCR model.

### Features

- 🖼️ **Image to Document**: Convert JPG, PNG, TIFF, BMP images to structured documents
- 📄 **PDF to Document**: Convert multi-page PDFs to structured documents
- 📝 **Dual Format Output**: Generate both Markdown (.md) and Word (.docx) formats
- 🎯 **Content Preservation**: Maintains titles, paragraphs, images, tables, and formulas
- 🧮 **Math Formula Support**: Full support for LaTeX math formulas
- 📊 **Table Recognition**: Preserves table structure and formatting
- 🚀 **High Performance**: Powered by vLLM for efficient inference

### Quick Start

```bash
# Install dependencies (in vllm-0.11 conda environment)
pip install python-docx PyMuPDF

# Convert image to Markdown
python run_doc_conversion.py /path/to/image.jpg

# Convert image to Word
python run_doc_conversion.py /path/to/image.jpg -f docx

# Convert PDF to Word
python run_doc_conversion.py /path/to/document.pdf -f docx
```

### Requirements

- Python 3.9+
- CUDA-capable GPU
- DeepSeek-OCR model
- Conda environment with vllm >= 0.11.0

### Documentation

📖 [Complete English Documentation](README_DOC_CONVERSION.md)

📖 [完整中文文档](README_DOC_CONVERSION_ZH.md)

### Project Structure

```
DeepSeek-OCR-vllm/
├── run_doc_conversion.py          # Main entry point
├── config.py                       # Configuration
├── utils/                          # Utilities
│   ├── deepseek_parser.py         # DeepSeek-OCR parser
│   ├── markdown_formatter.py      # Markdown formatter
│   ├── word_formatter.py          # Word formatter
│   ├── pdf_processor.py           # PDF processing
│   ├── image_processor.py         # Image processing
│   └── structs.py                 # Data structures
├── README.md                       # This file
├── README_DOC_CONVERSION.md       # English documentation
└── README_DOC_CONVERSION_ZH.md    # Chinese documentation
```

### Example Output

**Markdown Output:**
- Clean markdown format with proper heading hierarchy
- Embedded images with automatic extraction
- Tables in markdown syntax
- Math formulas in LaTeX format

**Word Output:**
- Professional A4 document format
- Chinese-optimized fonts (宋体/黑体)
- Automatic page numbering
- Embedded images and tables
- 1.5x line spacing

### License

This project follows the DeepSeek-OCR license terms.

---

## Chinese

一个强大的文档转换工具，使用 DeepSeek-OCR 模型将图片和 PDF 转换为 Markdown 或 Word 文档。

### 功能特性

- 🖼️ **图片转文档**: 支持 JPG、PNG、TIFF、BMP 等格式转换为结构化文档
- 📄 **PDF 转文档**: 支持多页 PDF 转换为结构化文档
- 📝 **双格式输出**: 可生成 Markdown (.md) 和 Word (.docx) 格式
- 🎯 **内容保留**: 完整保留标题、段落、图片、表格和公式
- 🧮 **数学公式支持**: 完整支持 LaTeX 数学公式
- 📊 **表格识别**: 保留表格结构和格式
- 🚀 **高性能**: 基于 vLLM 实现高效推理

### 快速开始

```bash
# 安装依赖（在 vllm-0.11 conda 环境中）
pip install python-docx PyMuPDF

# 图片转 Markdown
python run_doc_conversion.py /path/to/image.jpg

# 图片转 Word
python run_doc_conversion.py /path/to/image.jpg -f docx

# PDF 转 Word
python run_doc_conversion.py /path/to/document.pdf -f docx
```

### 环境要求

- Python 3.9+
- 支持 CUDA 的 GPU
- DeepSeek-OCR 模型
- 安装了 vllm >= 0.11.0 的 Conda 环境

### 文档

📖 [Complete English Documentation](README_DOC_CONVERSION.md)

📖 [完整中文文档](README_DOC_CONVERSION_ZH.md)

### 项目结构

```
DeepSeek-OCR-vllm/
├── run_doc_conversion.py          # 主程序入口
├── config.py                       # 配置文件
├── utils/                          # 工具包
│   ├── deepseek_parser.py         # DeepSeek-OCR 解析器
│   ├── markdown_formatter.py      # Markdown 格式化器
│   ├── word_formatter.py          # Word 格式化器
│   ├── pdf_processor.py           # PDF 处理
│   ├── image_processor.py         # 图片处理
│   └── structs.py                 # 数据结构
├── README.md                       # 本文件
├── README_DOC_CONVERSION.md       # 英文文档
└── README_DOC_CONVERSION_ZH.md    # 中文文档
```

### 输出示例

**Markdown 输出:**
- 清晰的 Markdown 格式，正确的标题层级
- 嵌入图片并自动提取
- Markdown 语法的表格
- LaTeX 格式的数学公式

**Word 输出:**
- 专业的 A4 文档格式
- 中文优化字体（宋体/黑体）
- 自动页码
- 嵌入图片和表格
- 1.5 倍行距

### 许可证

本项目遵循 DeepSeek-OCR 许可条款。
