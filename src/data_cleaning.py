"""Data cleaning utilities for medical text annotations.

This module provides functions to clean and normalize medical terminology
annotations from the TLC-UMLS dataset, including technical terms, lay terms,
and their synonyms.
"""

from typing import List

from tqdm import tqdm

from models import Annotation, Sample, TermType, SearchTerm, SearchTerms
from preprocessing.cistem import stem

TO_STRIP = " .,-"
TECH_TERM_TRIGGERS = ["(lat.)", "(gr.)", "(von lat.)", "(von gr.)", "( von gr.)", "( von lat.)",
                      "(von gr. und lat.)", "(von lat. und gr.)"]


def clean_tech_annotation(annotation: Annotation):
    """Clean technical medical term annotations.
    
    Removes language indicators and standardizes formatting of technical terms.
    Raises ValueError if annotation contains unexpected technical term triggers.
    
    Args:
        annotation: The annotation object to clean.
        
    Returns:
        The cleaned annotation with normalized technical term.
        
    Raises:
        ValueError: If annotation contains unexpected technical term triggers.
    """
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
    """Clean lay medical term annotations.
    
    Removes unnecessary characters and standardizes formatting of lay terms.
    
    Args:
        annotation: The annotation object to clean.
        
    Returns:
        The cleaned annotation with normalized lay term.
        
    Raises:
        ValueError: If annotation contains unexpected technical term triggers.
    """
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
    """Clean and normalize synonym annotations.
    
    Parses synonym fields, splits combined synonyms, and normalizes formatting.
    Handles various synonym markers like 'Syn.:', 'Synonym:', etc.
    
    Args:
        annotation: The annotation object with synonyms to clean.
        
    Returns:
        The cleaned annotation with normalized synonyms list.
    """
    if not annotation.synonyms:
        return annotation
    synonym_triggers = ["Syn.:", "Synonym:", "Syn,:", "syn. "]
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
    splitters = [" und", "(", " oder", " - "]
    lstrips = ["Laien:", "Laienbegriff:"]

    new_synonyms = []
    for text in annotation.synonyms:
        text = text.strip(TO_STRIP)
        to_remove = TECH_TERM_TRIGGERS + []
        for item in to_remove:
            text = text.replace(item, "")
            text = text.strip(TO_STRIP)
        new_synonyms.append(text)
        for splitter in splitters:
            text = text.split(splitter)[0]
        for lstrip in lstrips:
            text = text.removeprefix(lstrip)
        new_synonyms.append(text.strip())
    annotation.synonyms = new_synonyms
    return annotation


def clean_annotation(annotation: Annotation):
    """Clean all components of an annotation.
    
    Applies cleaning to lay terms, technical terms, and synonyms in sequence.
    Order matters as synonyms may reference cleaned lay/tech terms.
    
    Args:
        annotation: The annotation object to fully clean.
        
    Returns:
        The fully cleaned annotation.
    """
    annotation = clean_lay_annotation(annotation)
    annotation = clean_tech_annotation(annotation)
    # order matters because synonyms could still be added from lay or tech terms
    annotation = clean_synonyms_annotation(annotation)
    return annotation


def create_search_terms_from_samples(samples: List[Sample], intersect_terms=True):
    """Create search terms with stems from annotated samples.
    
    Generates searchable terms by stemming medical terms and their synonyms
    using the CISTEM stemmer. Optionally links synonyms with overlapping stems.
    
    Args:
        samples: List of Sample objects containing annotations.
        intersect_terms: If True, link terms with overlapping stems.
        
    Returns:
        SearchTerms object containing all processed search terms.
    """
    search_terms = []
    annotations = [ann for sample in samples for ann in sample.annotations]
    for annotation in annotations:
        annotation_term = annotation.lay_term if annotation.type == TermType.LAY else annotation.tech_term
        synonym_terms = [annotation_term] + annotation.synonyms
        stems = []
        for term in synonym_terms:
            stems.extend([" ".join([stem(word) for word in term.split(" ")])])
        search_term = SearchTerm(annotation=annotation, stems=set(stems))
        search_terms.append(search_term)
    if intersect_terms:
        link_synonyms(search_terms)
    return SearchTerms(terms=search_terms)


def link_synonyms(search_terms: List[SearchTerm]):
    """Link search terms with overlapping stems.
    
    Iteratively finds and merges search terms that share common stems,
    creating connected synonym groups. Continues until no new links are found.
    
    Args:
        search_terms: List of SearchTerm objects to link.
        
    Note:
        Modifies search_terms in place by updating their stems sets.
    """
    while True:
        with tqdm(total=len(search_terms) ** 2) as pbar:
            found_new_link = False
            for term1 in search_terms:
                for term2 in search_terms:
                    if term1.stems.intersection(term2.stems) and term1.stems != term2.stems:
                        found_new_link = True
                        union = term1.stems.union(term2.stems)
                        term1.stems = union
                        term2.stems = union

                    pbar.update(1)
            if not found_new_link:
                break
