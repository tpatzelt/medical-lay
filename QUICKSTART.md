# Quick Start Guide

Welcome! This guide will help you get started with the medical concept normalization repository quickly.

## Prerequisites

- Python 3.11 or higher
- Poetry (Python dependency manager)
- UMLS API key (optional, for UMLS queries)
- Git

## Installation

### Option 1: Automated Setup (Recommended)

```bash
git clone https://github.com/tpatzelt/medical-lay.git
cd medical-lay
./setup.sh
```

### Option 2: Manual Setup

```bash
# Clone the repository
git clone https://github.com/tpatzelt/medical-lay.git
cd medical-lay

# Install dependencies
poetry install

# Copy environment template
cp .env.example .env

# Edit .env and add your credentials
nano .env  # or use your preferred editor
```

## Quick Commands

```bash
# Activate virtual environment
poetry shell

# Run tests
pytest tests/

# Run all checks (formatting, linting, tests)
make check-all

# Start Jupyter notebooks
jupyter notebook

# Format code
make format

# Run linting
make lint
```

## Project Structure

```
medical-lay/
├── src/                    # Core library code
│   ├── config.py          # Configuration
│   ├── data_loading.py    # Data loading utilities
│   ├── data_cleaning.py   # Data preprocessing
│   ├── models.py          # Pydantic models
│   └── ...
├── notebooks/             # Jupyter notebooks
│   ├── experiments/       # Main experiments
│   ├── analysis/          # Analysis notebooks
│   └── ...
├── tests/                 # Unit tests
├── data/                  # Data directory (gitignored)
└── ...
```

## Core Workflows

### 1. Load and Process TLC Data

```python
from src.data_loading import process_tlc_files, load_tlc_samples

# Process raw TLC files (requires dataset)
samples = process_tlc_files()

# Load preprocessed samples
samples = load_tlc_samples()
```

### 2. Query UMLS API

```bash
# Set your API key in .env first
export UMLS_API_KEY="your_key_here"

# Run UMLS query script
python src/parse_umls/umls_api/get_cui_for_strings.py \
  -i input.txt \
  -o output.txt
```

### 3. Run Main Experiments

Open Jupyter notebooks:
```bash
jupyter notebook
```

Navigate to:
- `notebooks/sapbert_xlmr_tlc_create_embeddings.ipynb` - Create embeddings
- `notebooks/sapbert_xlmr_tlc_ger_similarity_search.ipynb` - Run similarity search
- `notebooks/train_cross_encoder_xmen.ipynb` - Train cross-encoder

## Dataset Setup

⚠️ **Important**: This repository requires specific datasets that are not included.

See [DATASET_ACCESS.md](DATASET_ACCESS.md) for:
- How to obtain the TLC-UMLS dataset
- How to get WUMLS (German UMLS)
- Dataset structure requirements
- Access request procedures

You can explore the code without datasets, but cannot run experiments.

## Configuration

Edit `.env` file to configure:

```bash
# API Keys
UMLS_API_KEY=your_umls_api_key_here
DEEPL_API_KEY=your_deepl_api_key_here

# Dataset Paths
TLC_DATASET_PATH=./data/TLC_v01
WUMLS_DATASET_PATH=./data/WUMLS
```

## Common Issues

### "No module named 'src'"
```bash
# Make sure you're in the project directory and virtual environment is activated
poetry shell
```

### "Dataset not found"
- Check your `.env` file paths
- Ensure datasets are in the correct directories
- See [DATASET_ACCESS.md](DATASET_ACCESS.md) for dataset requirements

### Import errors in notebooks
```bash
# Restart the Jupyter kernel after installing dependencies
# In Jupyter: Kernel → Restart
```

## Development

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_data_cleaning.py
```

### Code Quality

```bash
# Format code
black src/ tests/

# Check linting
ruff check src/

# Type checking
mypy src/ --ignore-missing-imports

# Run all checks
make check-all
```

### Pre-commit Hooks

```bash
# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## Next Steps

1. ✅ Complete installation
2. ✅ Configure `.env` file
3. ✅ Review [DATASET_ACCESS.md](DATASET_ACCESS.md)
4. ✅ Explore notebooks in `notebooks/`
5. ✅ Read the [paper](https://arxiv.org/abs/2409.14579)
6. ✅ Check [CONTRIBUTING.md](CONTRIBUTING.md) to contribute

## Getting Help

- 📖 Read the full [README.md](README.md)
- 🐛 Report issues on GitHub
- 📧 Contact authors through the paper
- 💬 Check existing issues for solutions

## Useful Resources

- **UMLS**: https://www.nlm.nih.gov/research/umls/
- **SapBERT**: https://github.com/cambridgeltl/sapbert
- **Paper**: https://arxiv.org/abs/2409.14579
- **Poetry Docs**: https://python-poetry.org/docs/

---

Happy coding! 🚀
