# DeepSeek-OCR Document Converter

[English](#english) | [中文](#chinese)

---

## English

A powerful document conversion tool that converts images and PDFs to Markdown or Word documents using [DeepSeek-OCR](https://github.com/deepseek-ai/DeepSeek-OCR) model.

> **Note**: This project is based on the official [DeepSeek-OCR](https://github.com/deepseek-ai/DeepSeek-OCR) model. Please refer to the official repository for model downloads and detailed information.

### Features

- 🖼️ **Image to Document**: Convert JPG, PNG, TIFF, BMP images to structured documents
- 📄 **PDF to Document**: Convert multi-page PDFs to structured documents
- 📁 **Batch Processing**: Process entire directories of images and PDFs automatically
- 📝 **Dual Format Output**: Generate both Markdown (.md) and Word (.docx) formats
- 🎯 **Content Preservation**: Maintains titles, paragraphs, images, tables, and formulas
- 🧮 **Math Formula Support**: Full support for LaTeX math formulas
- 📊 **Table Recognition**: Preserves table structure and formatting
- 🔀 **Smart Organization**: Separate image folders for each file to avoid conflicts
- 🚀 **High Performance**: Powered by vLLM for efficient inference

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Single file conversion
python run_doc_conversion.py /path/to/image.jpg                    # To Markdown
python run_doc_conversion.py /path/to/image.jpg -f docx           # To Word
python run_doc_conversion.py /path/to/document.pdf -f docx        # PDF to Word

# Batch processing (NEW!)
python run_doc_conversion.py /path/to/directory -o ./output       # Convert all files
python run_doc_conversion.py /path/to/directory -f docx -o ./out  # Batch to Word
```

### Requirements

- Python 3.9+
- CUDA-capable GPU
- DeepSeek-OCR model
- vLLM >= 0.11.0 with DeepSeek-OCR support (requires [PR #27247](https://github.com/vllm-project/vllm/pull/27247))

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

一个强大的文档转换工具，使用 [DeepSeek-OCR](https://github.com/deepseek-ai/DeepSeek-OCR) 模型将图片和 PDF 转换为 Markdown 或 Word 文档。

> **说明**: 本项目基于官方 [DeepSeek-OCR](https://github.com/deepseek-ai/DeepSeek-OCR) 模型。模型下载和详细信息请参考官方仓库。

### 功能特性

- 🖼️ **图片转文档**: 支持 JPG、PNG、TIFF、BMP 等格式转换为结构化文档
- 📄 **PDF 转文档**: 支持多页 PDF 转换为结构化文档
- 📁 **批量处理**: 自动处理整个目录的图片和 PDF 文件
- 📝 **双格式输出**: 可生成 Markdown (.md) 和 Word (.docx) 格式
- 🎯 **内容保留**: 完整保留标题、段落、图片、表格和公式
- 🧮 **数学公式支持**: 完整支持 LaTeX 数学公式
- 📊 **表格识别**: 保留表格结构和格式
- 🔀 **智能组织**: 为每个文件创建独立图片文件夹，避免冲突
- 🚀 **高性能**: 基于 vLLM 实现高效推理

### 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 单文件转换
python run_doc_conversion.py /path/to/image.jpg                    # 转为 Markdown
python run_doc_conversion.py /path/to/image.jpg -f docx           # 转为 Word
python run_doc_conversion.py /path/to/document.pdf -f docx        # PDF 转 Word

# 批量处理（新功能！）
python run_doc_conversion.py /path/to/directory -o ./output       # 转换所有文件
python run_doc_conversion.py /path/to/directory -f docx -o ./out  # 批量转为 Word
```

### 环境要求

- Python 3.9+
- 支持 CUDA 的 GPU
- DeepSeek-OCR 模型
- vLLM >= 0.11.0（需要支持 DeepSeek-OCR，参考 [PR #27247](https://github.com/vllm-project/vllm/pull/27247)）

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
