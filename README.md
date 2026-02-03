# Medical Concept Normalization in a Low-Resource Setting

[![arXiv](https://img.shields.io/badge/arXiv-2409.14579-b31b1b.svg)](https://arxiv.org/abs/2409.14579)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

Research code for medical concept normalization in low-resource settings, specifically for normalizing German medical forum posts to UMLS concepts using multilingual Transformer models (SapBERT).

## Abstract

In the field of biomedical natural language processing, medical concept normalization is a crucial task for accurately mapping mentions of concepts to a large knowledge base. However, this task becomes even more challenging in low-resource settings, where limited data and resources are available. This research explores the challenges of medical concept normalization in a low-resource setting, specifically investigating the shortcomings of current methods applied to German lay texts.

A dataset consisting of posts from a German medical online forum is annotated with concepts from the Unified Medical Language System (UMLS). The experiments demonstrate that multilingual Transformer-based models are able to outperform string similarity methods. The use of contextual information to improve the normalization of lay mentions is also examined. Based on the results of the best performing model, a systematic error analysis is presented along with potential improvements to mitigate frequent errors.

📄 **Full Paper**: [arXiv:2409.14579](https://arxiv.org/abs/2409.14579)

![top64_ersults.png](data%2Fimages%2Ftop64_ersults.png)![error_counts.png](data%2Fimages%2Ferror_counts.png)

## 🚀 Quick Start

### Installation

#### Using Poetry (Recommended)

```bash
# Clone the repository
git clone https://github.com/tpatzelt/medical-lay.git
cd medical-lay

# Install dependencies with Poetry
poetry install

# Activate the virtual environment
poetry shell
```

#### Using pip

```bash
# Clone the repository
git clone https://github.com/tpatzelt/medical-lay.git
cd medical-lay

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API keys and dataset paths:
   ```bash
   UMLS_API_KEY=your_umls_api_key_here
   DEEPL_API_KEY=your_deepl_api_key_here
   TLC_DATASET_PATH=./data/TLC_v01
   ```

### Dataset Requirements

⚠️ **Important**: This repository is a research artifact. The datasets used in this research are not publicly available and require separate access:

- **TLC-UMLS Dataset**: Custom-annotated German medical forum posts. Contact the authors for access requests.
- **WUMLS**: German subset of UMLS (Unified Medical Language System). Requires [UMLS license](https://www.nlm.nih.gov/databases/umls.html).

The code is provided for transparency and reproducibility by researchers with appropriate dataset access.

## 📁 Repository Structure

```
medical-lay/
├── src/                          # Core library code
│   ├── config.py                 # Configuration and path management
│   ├── data_loading.py           # Dataset loading utilities
│   ├── data_cleaning.py          # Data preprocessing
│   ├── models.py                 # Pydantic data models
│   ├── parse_umls/               # UMLS parsing utilities
│   └── preprocessing/            # Text preprocessing (CISTEM stemmer)
├── notebooks/                    # Jupyter notebooks for experiments
│   ├── experiments/              # Main experiments
│   ├── analysis/                 # Results analysis
│   ├── annotation/               # Annotation preparation
│   └── plots/                    # Visualization
├── bash_scripts/                 # Utility scripts
├── data/                         # Data directory (gitignored)
├── pyproject.toml               # Poetry dependencies
├── requirements.txt             # Pip dependencies
└── README.md                    # This file
```

## 🔬 Main Experiments

### 1. SapBERT-based Concept Normalization

The main experiment uses multilingual SapBERT to embed mentions and UMLS concepts:

- **[sapbert_xlmr_tlc_create_embeddings.ipynb](notebooks/sapbert_xlmr_tlc_create_embeddings.ipynb)**: Create embeddings for TLC-UMLS mentions and UMLS concepts using the `cambridgeltl/SapBERT-UMLS-2020AB-all-lang-from-XLMR-large` model
- **[sapbert_xlmr_tlc_ger_similarity_search.ipynb](notebooks/sapbert_xlmr_tlc_ger_similarity_search.ipynb)**: Find the closest concept for each mention using cosine similarity

### 2. Cross-Encoder Re-ranking

The experiment to train a Sentence Cross-Encoder to re-rank candidate concepts:

- **[train_cross_encoder_xmen.ipynb](notebooks/train_cross_encoder_xmen.ipynb)**: Train and evaluate cross-encoder models for candidate re-ranking

### 3. Analysis Notebooks

Additional analysis notebooks are available in [notebooks/analysis/](notebooks/analysis/):
- Error analysis and systematic evaluation
- TLC-UMLS corpus statistics
- Semantic type analysis
- Solr baseline comparison

## 🧪 Usage Examples

### Using the Core Library

```python
from src.data_loading import process_tlc_files, load_tlc_samples
from src.models import Sample, Annotation

# Load TLC samples (requires dataset access)
samples = process_tlc_files()

# Access annotations
for sample in samples:
    print(f"Sample: {sample.file_name}")
    for annotation in sample.annotations:
        print(f"  {annotation.type}: {annotation.lay_term or annotation.tech_term}")
```

### Querying UMLS API

```python
# Set UMLS_API_KEY environment variable first
import os
os.environ['UMLS_API_KEY'] = 'your_key_here'

# Run the UMLS query script
# python src/parse_umls/umls_api/get_cui_for_strings.py -i input.txt -o output.txt
```

## 🛠️ Development

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src --cov-report=html
```

### Code Quality

```bash
# Format code
poetry run black src/

# Type checking
poetry run mypy src/

# Linting
poetry run ruff check src/
```

## 📊 Results

The experiments show that multilingual Transformer-based models (SapBERT) significantly outperform traditional string similarity methods for German medical concept normalization. See the [paper](https://arxiv.org/abs/2409.14579) for detailed results and analysis.

## 📖 Citation

If you use this code or dataset in your research, please cite:

```bibtex
@article{patzelt2024medical,
  title={Medical Concept Normalization in a Low-Resource Setting},
  author={Patzelt, Tim},
  journal={arXiv preprint arXiv:2409.14579},
  year={2024}
}
```

Or use the `CITATION.cff` file in this repository.

## 🤝 Contributing

This is primarily a research artifact, but contributions are welcome! Please feel free to:
- Open issues for bugs or questions
- Submit pull requests for improvements
- Request features or enhancements

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **SapBERT**: [Cambridge Language Technology Lab](https://github.com/cambridgeltl/sapbert)
- **UMLS**: National Library of Medicine
- **Transformers**: Hugging Face

## 📧 Contact

For dataset access requests or questions about the research, please open an issue or contact the authors through the paper.

---

**Note**: This repository contains research code. While efforts have been made to ensure code quality and documentation, some components may require adaptation for production use.