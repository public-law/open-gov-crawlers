import pytest
from more_itertools import first, last
from scrapy.http.response.html import HtmlResponse

from public_law.shared.utils.text import NonemptyString
from public_law.glossaries.parsers.can.patents_glossary import parse_entries

ORIG_URL = "https://ised-isde.canada.ca/site/canadian-intellectual-property-office/en/patents/glossary"

@pytest.fixture(scope="module")
def response():
    """Load the HTML fixture for Canada Patents Glossary"""
    with open("tests/fixtures/can/patents-glossary.html", "rb") as f:
        html_content = f.read()
    
    return HtmlResponse(
        url=ORIG_URL,
        body=html_content,
        encoding="utf-8",
    )

@pytest.fixture
def entries(response):
    return parse_entries(response)


class TestParseEntries:
    def test_has_entries(self, entries):
        assert len(entries) > 0

    def test_first_entry(self, entries):
        first_entry = first(entries)
        assert first_entry.phrase == "Abstract"
        assert first_entry.definition == "A brief summary of your invention."

    def test_last_entry(self, entries):
        last_entry = last(entries)
        assert last_entry.phrase == "WIPO"
        assert last_entry.definition == "World Intellectual Property Organization."

    def test_specific_entries(self, entries):
        entries_dict = {entry.phrase: entry.definition for entry in entries}
        
        assert "Claims" in entries_dict
        assert entries_dict["Claims"] == "The parts of a patent that define the boundaries of patent protection."
        
        assert "Patent" in entries_dict
        assert entries_dict["Patent"] == "A government grant giving the right to exclude others from making, using, or selling an invention."

    def test_no_date_modified_entry(self, entries):
        """Test that 'Date modified:' is not present as any glossary entry."""
        phrases = [str(entry.phrase) for entry in entries]
        assert "Date modified:" not in phrases

    def test_returns_tuple(self, entries):
        assert isinstance(entries, tuple)

    def test_all_entries_have_required_fields(self, entries):
        for entry in entries:
            assert isinstance(entry.phrase, NonemptyString)
            assert hasattr(entry, 'definition')
            assert len(entry.phrase) > 0
            assert len(entry.definition) > 0 
