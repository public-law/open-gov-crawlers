from datetime import date

import pytest
from scrapy.http.response.html import HtmlResponse

from public_law.parsers.aus.designip_glossary import parse_glossary
from public_law.models.glossary import GlossaryParseResult


@pytest.fixture
def glossary_response():
    """Create a mock response with the glossary HTML content."""
    with open("tests/fixtures/aus/designip-glossary.html", "r") as f:
        html_content = f.read()

    return HtmlResponse(
        url="http://manuals.ipaustralia.gov.au/design/glossary",
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


def test_glossary_has_correct_number_of_entries(parsed_glossary):
    """Test that the glossary has the correct number of entries."""
    assert len(tuple(parsed_glossary.entries)) == 172


@pytest.mark.parametrize("field,expected", [
    ("dcterms_title",            "Design Examiners Manual Glossary"),
    ("dcterms_language",         "en"),
    ("dcterms_coverage",         "AUS"),
    ("publiclaw_sourceCreator",  "IP Australia"),
    ("publiclaw_sourceModified", date(2024, 10, 14)),
])
def test_glossary_metadata(parsed_glossary, field, expected):
    """Test individual metadata fields."""
    assert getattr(parsed_glossary.metadata, field) == expected


def test_first_glossary_entry(parsed_glossary: GlossaryParseResult):
    """Test the first glossary entry."""
    entries = tuple(parsed_glossary.entries)
    first_entry = entries[0]

    assert first_entry.phrase == "ART"
    assert first_entry.definition == "Administrative Review Tribunal."


def test_last_glossary_entry(parsed_glossary: GlossaryParseResult):
    """Test the last glossary entry."""
    entries = tuple(parsed_glossary.entries)
    last_entry = entries[-1]

    assert last_entry.phrase == "Withdraw (as in withdraw a design)"
    assert last_entry.definition == "Where an applicant elects to discontinue their application under s 32 of the Act.​​​​​​​"
