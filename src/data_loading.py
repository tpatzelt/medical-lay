import enum
import re
from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, Field
from tqdm import tqdm

from config import TLCPaths

TO_STRIP = " .,-"
TECH_TERM_TRIGGERS = ["(lat.)", "(gr.)", "(von lat.)", "(von gr.)", ]


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
    synonyms: List[str] = []
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
        source_term = line_content[2].strip()
        source_tag = line_content[0]
        synonyms = []
        for j in range(i + 1, i + 10):  # increase to max dep. on exec time
            try:
                next_line_content = line_contents[j]
                if (source_tag not in next_line_content[1] or
                        "AnnotatorNotes" not in next_line_content[1]):
                    continue
                else:
                    synonyms.append(next_line_content[2])
            except IndexError:
                continue
        if source_type == TermType.LAY:
            annotation = Annotation(lay_term=source_term, type=source_type, span_start=span_start,
                                    span_end=span_end, synonyms=synonyms)
        elif source_type == TermType.TECH:
            annotation = Annotation(tech_term=source_term, type=source_type,
                                    span_start=span_start, span_end=span_end, synonyms=synonyms)
        else:
            raise ValueError(f"Source type {source_type} not known.")
        annotations.append(annotation)
    return annotations


def clean_tech_annotation(annotation: Annotation):
    if not annotation.tech_term:
        return annotation
    text = annotation.tech_term
    if any([trigger in text for trigger in TECH_TERM_TRIGGERS]):
        raise ValueError
    text = text.strip(TO_STRIP)
    to_remove = TECH_TERM_TRIGGERS + []
    for item in to_remove:
        text = text.replace(item, "")
        text = text.strip(TO_STRIP)
    annotation.tech_term = text
    return annotation


def clean_lay_annotation(annotation: Annotation):
    if not annotation.lay_term:
        return annotation
    text = annotation.lay_term
    if any([trigger in text for trigger in TECH_TERM_TRIGGERS]):
        raise ValueError
    text = text.strip(TO_STRIP)
    to_remove = []
    for item in to_remove:
        text = text.replace(item, "")
        text = text.strip(TO_STRIP)
    annotation.lay_term = text
    return annotation


def clean_synonyms_annotation(annotation: Annotation):
    if not annotation.synonyms:
        return annotation
    synonym_triggers = ["Syn.:", "Synonym:", "Syn,:"]
    new_synonyms = []
    for text in annotation.synonyms:
        try:
            trigger = next(syn for syn in synonym_triggers if syn in text)
        except StopIteration:
            new_synonyms.append(text)
            continue
        split_synonym = text.split(trigger)
        if not split_synonym[0]:
            new_synonyms.append(split_synonym[1])
            continue
        if len(split_synonym) > 2:
            raise RuntimeWarning("Found more than two synonyms in one annotation")
        new_synonyms.extend(split_synonym)
    annotation.synonyms = new_synonyms

    # clean synonyms
    new_synonyms = []
    for text in annotation.synonyms:
        text = text.strip(TO_STRIP)
        to_remove = TECH_TERM_TRIGGERS + []
        for item in to_remove:
            text = text.replace(item, "")
            text = text.strip(TO_STRIP)
        new_synonyms.append(text)
    annotation.synonyms = new_synonyms
    return annotation


def clean_annotation(annotation: Annotation):
    annotation = clean_lay_annotation(annotation)
    annotation = clean_tech_annotation(annotation)
    # order matters because synonyms could still be added from lay or tech terms
    annotation = clean_synonyms_annotation(annotation)
    return annotation


def process_tlc_files():
    samples = []
    for sample_file in tqdm(TLCPaths.sample_files):
        annotation_file = next(
            file for file in TLCPaths.annotation_files if sample_file.stem == file.stem)
        text = process_sample_file(sample_file)
        annotations = process_annotation_file(annotation_file)
        annotations = [clean_annotation(annotation) for annotation in annotations]
        subforum = SubForumType.KIDNEY if "Kidney" == str(
            sample_file.parent.stem) else SubForumType.STOMACH
        samples.append(Sample(annotations=annotations, text=text, file_name=sample_file.stem,
                              subforum=subforum))
    return samples


def create_tlc_json_files():
    samples = process_tlc_files()
    for sample in samples:
        with open(TLCPaths.json_dir.joinpath(sample.file_name + ".json"), "w") as fp:
            fp.write(sample.json())
    return samples


def load_tlc_samples():
    samples = []
    for file in TLCPaths.json_dir.iterdir():
        sample = Sample.parse_file(file)
        samples.append(sample)
    return samples
