from datetime import date

import pytest
from scrapy.http.response.html import HtmlResponse

from public_law.parsers.aus.law_handbook import parse_glossary
from public_law.models.glossary import GlossaryParseResult


@pytest.fixture
def glossary_response():
    """Create a mock response with the glossary HTML content."""
    with open("tests/fixtures/aus/handbook-glossary.html", "r") as f:
        html_content = f.read()

    return HtmlResponse(
        url="https://lawhandbook.sa.gov.au/go01.php",
        body=html_content.encode(),
        encoding="utf-8",
    )


@pytest.fixture
def parsed_glossary(glossary_response):
    """Parse the glossary and return the result."""
    return parse_glossary(glossary_response)


def test_glossary_has_entries(parsed_glossary):
    """Test that the glossary has entries."""
    assert len(tuple(parsed_glossary.entries)) > 0


@pytest.mark.parametrize("field,expected", [
    ("dcterms_title",            "Law Handbook Glossary"),
    ("dcterms_language",         "en"),
    ("dcterms_coverage",         "AUS"),
    ("publiclaw_sourceCreator",  "Legal Services Commission of South Australia"),
    ("publiclaw_sourceModified", "unknown"),
])
def test_glossary_metadata(parsed_glossary, field, expected):
    """Test individual metadata fields."""
    assert getattr(parsed_glossary.metadata, field) == expected


def test_first_glossary_entry(parsed_glossary: GlossaryParseResult):
    """Test the first glossary entry."""
    entries = tuple(parsed_glossary.entries)
    first_entry = entries[0]

    assert first_entry.phrase == "abduction"
    assert first_entry.definition == "Unlawful removal of a person (often a child) from their home environment."


def test_last_glossary_entry(parsed_glossary: GlossaryParseResult):
    """Test the last glossary entry."""
    entries = tuple(parsed_glossary.entries)
    last_entry = entries[-1]

    assert last_entry.phrase == "written off"
    assert last_entry.definition == "Of a debt: cancelled, releasing the debtor from obligation to pay."
