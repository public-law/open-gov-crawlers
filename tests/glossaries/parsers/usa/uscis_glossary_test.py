from more_itertools import first, last
import pytest

from public_law.glossaries.models.glossary import GlossaryEntry
from public_law.glossaries.parsers.usa.uscis_glossary import parse_entries
from public_law.shared.utils.text import NonemptyString
from scrapy.http.response.html import HtmlResponse

ORIG_URL = "https://www.uscis.gov/tools/glossary"

@pytest.fixture(scope="module")
def response():
    """Create a mock response for testing parse_entries function."""
    with open("tests/fixtures/usa/uscis-glossary.html", "rb") as f:
        html_content = f.read()
    
    return HtmlResponse(
        url=ORIG_URL,
        body=html_content,
        encoding="utf-8",
    )

@pytest.fixture(scope="module")
def entries(response):
    """Parse entries using the new parse_entries function."""
    return tuple(parse_entries(response))


class TestParseEntries:
    """Test the pure data extraction function parse_entries()."""
    
    def test_returns_tuple_of_glossary_entries(self, entries):
        assert isinstance(entries, tuple)
        assert all(isinstance(entry, GlossaryEntry) for entry in entries)

    def test_first_entry_phrase(self, entries):
        assert first(entries).phrase == "Alien Registration Number"

    def test_first_entry_definition(self, entries):
        assert (
            first(entries).definition == (
                '<p>A unique seven-, eight- or nine-digit number assigned to a noncitizen '
                'by the Department of Homeland Security. Also see '
                '<a aria-label="Show glossary definition for USCIS Number" data-entity-substitution="canonical" data-entity-type="node" data-lang="en" data-linktype="glossary" data-nid="50674" href="#">USCIS Number</a>.'
                '</p>'
            )
        )

    def test_entry_count(self, entries):
        assert len(entries) == 266

    def test_last_entry_phrase(self, entries):
        last_entry = last(entries)
        assert last_entry.phrase == "Withdrawal"

    def test_last_entry_definition(self, entries):
        last_entry = last(entries)
        expected = (
            "<p>This is an arriving noncitizen\u2019s voluntary retraction of an application "
            "for admission to the United States in lieu of a removal hearing before an "
            "immigration judge or an expedited removal.</p>"
        )
        assert last_entry.definition == expected
