# Contributing to Medical Concept Normalization

Thank you for your interest in contributing to this project! This is primarily a research artifact, but we welcome improvements and bug fixes.

## How to Contribute

### Reporting Issues

- Use the GitHub issue tracker to report bugs
- Include detailed information about the issue
- Provide steps to reproduce the problem
- Mention your Python version and operating system

### Submitting Changes

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/medical-lay.git
   cd medical-lay
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed
   - Add docstrings to new functions

4. **Run tests and linting**
   ```bash
   poetry run pytest
   poetry run black src/
   poetry run ruff check src/
   poetry run mypy src/
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```
   
   We follow [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `test:` for test additions/changes
   - `refactor:` for code refactoring
   - `chore:` for maintenance tasks

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide a clear description of the changes
   - Reference any related issues
   - Ensure all CI checks pass

## Development Setup

```bash
# Install development dependencies
poetry install

# Install pre-commit hooks (optional)
pre-commit install
```

## Code Style

- **Formatting**: We use [Black](https://black.readthedocs.io/) for code formatting
- **Linting**: We use [Ruff](https://docs.astral.sh/ruff/) for linting
- **Type Hints**: Add type hints to function signatures
- **Docstrings**: Use Google-style docstrings for all public functions

## Testing

- Write unit tests for new functionality
- Aim for good test coverage
- Place tests in the `tests/` directory
- Use pytest fixtures when appropriate

## Questions?

Feel free to open an issue for any questions or clarifications!
