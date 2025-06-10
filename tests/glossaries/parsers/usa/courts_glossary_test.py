from more_itertools import first, last
import pytest

from public_law.glossaries.models.glossary import GlossaryEntry
from public_law.glossaries.parsers.usa.courts_glossary import parse_entries
from public_law.shared.utils.text import NonemptyString
from scrapy.http.response.html import HtmlResponse

ORIG_URL = "https://www.uscourts.gov/glossary"

@pytest.fixture(scope="module")
def response():
    """Create a mock response for testing parse_entries function."""
    with open("tests/fixtures/usa/courts-glossary.html", "rb") as f:
        html_content = f.read()
    
    return HtmlResponse(
        url=ORIG_URL,
        body=html_content,
        encoding="utf-8",
    )

@pytest.fixture
def entries(response):
    """Parse entries using the new parse_entries function."""
    return parse_entries(response)


class TestParseEntries:
    """Test the pure data extraction function parse_entries()."""
    
    def test_returns_tuple_of_glossary_entries(self, entries):
        assert isinstance(entries, tuple)
        assert all(isinstance(entry, GlossaryEntry) for entry in entries)

    def test_first_entry_phrase(self, entries):
        assert first(entries).phrase == "Acquittal"

    def test_first_entry_definition(self, entries):
        assert first(entries).definition == (
            "A jury verdict that a criminal defendant is not guilty, "
            "or the finding of a judge that the evidence is insufficient "
            "to support a conviction."
        )

    def test_proper_number_of_entries(self, entries):
        assert len(entries) == 237

    def test_last_entry(self, entries):
        last_entry = last(entries)
        assert last_entry.phrase == "Writ of certiorari"
        assert last_entry.definition == (
            "An order issued by the U.S. Supreme Court directing "
            "the lower court to transmit records for a case which "
            "it will hear on appeal."
        )
