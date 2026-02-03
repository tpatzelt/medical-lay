# Dataset Access Information

## Overview

This repository contains research code for medical concept normalization. The actual datasets used in the research are **not included** in this repository due to licensing and privacy considerations.

## Required Datasets

### 1. TLC-UMLS Dataset

**Description**: Custom-annotated German medical forum posts from kidney and stomach/intestines subforums.

**Format**: BRAT-style annotation files (.txt and .ann files)

**Required Structure**:
```
data/TLC_v01/
├── Kidney/
│   ├── sample001.txt
│   ├── sample001.ann
│   └── ...
└── StomachIntestines/
    ├── sample001.txt
    ├── sample001.ann
    └── ...
```

**Access**: This is a proprietary dataset created for this research. For access requests:
- Open an issue in this repository
- Contact the authors through the paper: https://arxiv.org/abs/2409.14579
- Include your intended use case and institutional affiliation

**Annotation Format**: Annotations follow the BRAT format with:
- `Laienbegriff` - Lay medical terms
- `Fachterm` - Technical medical terms
- `AnnotatorNotes` - UMLS CUI annotations and synonyms

### 2. WUMLS (German UMLS Subset)

**Description**: German subset of the Unified Medical Language System (UMLS).

**Format**: MRCONSO.RRF file in pipe-delimited format

**Required Structure**:
```
data/WUMLS/
└── MRCONSO_WUMLS_GER.RRF
```

**Access**: 
1. Register for a UMLS license at: https://uts.nlm.nih.gov/uts/umls/home
2. Download the UMLS Metathesaurus
3. Extract German language entries from MRCONSO.RRF
4. Place the extracted file in `data/WUMLS/`

**License**: Requires UMLS Metathesaurus License from the National Library of Medicine

### 3. UMLS API Access

**Description**: API access for querying UMLS concepts.

**Access**:
1. Create an account at: https://uts.nlm.nih.gov/uts/signup-login
2. Get your API key from your profile: https://uts.nlm.nih.gov/uts/profile
3. Add the API key to your `.env` file

## Working Without the Full Dataset

If you don't have access to the full datasets, you can still:

1. **Explore the Code**: All source code is available and documented
2. **Read the Notebooks**: Jupyter notebooks show the analysis workflow
3. **Understand the Methods**: Documentation explains the approach
4. **Adapt for Your Data**: Use the code structure as a template for your own datasets

## Sample Data (Future)

We are exploring options to provide:
- Anonymized/synthetic sample data for testing
- Public subset of annotations (pending ethical review)
- Example data format templates

Check back for updates or open an issue to express interest.

## Citation and Academic Use

If you use this code or datasets in your research, please cite:

```bibtex
@article{patzelt2024medical,
  title={Medical Concept Normalization in a Low-Resource Setting},
  author={Patzelt, Tim},
  journal={arXiv preprint arXiv:2409.14579},
  year={2024}
}
```

## Questions?

For dataset access questions:
- Open an issue in this repository
- Contact authors through the paper
- Check for updates in the CHANGELOG.md

## Legal and Ethical Considerations

- TLC-UMLS contains real medical forum posts - privacy and ethical review required
- WUMLS requires UMLS licensing agreement
- Ensure you have proper institutional approval before requesting access
- Data should only be used for research purposes as specified in licenses
