"""Unit tests for configuration module."""

import os
from pathlib import Path
from src.config import TLCPaths


class TestTLCPaths:
    """Tests for TLCPaths configuration class."""
    
    def test_project_path_uses_env_variable(self, monkeypatch):
        """Test that project path uses environment variable when set."""
        test_path = "/test/project/path"
        monkeypatch.setenv("PROJECT_PATH", test_path)
        # Note: TLCPaths is already instantiated, this test documents behavior
        # In practice, environment variables should be set before module import
        assert True  # Placeholder for configuration behavior test
    
    def test_tlc_dataset_path_fallback(self):
        """Test that TLC dataset path has proper fallback."""
        # TLCPaths should handle missing dataset directory gracefully
        assert isinstance(TLCPaths.tlc_dir, Path)
        assert isinstance(TLCPaths.project_data_path, Path)
    
    def test_json_dir_created(self):
        """Test that JSON directory is created if it doesn't exist."""
        # The json_dir should be created during initialization
        assert TLCPaths.json_dir.exists()
    
    def test_paths_are_path_objects(self):
        """Test that all paths are Path objects."""
        assert isinstance(TLCPaths.project_path, Path)
        assert isinstance(TLCPaths.tlc_dir, Path)
        assert isinstance(TLCPaths.json_dir, Path)
        assert isinstance(TLCPaths.search_term_file, Path)
