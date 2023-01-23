from pathlib import Path


class TLCPaths:
    tlc_dir = Path("/home/tim/MedicalLay/TLC_v01")
    kidney_dir = tlc_dir.joinpath("Kidney")
    stomach_dir = tlc_dir.joinpath("StomachIntestines")
    dataset_files = list(kidney_dir.iterdir()) + list(stomach_dir.iterdir())
    annotation_files = [file for file in dataset_files if file.suffix == ".ann"]
    sample_files = [file for file in dataset_files if file.suffix == ".txt"]
    json_dir = Path("/home/tim/PycharmProjects/medical-lay/data/tlc_json")
    if not json_dir.exists():
        json_dir.mkdir()
