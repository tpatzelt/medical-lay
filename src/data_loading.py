"""Data loading utilities for TLC-UMLS dataset and WUMLS (German UMLS).

This module provides functions to load, process, and cache medical text
samples and annotations from the TLC-UMLS dataset, as well as UMLS
concept entries from WUMLS.
"""

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
    """Read and process a sample text file.
    
    Handles different encodings (UTF-8 and Latin-1) to ensure
    successful file reading.
    
    Args:
        file: Path to the sample text file.
        
    Returns:
        The file content as a string.
    """
    try:
        with open(file) as fp:
            content = fp.read()
    except UnicodeDecodeError:
        with open(file, encoding="latin-1") as fp:
            content = fp.read()
    return content


def process_annotation_file(file: Path):
    """Parse annotation file and extract medical term annotations.
    
    Processes BRAT-style annotation files to extract lay terms (Laienbegriff)
    and technical terms (Fachterm) along with their spans and synonyms.
    
    Args:
        file: Path to the .ann annotation file.
        
    Returns:
        List of Annotation objects parsed from the file.
        
    Raises:
        ValueError: If source type is not LAY or TECH.
    """
    with open(file) as fp:
        content = fp.read()
    if not content:
        return []
    line_contents = [line.split("\t") for line in content.split("\n")]
    annotations = []
    for i in range(len(line_contents)):
        line_content = line_contents[i]
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
    """Process all TLC-UMLS sample and annotation files.
    
    Loads and pairs sample text files with their corresponding annotation files,
    creating Sample objects with cleaned annotations.
    
    Returns:
        List of Sample objects containing text and annotations.
    """
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
    """Process TLC files and save samples as JSON.
    
    Converts TLC-UMLS samples to JSON format and saves them to the
    configured JSON directory.
    
    Returns:
        List of processed Sample objects.
    """
    samples = process_tlc_files()
    for sample in samples:
        with open(TLCPaths.json_dir.joinpath(sample.file_name + ".json"), "w") as fp:
            fp.write(sample.json(ensure_ascii=False))
    return samples


def load_tlc_samples():
    """Load TLC-UMLS samples from JSON files.
    
    Reads previously processed samples from the JSON directory.
    
    Returns:
        List of Sample objects loaded from JSON.
    """
    samples = []
    for file in TLCPaths.json_dir.iterdir():
        sample = Sample.parse_file(file)
        samples.append(sample)
    return samples


def create_search_terms_json_file():
    """Create and save search terms JSON file.
    
    Generates stemmed search terms from TLC samples and saves them
    to the configured search terms file.
    
    Returns:
        SearchTerms object containing all search terms.
    """
    samples = load_tlc_samples()
    search_terms = create_search_terms_from_samples(samples)
    with open(TLCPaths.search_term_file, "w") as fp:
        fp.write(search_terms.json(ensure_ascii=False))
    return search_terms


def load_search_terms():
    """Load search terms from JSON file.
    
    Returns:
        SearchTerms object parsed from the search terms file.
    """
    return SearchTerms.parse_file(TLCPaths.search_term_file)


def load_jsonl_file_as_generator(path):
    """Load a JSONL file as a generator of JSON objects.
    
    Memory-efficient loading for large JSONL files.
    
    Args:
        path: Path to the JSONL file.
        
    Yields:
        Parsed JSON objects, one per line.
    """
    with open(path) as fp:
        for line in fp:
            yield json.loads(line)


annotations_cache = dc.Cache("caches/annotations_ids")

annotations = [ann for sample in load_tlc_samples() for ann in sample.annotations]

@annotations_cache.memoize()
def get_annotation_ids(mention: str):
    """Get all annotation IDs for a given mention.
    
    Cached function that searches through all annotations to find
    matching mentions.
    
    Args:
        mention: The medical term mention to search for.
        
    Returns:
        List of annotation IDs that match the mention.
    """
    res = []
    for ann in annotations:
        if ann.get_mention() == mention:
            res.append(ann.id)
    return res


def load_wumls_entries(wumls_file=None):
    """Load WUMLS (German UMLS) entries from RRF file.
    
    Parses the MRCONSO RRF file format to extract UMLS concepts
    for German language.
    
    Args:
        wumls_file: Path to the WUMLS RRF file. If None, uses default
                    from environment or standard data location.
        
    Returns:
        List of WUMLSEntry objects containing CUI, language, name, and source.
    """
    import os
    from pathlib import Path
    
    if wumls_file is None:
        wumls_file = os.getenv('WUMLS_DATASET_PATH', 
                               Path(__file__).parent.parent / 'data' / 'WUMLS' / 'MRCONSO_WUMLS_GER.RRF')
    
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