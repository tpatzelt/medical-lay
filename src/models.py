import enum
from typing import Optional, List, Set

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
    tech_term: Optional[str]
    lay_term: Optional[str]
    type: TermType
    span_start: int
    span_end: int
    synonyms: List[str] = []
    id: int = Field(default_factory=IntGenerator())

    def get_mention(self):
        return self.tech_term if self.type == TermType.TECH else self.lay_term


class Sample(BaseModel):
    annotations: List[Annotation]
    text: str
    file_name: str
    subforum: SubForumType
    id: int = Field(default_factory=IntGenerator())


class SearchTerm(BaseModel):
    annotation: Annotation
    stems: Set[str] = set()


class SearchTerms(BaseModel):
    terms: List[SearchTerm]
