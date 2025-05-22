from datetime import date

import pytest
from scrapy.http.response.html import HtmlResponse

from public_law.parsers.gbr.cpr_glossary import parse_glossary


@pytest.fixture
def glossary_response():
    """Create a mock response with the glossary HTML content."""
    with open("tests/fixtures/gbr/cpr-glossary.html", "r") as f:
        html_content = f.read()

    return HtmlResponse(
        url="https://www.legislation.gov.uk/uksi/2020/759/part/Glossary?view=plain",
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
    ("dcterms_title", "Criminal Procedure Rules Glossary"),
    ("dcterms_language", "en"),
    ("dcterms_coverage", "GBR"),
    ("publiclaw_sourceCreator", "The National Archives"),
    ("publiclaw_sourceModified", date(2020, 10, 5)),
])
def test_glossary_metadata(parsed_glossary, field, expected):  # type: ignore
    """Test individual metadata fields."""
    assert getattr(parsed_glossary.metadata, field) == expected  # type: ignore


def test_first_glossary_entry(parsed_glossary):  # type: ignore
    """Test the first glossary entry."""
    entries = tuple(parsed_glossary.entries)  # type: ignore
    first_entry = entries[0]  # type: ignore

    assert first_entry.phrase == "Account monitoring order"  # type: ignore
    assert first_entry.definition == "An order requiring certain types of financial institution to provide certain information held by them relating to a customer for the purposes of an investigation."  # type: ignore


def test_last_glossary_entry(parsed_glossary):  # type: ignore
    """Test the last glossary entry."""
    entries = tuple(parsed_glossary.entries)  # type: ignore
    last_entry = entries[-1]  # type: ignore

    assert last_entry.phrase == "Youth court"  # type: ignore
    assert last_entry.definition == "A magistrates' court exercising jurisdiction over offences committed by, and other matters related to, children and young persons."  # type: ignore
