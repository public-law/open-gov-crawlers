from datetime import date

import pytest
from scrapy.http.response.html import HtmlResponse

from public_law.parsers.usa.courts_glossary import parse_glossary
from public_law.models.glossary import GlossaryParseResult


@pytest.fixture
def glossary_response():
    """Create a mock response with the glossary HTML content."""
    with open("tests/fixtures/usa/courts_glossary.html", "r") as f:
        html_content = f.read()

    return HtmlResponse(
        url="https://www.sdcourt.ca.gov/sdcourt/criminal2/criminalglossary",
        body=html_content.encode(),
        encoding="utf-8",
    )


@pytest.fixture
def parsed_glossary(glossary_response):  # type: ignore
    """Parse the glossary and return the result."""
    return parse_glossary(glossary_response)  # type: ignore


def test_glossary_has_entries(parsed_glossary):  # type: ignore
    """Test that the glossary has entries."""
    assert len(tuple(parsed_glossary.entries)) > 0  # type: ignore


@pytest.mark.parametrize("field,expected", [
    ("dcterms_title", "US Courts Glossary"),
    ("dcterms_language", "en"),
    ("dcterms_coverage", "USA"),
    ("publiclaw_sourceCreator", "San Diego Superior Court"),
    ("publiclaw_sourceModified", "unknown"),
])
def test_glossary_metadata(parsed_glossary, field, expected):  # type: ignore
    """Test individual metadata fields."""
    assert getattr(parsed_glossary.metadata, field) == expected  # type: ignore


def test_first_glossary_entry(parsed_glossary: GlossaryParseResult):
    """Test the first glossary entry."""
    entries = tuple(parsed_glossary.entries)
    first_entry = entries[0]

    assert first_entry.phrase == "Adjourn"
    assert first_entry.definition == "To close a court session for a time."


def test_last_glossary_entry(parsed_glossary: GlossaryParseResult):
    """Test the last glossary entry."""
    entries = tuple(parsed_glossary.entries)
    last_entry = entries[-1]

    assert last_entry.phrase == "Witness"
    assert last_entry.definition == "A person who testifies as to what was seen, heard, or otherwise known."
