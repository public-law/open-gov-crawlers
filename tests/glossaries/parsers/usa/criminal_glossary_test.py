import pytest
from more_itertools import first
from scrapy.http.response.html import HtmlResponse

from public_law.glossaries.parsers.usa.criminal_glossary import parse_entries

ORIG_URL = "https://www.sdcourt.ca.gov/sdcourt/criminal2/criminalglossary"

@pytest.fixture(scope="module")
def html_response():
    with open("tests/fixtures/usa/criminal-glossary.html", encoding="utf8") as f:
        html = f.read()
    return HtmlResponse(
        url=ORIG_URL,
        body=html,
        encoding="utf-8",
    )

@pytest.fixture
def entries(html_response):
    return parse_entries(html_response)

class TestEntries:
    def test_has_entries(self, entries):
        assert len(entries) > 0

    def test_first_entry(self, entries):
        first_entry = first(entries)
        assert first_entry.phrase == "Adjourn"
        assert first_entry.definition == "To close a court session for a time."

    def test_last_entry(self, entries):
        last_entry = entries[-1]
        assert last_entry.phrase == "Witness"
        assert last_entry.definition == "A person who testifies as to what was seen, heard, or otherwise known."
