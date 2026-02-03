import enum
from typing import Literal

from pydantic import BaseModel, Field


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
    tech_term: str | None
    lay_term: str | None
    type: TermType
    span_start: int
    span_end: int
    synonyms: list[str] = []
    id: int = Field(default_factory=IntGenerator())

    def get_mention(self):
        return self.tech_term if self.type == TermType.TECH else self.lay_term


class Sample(BaseModel):
    annotations: list[Annotation]
    text: str
    file_name: str
    subforum: SubForumType
    id: int = Field(default_factory=IntGenerator())


class SearchTerm(BaseModel):
    annotation: Annotation
    stems: set[str] = set()


class SearchTerms(BaseModel):
    terms: list[SearchTerm]


class Match(BaseModel):
    mention: SearchTerm
    match: dict | None = None
    matched_string: str | None = None
    # keep string because a search term can have multiple strings to match


class SampleCollection:
    def __init__(self, samples):
        self.samples = samples
        self.id_mapping = {sample.id: sample for sample in self.samples}
        self.annotation_id_mapping = {annotation.id: sample for sample in self.samples for
                                      annotation in sample.annotations}

    def get_sample_by_id(self, identifier: int):
        return self.id_mapping[identifier]

    def get_sample_by_annotation_id(self, identifier: int):
        return self.annotation_id_mapping[identifier]


class WUMLSEntry(BaseModel):
    # id: int = Field(default_factory=IntGenerator())
    cui: str
    source: str
    language: str
    name: str
    index_term: str | None = None  # is the stemmed name


class WUMLSMultiValuedEntry(BaseModel):
    cui: str
    source: str
    language: str
    names: list[str]
    index_terms: list[str] = []


class ProdigyNERLabel(BaseModel):
    start: int
    end: int
    label: Literal["Mention"] = "Mention"


class ProdigySample(BaseModel):
    text: str
    spans: list[ProdigyNERLabel]
    html: str
    annotation_ids: list[int]
    cui: str
    meta: dict = {}
