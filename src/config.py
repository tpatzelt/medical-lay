from pathlib import Path


class TLCPaths:
    tlc_dir = Path("/home/tim/MedicalLay/TLC_v01")
    kidney_dir = tlc_dir.joinpath("Kidney")
    stomach_dir = tlc_dir.joinpath("StomachIntestines")
    dataset_files = list(kidney_dir.iterdir()) + list(stomach_dir.iterdir())
    annotation_files = [file for file in dataset_files if file.suffix == ".ann"]
    sample_files = [file for file in dataset_files if file.suffix == ".txt"]
    project_path = Path("/home/tim/PycharmProjects/medical-lay/")
    project_data_path = project_path.joinpath("data")
    json_dir = project_data_path.joinpath("tlc_json")
    if not json_dir.exists():
        json_dir.mkdir()
    search_term_file = project_data_path.joinpath("tlc_search_terms.json")
