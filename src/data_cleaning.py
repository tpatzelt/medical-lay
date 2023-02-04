from typing import List

from tqdm import tqdm

from cistem import stem
from data_loading import TECH_TERM_TRIGGERS, TO_STRIP
from models import Annotation, Sample, TermType, SearchTerm, SearchTerms


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


def create_search_terms_from_samples(samples: List[Sample]):
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
    return SearchTerms(terms=search_terms)


def link_synonyms(search_terms: SearchTerms):
    search_terms = search_terms.terms
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
