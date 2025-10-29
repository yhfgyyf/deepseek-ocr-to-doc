# 文档转换功能使用指南

基于 [DeepSeek-OCR](https://github.com/deepseek-ai/DeepSeek-OCR) 的图片和 PDF 转 Markdown/Word 文档转换工具。

> **关于 DeepSeek-OCR**: 本项目基于 DeepSeek AI 开发的官方 [DeepSeek-OCR](https://github.com/deepseek-ai/DeepSeek-OCR) 模型构建。模型下载、技术细节和最新更新请访问官方仓库。

[English](README_DOC_CONVERSION.md) | 简体中文

## 功能特性

- **图片转文档**: 支持将 JPG、PNG、TIFF、BMP 等格式的图片转换为结构化文档
- **PDF 转文档**: 支持多页 PDF 转换为结构化文档
- **批量处理**: 自动处理整个目录的图片和 PDF 文件
- **输出格式**: 支持 Markdown (.md) 和 Word (.docx) 两种格式
- **内容保留**: 完整保留标题、正文、图片、表格和公式
- **数学公式支持**: 支持 LaTeX 格式的数学公式（Markdown 格式）
- **智能组织**: 为每个文件创建独立图片子目录，避免文件名冲突

## 环境要求

- Python 3.9+
- Conda 环境: `vllm-0.11`
- GPU: 需要 NVIDIA GPU 和 CUDA 支持
- 模型: DeepSeek-OCR 模型

### 依赖包

以下依赖包已在 vllm-0.11 环境中安装：
- vllm >= 0.11.0（支持 DeepSeek-OCR）
  - **重要**: 需要 [PR #27247](https://github.com/vllm-project/vllm/pull/27247) 以原生支持 DeepSeek-OCR
  - 该 PR 将 `DeepseekOCRForCausalLM` 添加到 vLLM 的支持模型列表中
- torch
- Pillow
- python-docx
- PyMuPDF (fitz)

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/yhfgyyf/deepseek-ocr-to-doc.git
cd deepseek-ocr-to-doc

# 安装依赖
pip install -r requirements.txt
```

**注意**: 关于支持 DeepSeek-OCR 的 vLLM 安装，请参考 [PR #27247](https://github.com/vllm-project/vllm/pull/27247)。

## 使用方法

### 基础用法

**单文件转换：**

图片转 Markdown：
```bash
python run_doc_conversion.py /path/to/image.jpg
```

图片转 Word：
```bash
python run_doc_conversion.py /path/to/image.jpg -f docx
```

PDF 转 Markdown：
```bash
python run_doc_conversion.py /path/to/document.pdf
```

**批量处理（目录）：**

转换目录中的所有图片和 PDF：
```bash
python run_doc_conversion.py /path/to/directory -o /path/to/output
```

批量转换为 Word 文档：
```bash
python run_doc_conversion.py /path/to/directory -f docx -o /path/to/output
```

### 命令行参数

```
用法: run_doc_conversion.py [-h] [-f {md,docx}]
                             [-o OUTPUT] [-m MODEL] [-g GPU] [-n NAME]
                             input_path

位置参数:
  input_path            输入图片、PDF 文件或包含图片/PDF 的目录路径

选项:
  -h, --help            显示帮助信息并退出
  -f {md,docx}, --format {md,docx}
                        输出格式: md (Markdown) 或 docx (Word)，默认为 md
  -o OUTPUT, --output OUTPUT
                        输出目录，默认为 /home/yyf/DeepSeek-OCR/output
  -m MODEL, --model MODEL
                        DeepSeek-OCR 模型路径
  -g GPU, --gpu GPU     GPU 设备 ID，默认为 0
  -n NAME, --name NAME  输出文件名（不含扩展名），仅用于单文件转换
```

### 使用示例

1. **图片转 Markdown，自定义输出文件名**:
```bash
python run_doc_conversion.py test.png -n my_document
# 输出: my_document.md 和 my_document_raw.mmd
```

2. **PDF 转 Word 文档**:
```bash
python run_doc_conversion.py report.pdf -f docx -o ./results
# 输出: ./results/report.docx
```

3. **批量转换目录中的文件**:
```bash
python run_doc_conversion.py /path/to/documents -o ./output
# 处理目录中所有图片和 PDF 文件
# 为每个文件创建独立的图片子目录:
#   output/file1.md
#   output/images_file1/image_1.jpg
#   output/file2.md
#   output/images_file2/image_1.jpg
```

4. **批量转换为 Word 格式**:
```bash
python run_doc_conversion.py /path/to/documents -f docx -o ./output
# 将所有文件转换为 Word 格式，使用独立的图片文件夹
```

5. **指定 GPU 设备**:
```bash
python run_doc_conversion.py image.jpg -g 1
```

## 输出文件

### 单文件转换

每次转换会生成以下文件：

1. **主要输出**:
   - `{name}.md` (Markdown 格式) 或 `{name}.docx` (Word 格式)
   - 清理和格式化后的文档

2. **原始输出**:
   - `{name}_raw.mmd`
   - 包含定位标签的原始 OCR 输出

3. **图片目录**:
   - `images/image_*.jpg`（单文件默认使用）
   - 从文档中提取的图片（如有）

### 批量处理输出

批量处理时，每个文件都有独立的图片子目录：

```
output/
├── file1.md                    # 转换后的文档
├── file1_raw.mmd              # 原始 OCR 输出
├── images_file1/              # file1 的图片
│   ├── image_1.jpg
│   └── image_2.jpg
├── file2.docx                 # 转换后的文档
├── file2_raw.mmd              # 原始 OCR 输出
└── images_file2/              # file2 的图片
    └── image_1.jpg
```

这种组织方式可以避免处理多个文件时的图片文件名冲突。

## 文档结构

### Markdown 输出

生成的 Markdown 文档包含：
- `## 标题` - 二级标题
- 正文段落
- 图片: `![](images/image_1.jpg)`
- Markdown 格式的表格
- 代码块: ` ```代码``` `
- 公式: `$行内公式$` 或 `$$块级公式$$`

### Word 输出

生成的 Word 文档具有以下格式：
- **页面格式**: A4 纸张 (21.0cm × 29.7cm)
- **页边距**: 上下 2.54cm，左右 3.17cm
- **字体**:
  - 正文: 宋体 10.5pt
  - 标题: 黑体 14pt，加粗
- **行距**: 1.5 倍
- **页码**: 页脚居中显示
- **嵌入图片**: 自动提取并嵌入
- **表格**: 使用"Light Grid Accent 1"样式
- **代码**: 等宽字体 (Consolas)，灰色背景

## 功能测试

测试图片转换：
```bash
# 测试图片转 Markdown
python run_doc_conversion.py /path/to/your/image.png

# 测试图片转 Word
python run_doc_conversion.py /path/to/your/image.png -f docx
```

测试 PDF 转换：
```bash
# 测试 PDF 转换（多页 PDF 会花费更长时间）
python run_doc_conversion.py /path/to/your/document.pdf -f docx
```

## 架构设计

```
run_doc_conversion.py          # 主程序入口
├── utils/
│   ├── deepseek_parser.py     # DeepSeek-OCR 输出解析器
│   ├── markdown_formatter.py  # Markdown 格式化器
│   ├── word_formatter.py      # Word 文档格式化器
│   ├── pdf_processor.py       # PDF 处理工具
│   ├── image_processor.py     # 图片处理工具
│   └── structs.py             # 块类型定义
└── config.py                   # 配置文件
```

### 处理流程

```
输入 (图片/PDF)
    ↓
[PDF] → 转换为图片 (PyMuPDF, 200 DPI)
    ↓
[OCR] → DeepSeek-OCR 处理
    ↓
[解析] → 提取带有边界框的内容块
    ↓
[格式化] → 生成 Markdown 或 Word
    ↓
输出文档 + 图片
```

## 性能指标

- **模型加载**: 约 6-8 秒
- **图片处理**: 每张图片约 10-15 秒
- **GPU 显存**: 约 6-7 GB（模型 + KV 缓存）
- **PDF 处理**: 每页约 10-15 秒

## 常见问题

### 问题：CUDA 显存不足
**解决方案**:
- 降低配置中的 `gpu_memory_utilization`
- 使用更小的图片（处理前调整大小）
- 减少同时处理的 PDF 页数

### 问题：找不到 'fitz' 模块
**解决方案**:
```bash
conda activate vllm-0.11
pip install PyMuPDF
```

### 问题：找不到 'docx' 模块
**解决方案**:
```bash
conda activate vllm-0.11
pip install python-docx
```

### 问题：图片未被提取
**可能原因**:
- 未向格式化器提供源图片
- 边界框坐标无效
- 图片区域太小

**检查方法**: 验证 `images/` 目录中是否包含提取的图片

## 开发说明

本实现的特点：
- 使用 DeepSeek-OCR 进行高质量 OCR 识别
- 实现了针对 DeepSeek-OCR 输出格式的自定义解析器，支持定位标签
- 提供独立的 BlockType 定义
- 支持流式输出和结构化文档生成
- 除标准 Python 包外无额外外部依赖

## 未来改进

- [ ] 支持批量处理多个文件
- [ ] 并行处理 PDF 页面
- [ ] 增强表格检测和格式化
- [ ] 改进 Word 中的公式渲染
- [ ] Word 输出的自定义样式选项
- [ ] 多页 PDF 处理的进度条
- [ ] 支持更多图片格式 (WebP, HEIC)

## 技术细节

### DeepSeek-OCR 输出格式

DeepSeek-OCR 的原始输出包含定位标签：
```
<|ref|>title<|/ref|><|det|>[[x1, y1, x2, y2]]<|/det|>
标题文本

<|ref|>text<|/ref|><|det|>[[x1, y1, x2, y2]]<|/det|>
正文内容

<|ref|>image<|/ref|><|det|>[[x1, y1, x2, y2]]<|/det|>
```

### 解析流程

1. **提取标签**: 使用正则表达式匹配 `<|ref|>` 和 `<|det|>` 标签
2. **分类处理**:
   - 图片标签 (`image`) → 提取并保存图片
   - 其他标签 → 移除定位信息，保留内容
3. **内容分块**: 将清理后的文本分割为内容块
4. **类型推断**: 根据格式特征判断块类型（标题、表格、代码等）

### Word 文档样式

Word 文档使用专业排版样式：
- 符合中文文档规范
- A4 标准页面
- 适合打印和阅读的字体和间距
- 自动页码
- 专业的表格样式

## 许可证

本代码是 DeepSeek-OCR 项目的一部分，遵循相同的许可条款。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

如有问题或建议，请在 GitHub 上提交 Issue。
