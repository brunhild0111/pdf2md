# PDF to Markdown

A small CLI wrapper script for converting a single PDF into Markdown using the Marker pipeline.

This folder is intended to be a clean “open-source ready” entry point for running the conversion.

This code has been modified based on the Marker code (https://github.com/datalab-to/marker) and is only for personal use. If you want to further optimize or modify the content, please refer to the original code link.

## What it does

- Loads Marker models (layout, OCR, etc.) via `marker.models.create_model_dict`
- Runs the configured Marker converter on one PDF
- Saves Markdown (and related artifacts, depending on Marker settings) into Marker’s output directory

## Prerequisites

- Python 3.10 (recommended)
- If you want GPU acceleration:
  - An NVIDIA GPU
  - A recent NVIDIA driver
  - A CUDA-enabled PyTorch build

## Installation

This script depends on the Marker codebase/package being importable as `marker`.

### Option A: Run inside the Marker repository (recommended)

1. Clone/open the Marker repository (the one that contains the `marker/` directory).
2. Create and activate a Python environment (conda example):

```bash
conda create -n pdf2md python=3.10 -y
conda activate pdf2md
```

3. Install Python dependencies.

CPU-only example:

```bash
python -m pip install -r pip_requirements.txt
```

CUDA example (PyTorch wheels):

```bash
python -m pip install --upgrade pip
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
python -m pip install -r pip_requirements.txt
python -m pip install surya-ocr scikit-learn pandas
```

Notes:
- `surya-ocr` declares a PyTorch version constraint; if pip reports a version conflict but the runtime works, prefer a PyTorch version that satisfies `surya-ocr` while still matching your CUDA runtime.
- If your machine is CPU-only, use `--device cpu`.

## Usage

From the Marker repository root:

```bash
python open_source/single_pdf_to_markdown/single_pdf_to_markdown.py --pdf examples/TCHES2025_3_14.pdf --device cuda
```

Common examples:

```bash
python open_source/single_pdf_to_markdown/single_pdf_to_markdown.py --pdf examples/2024CMFD.pdf --device cuda --page_range 0-1
python open_source/single_pdf_to_markdown/single_pdf_to_markdown.py --pdf examples/2024CMFD.pdf --device cpu --dtype float32
```

Arguments:

- `--pdf`: input PDF path (default is `examples/AESPT.pdf`)
- `--output_dir`: override output directory (otherwise uses Marker settings)
- `--page_range`: page selection, e.g. `0,5-10,20`
- `--force_ocr`: force OCR for all pages
- `--paginate_output`: insert page separators
- `--use_llm`: enable LLM-enhanced processors if configured
- `--device`: `auto | cpu | cuda`
- `--dtype`: `auto | float32 | float16 | bfloat16`
- `--attention`: `auto | sdpa`

## Environment / Dependencies (tested)

This script was tested on Windows with:

- Python: 3.10
- GPU: NVIDIA GeForce RTX 4070 Ti SUPER
- Driver CUDA: 12.6 (from `nvidia-smi`)
- PyTorch (CUDA): `torch==2.6.0+cu124`, `torchvision==0.21.0+cu124`, `torchaudio==2.6.0+cu124`
- OCR: `surya-ocr==0.17.0`

Full `pip freeze` (tested environment):

```text
aiofiles==0.6.0
annotated-types==0.7.0
anyio==4.11.0
attrs==25.4.0
beautifulsoup4==4.14.2
Bottleneck==1.4.2
cachetools==6.2.1
certifi==2025.10.5
cfgv==3.4.0
chardet==3.0.4
charset-normalizer==3.4.4
click==8.3.0
cmd2==1.5.0
colorama==0.4.6
coloredlogs==15.0.1
commonmark==0.9.1
distlib==0.4.0
einops==0.8.1
exceptiongroup==1.3.0
filelock==3.20.0
filetype==1.2.0
flatbuffers==25.9.23
fsspec==2025.10.0
ftfy==6.3.1
google-auth==2.43.0
google-genai==1.49.0
h11==0.16.0
h5py==3.14.0
httpcore==1.0.9
httpx==0.28.1
huggingface-hub==0.36.0
humanfriendly==10.0
identify==2.6.15
idna==2.10
Jinja2==3.0.0
joblib==1.5.2
markdown2==2.5.4
markdownify==1.2.0
MarkupSafe==3.0.3
mpmath==1.3.0
networkx==3.4.2
nodeenv==1.9.1
numpy==2.2.6
opencv-python-headless==4.11.0.86
packaging==25.0
pandas==2.2.3
pdftext==0.6.3
pillow==10.4.0
platformdirs==4.5.0
pre_commit==4.3.0
propcache==0.4.1
protobuf==6.33.0
pyasn1==0.6.1
pyasn1_modules==0.4.2
pydantic==2.12.4
pydantic-settings==2.11.0
pydantic_core==2.41.5
Pygments==2.19.2
pypdfium2==4.30.0
pyperclip==1.11.0
pyreadline3==3.5.4
python-dateutil==2.9.0.post0
python-dotenv==1.2.1
pytz==2025.2
PyYAML==6.0.3
RapidFuzz==3.14.3
regex==2025.11.3
requests==2.32.5
rich==10.2.0
rsa==4.9.1
ruamel.yaml==0.17.17
ruamel.yaml.clib==0.2.14
safetensors==0.6.2
scikit-learn==1.7.2
scipy==1.15.3
six==1.17.0
sniffio==1.3.1
soupsieve==2.8
surya-ocr==0.17.0
sympy==1.13.1
tenacity==9.1.2
threadpoolctl==3.6.0
tokenizers==0.22.1
torch==2.6.0+cu124
torchaudio==2.6.0+cu124
torchvision==0.21.0+cu124
tqdm==4.67.1
transformers==4.56.1
typing-inspection==0.4.2
typing_extensions==4.15.0
tzdata==2025.2
urllib3==1.26.20
virtualenv==20.35.4
wcwidth==0.2.14
websockets==15.0.1
```

