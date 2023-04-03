import csv
import json
from pathlib import Path

import diskcache as dc
from tqdm import tqdm

from config import TLCPaths
from data_cleaning import clean_annotation, create_search_terms_from_samples
from models import TermType, SubForumType, Annotation, Sample, SearchTerms
from models import WUMLSEntry


def process_sample_file(file: Path):
    try:
        with open(file) as fp:
            content = fp.read()
    except UnicodeDecodeError:
        with open(file, encoding="latin-1") as fp:
            content = fp.read()
    return content

    # pattern = re.compile(r"Text: \[[^$]*")
    # res = pattern.search(content)
    # if not res:
    #     print(content)
    #     print(file)
    # text = res.group().lstrip("Text: [").rstrip("]\n")
    # return text


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


def create_search_terms_json_file():
    samples = load_tlc_samples()
    search_terms = create_search_terms_from_samples(samples)
    with open(TLCPaths.search_term_file, "w") as fp:
        fp.write(search_terms.json())
    return search_terms


def load_search_terms():
    return SearchTerms.parse_file(TLCPaths.search_term_file)


def load_jsonl_file_as_generator(path):
    """Load a jsonl file as a generator of json objects."""
    with open(path) as fp:
        for line in fp:
            yield json.loads(line)


annotations_cache = dc.Cache("caches/annotations_ids")


@annotations_cache.memoize()
def get_annotation_ids(mention: str):
    """Get all annotations ids for a mention."""
    annotations = [ann for sample in load_tlc_samples() for ann in sample.annotations]
    res = []
    for ann in annotations:
        if ann.get_mention() == mention:
            res.append(ann.id)
    return res


def load_wumls_entries(wumls_file='/home/tim/MedicalLay/WUMLS/MRCONSO_WUMLS_GER.RRF'):
    entries = []
    with open(wumls_file, newline='\n') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='|')
        for row in spamreader:
            cui = row[0]
            language = row[1]
            source = row[11]
            name = row[14]
            entry = WUMLSEntry(cui=cui, language=language, name=name, source=source)
            entries.append(entry)
    return entries