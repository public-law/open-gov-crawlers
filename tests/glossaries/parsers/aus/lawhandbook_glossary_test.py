import pytest
from more_itertools import first
from scrapy.http.response.html import HtmlResponse

from public_law.shared.utils.text import NonemptyString
from public_law.glossaries.parsers.aus.lawhandbook_glossary import parse_entries

ORIG_URL = "https://lawhandbook.sa.gov.au/go01.php"

@pytest.fixture(scope="module")
def response():
    """Load the HTML fixture for Australia Law Handbook Glossary"""
    with open("tests/fixtures/aus/lawhandbook-glossary.html", "rb") as f:
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
        assert first_entry.phrase == "abduction"
        assert first_entry.definition == "Unlawful removal of a person (often a child) from their home environment."

    def test_last_entry(self, entries):
        last_entry = entries[-1]
        assert last_entry.phrase == "written off"
        assert last_entry.definition == "Of a debt: cancelled, releasing the debtor from obligation to pay."

    def test_returns_tuple(self, entries):
        assert isinstance(entries, tuple)

    def test_all_entries_have_required_fields(self, entries):
        for entry in entries:
            assert isinstance(entry.phrase, NonemptyString)
            assert hasattr(entry, 'definition')
