"""Unit tests for data cleaning utilities."""

import pytest
from src.models import Annotation, TermType
from src.data_cleaning import (
    clean_tech_annotation,
    clean_lay_annotation,
    clean_synonyms_annotation,
    clean_annotation,
)


class TestCleanTechAnnotation:
    """Tests for cleaning technical term annotations."""
    
    def test_clean_basic_tech_term(self):
        """Test cleaning of a basic technical term."""
        annotation = Annotation(
            tech_term="  Diabetes mellitus  ",
            type=TermType.TECH,
            span_start=0,
            span_end=10
        )
        result = clean_tech_annotation(annotation)
        assert result.tech_term == "Diabetes mellitus"
    
    def test_clean_tech_term_with_latin_trigger_raises_error(self):
        """Test that technical terms with (lat.) trigger raise ValueError."""
        annotation = Annotation(
            tech_term="Diabetes mellitus (lat.)",
            type=TermType.TECH,
            span_start=0,
            span_end=10
        )
        with pytest.raises(ValueError):
            clean_tech_annotation(annotation)
    
    def test_clean_tech_term_none(self):
        """Test that annotations without tech_term are returned unchanged."""
        annotation = Annotation(
            lay_term="Zuckerkrankheit",
            type=TermType.LAY,
            span_start=0,
            span_end=10
        )
        result = clean_tech_annotation(annotation)
        assert result.tech_term is None


class TestCleanLayAnnotation:
    """Tests for cleaning lay term annotations."""
    
    def test_clean_basic_lay_term(self):
        """Test cleaning of a basic lay term."""
        annotation = Annotation(
            lay_term="  Zuckerkrankheit  ",
            type=TermType.LAY,
            span_start=0,
            span_end=10
        )
        result = clean_lay_annotation(annotation)
        assert result.lay_term == "Zuckerkrankheit"
    
    def test_clean_lay_term_strips_punctuation(self):
        """Test that punctuation is properly stripped."""
        annotation = Annotation(
            lay_term="Zuckerkrankheit.",
            type=TermType.LAY,
            span_start=0,
            span_end=10
        )
        result = clean_lay_annotation(annotation)
        assert result.lay_term == "Zuckerkrankheit"
    
    def test_clean_lay_term_none(self):
        """Test that annotations without lay_term are returned unchanged."""
        annotation = Annotation(
            tech_term="Diabetes mellitus",
            type=TermType.TECH,
            span_start=0,
            span_end=10
        )
        result = clean_lay_annotation(annotation)
        assert result.lay_term is None


class TestCleanSynonymsAnnotation:
    """Tests for cleaning synonym annotations."""
    
    def test_clean_synonyms_with_trigger(self):
        """Test cleaning of synonyms with 'Syn.:' trigger."""
        annotation = Annotation(
            lay_term="Zuckerkrankheit",
            type=TermType.LAY,
            span_start=0,
            span_end=10,
            synonyms=["Syn.: Diabetes", "Blutzucker"]
        )
        result = clean_synonyms_annotation(annotation)
        assert "Diabetes" in result.synonyms
        assert "Blutzucker" in result.synonyms
    
    def test_clean_empty_synonyms(self):
        """Test that empty synonyms list is handled correctly."""
        annotation = Annotation(
            lay_term="Zuckerkrankheit",
            type=TermType.LAY,
            span_start=0,
            span_end=10,
            synonyms=[]
        )
        result = clean_synonyms_annotation(annotation)
        assert result.synonyms == []
    
    def test_clean_none_synonyms(self):
        """Test that None synonyms are handled correctly."""
        annotation = Annotation(
            lay_term="Zuckerkrankheit",
            type=TermType.LAY,
            span_start=0,
            span_end=10
        )
        result = clean_synonyms_annotation(annotation)
        assert result.synonyms is None


class TestCleanAnnotation:
    """Tests for the complete annotation cleaning pipeline."""
    
    def test_clean_full_annotation(self):
        """Test cleaning of a complete annotation with all components."""
        annotation = Annotation(
            lay_term="  Zuckerkrankheit  ",
            type=TermType.LAY,
            span_start=0,
            span_end=10,
            synonyms=["Syn.: Diabetes"]
        )
        result = clean_annotation(annotation)
        assert result.lay_term == "Zuckerkrankheit"
        assert "Diabetes" in result.synonyms
