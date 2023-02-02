import enum
import json
import re
from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, Field
from tqdm import tqdm

from config import TLCPaths


class IntGenerator:
    def __init__(self):
        self.i = 0

    def __call__(self, *args, **kwargs):
        self.i += 1
        return self.i


class TermType(enum.StrEnum):
    LAY = "LAY"
    TECH = "TECH"


class SubForumType(enum.StrEnum):
    KIDNEY = "KIDNEY"
    STOMACH = "STOMACH-INTESTINES"


class Annotation(BaseModel):
    tech_term: Optional[str]
    lay_term: Optional[str]
    type: TermType
    span_start: int
    span_end: int
    id: int = Field(default_factory=IntGenerator())


class Sample(BaseModel):
    annotations: List[Annotation]
    text: str
    file_name: str
    subforum: SubForumType
    id: int = Field(default_factory=IntGenerator())


def process_sample_file(file: Path):
    try:
        with open(file) as fp:
            content = fp.read()
    except UnicodeDecodeError:
        with open(file, encoding="latin-1") as fp:
            content = fp.read()

    pattern = re.compile(r"Text: \[[^$]*")
    res = pattern.search(content)
    if not res:
        print(content)
        print(file)
    text = res.group().lstrip("Text: [").rstrip("]\n")
    return text


def process_annotation_file(file: Path):
    with open(file) as fp:
        content = fp.read()
    if not content:
        return []
    line_contents = [line.split("\t") for line in content.split("\n")]
    annotations = []
    for i in range(len(line_contents)):
        line_content = line_contents[i]
        # print(line_content)
        if not line_content[0]:  # skip empty lines
            continue
        if line_content[1].startswith("Laienbegriff"):
            source_type = TermType.LAY
        elif line_content[1].startswith("Fachterm"):
            source_type = TermType.TECH
        else:
            continue
        spans = line_content[1].replace(";", "").split(" ")
        span_start, span_end = int(spans[1]), int(spans[-1])
        source_term = line_content[2]
        source_tag = line_content[0]
        target_term = None
        for j in range(i + 1, i + 5):  # increase to max dep. on exec time
            try:
                next_line_content = line_contents[j]
                if (source_tag not in next_line_content[1] or
                        "AnnotatorNotes" not in next_line_content[1]):
                    continue
                else:
                    target_term = next_line_content[2]
                    break
            except IndexError:
                continue
        lay_term = source_term if source_type == TermType.LAY else target_term
        tech_term = source_term if source_type == TermType.TECH else target_term
        annotations.append(Annotation(tech_term=tech_term, lay_term=lay_term, type=source_type,
                                      span_start=span_start, span_end=span_end))
    return annotations


def process_tlc_files():
    samples = []
    for sample_file in tqdm(TLCPaths.sample_files):
        annotation_file = next(
            file for file in TLCPaths.annotation_files if sample_file.stem == file.stem)
        text = process_sample_file(sample_file)
        annotations = process_annotation_file(annotation_file)
        subforum = SubForumType.KIDNEY if "Kidney" == str(
            sample_file.parent.stem) else SubForumType.STOMACH
        samples.append(Sample(annotations=annotations, text=text, file_name=sample_file.stem,
                              subforum=subforum))
    return samples


def create_tlc_json_files():
    samples = process_tlc_files()
    for sample in samples:
        with open(TLCPaths.json_dir.joinpath(sample.file_name + ".json"), "w") as fp:
            json.dump(sample.json(), fp=fp)


def load_tlc_samples():
    samples = []
    for file in TLCPaths.json_dir.iterdir():
        sample = Sample.parse_file(file)
        samples.append(sample)
    return samples
