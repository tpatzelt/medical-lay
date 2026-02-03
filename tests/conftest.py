"""Pytest configuration and fixtures."""

import pytest
from pathlib import Path


@pytest.fixture
def temp_data_dir(tmp_path):
    """Create a temporary data directory for testing."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return data_dir


@pytest.fixture
def sample_annotation_file(tmp_path):
    """Create a sample annotation file for testing."""
    ann_file = tmp_path / "test.ann"
    content = """T1\tLaienbegriff 0 10\tTestterm\nA1\tAnnotatorNotes T1 C0000000\n"""
    ann_file.write_text(content)
    return ann_file


@pytest.fixture
def sample_text_file(tmp_path):
    """Create a sample text file for testing."""
    txt_file = tmp_path / "test.txt"
    content = "This is a test medical text with Testterm in it."
    txt_file.write_text(content)
    return txt_file
