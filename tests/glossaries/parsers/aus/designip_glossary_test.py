import pytest
from more_itertools import first
from scrapy.http.response.html import HtmlResponse

from public_law.shared.utils.text import NonemptyString
from public_law.glossaries.parsers.aus.designip_glossary import parse_entries

ORIG_URL = "http://manuals.ipaustralia.gov.au/design/glossary"

@pytest.fixture(scope="module")
def response():
    """Load the HTML fixture for Australia Design IP Glossary"""
    with open("tests/fixtures/aus/designip-glossary.html", "rb") as f:
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

    def test_entry_count(self, entries):
        assert len(entries) == 87

    def test_first_entry(self, entries):
        first_entry = first(entries)
        assert first_entry.phrase == "ART"
        assert first_entry.definition == "Administrative Review Tribunal."

    def test_second_entry(self, entries):
        second_entry = entries[1]
        assert second_entry.phrase == "Address for correspondence"
        assert second_entry.definition == "An additional address to which IP Australia may forward correspondence. Note that this is not a requirement, whereas an address for service is a requirement."

    def test_last_entry(self, entries):
        last_entry = entries[-1]
        assert last_entry.phrase == "Withdraw (as in withdraw a design)"
        assert last_entry.definition == "Where an applicant elects to discontinue their application under s 32 of the Act."

    def test_returns_tuple(self, entries):
        assert isinstance(entries, tuple)

    def test_all_entries_have_required_fields(self, entries):
        for entry in entries:
            assert isinstance(entry.phrase, NonemptyString)
            assert hasattr(entry, 'definition')
