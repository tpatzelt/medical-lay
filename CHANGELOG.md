# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-03

### Added
- Initial public release of medical concept normalization research code
- Core library modules for data loading and cleaning
- Pydantic data models for medical annotations
- SapBERT-based concept normalization experiments
- Cross-encoder re-ranking experiments
- Comprehensive Jupyter notebooks for experiments and analysis
- UMLS API integration for concept queries
- German CISTEM stemmer for text preprocessing
- Unit tests for core functionality
- CI/CD pipeline with GitHub Actions
- MIT License
- Comprehensive README with setup instructions
- CITATION.cff for academic attribution
- Environment variable configuration for API keys and paths

### Changed
- Refactored hardcoded paths to use environment variables
- Improved code documentation with comprehensive docstrings
- Enhanced error handling and encoding support

### Security
- Removed hardcoded API keys (now use environment variables)
- Added .env.example template for secure configuration
- Updated .gitignore to exclude .idea/ and .env files

## [Unreleased]

### Planned
- Additional test coverage
- Documentation website
- Example datasets (synthetic/sample data)
- Command-line interface for common tasks
- Performance optimizations for large-scale processing

---

**Note**: This is a research artifact. Version 1.0.0 represents the state of the code as published with the research paper.
