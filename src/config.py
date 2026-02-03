import os
from pathlib import Path


class TLCPaths:
    # Use environment variable or default to relative path from project root
    project_path = Path(os.getenv("PROJECT_PATH", Path(__file__).parent.parent.resolve()))
    tlc_dir = Path(os.getenv("TLC_DATASET_PATH", project_path / "data" / "TLC_v01"))

    # Only initialize paths if dataset directory exists
    if tlc_dir.exists():
        kidney_dir = tlc_dir.joinpath("Kidney")
        stomach_dir = tlc_dir.joinpath("StomachIntestines")
        dataset_files = list(kidney_dir.iterdir()) + list(stomach_dir.iterdir()) if kidney_dir.exists() and stomach_dir.exists() else []
        annotation_files = [file for file in dataset_files if file.suffix == ".ann"]
        sample_files = [file for file in dataset_files if file.suffix == ".txt"]
    else:
        kidney_dir = tlc_dir / "Kidney"
        stomach_dir = tlc_dir / "StomachIntestines"
        dataset_files = []
        annotation_files = []
        sample_files = []

    project_data_path = project_path / "data"
    json_dir = project_data_path / "tlc_json"
    if not json_dir.exists():
        json_dir.mkdir(parents=True, exist_ok=True)
    search_term_file = project_data_path / "tlc_search_terms.json"
