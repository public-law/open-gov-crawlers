from datetime import date
import pytest
from more_itertools import first
from scrapy.http.response.html import HtmlResponse

from public_law.shared.utils.text import NonemptyString
from public_law.glossaries.parsers.gbr.cpr_glossary import parse_entries

ORIG_URL = "https://www.legislation.gov.uk/uksi/2020/759/part/Glossary?view=plain"

@pytest.fixture(scope="module")
def response():
    """Load the HTML fixture for Great Britain CPR Glossary"""
    with open("tests/fixtures/gbr/cpr-glossary.html", "rb") as f:
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
    def test_returns_tuple(self, entries):
        assert isinstance(entries, tuple)

    def test_has_entries(self, entries):
        assert len(entries) > 0

    def test_all_entries_have_required_fields(self, entries):
        for entry in entries:
            assert isinstance(entry.phrase, NonemptyString)
            assert hasattr(entry, 'definition')
            assert len(entry.phrase) > 0
            assert len(entry.definition) > 0

    def test_first_entry(self, entries):
        first_entry = first(entries)
        assert first_entry.phrase == "Account monitoring order"
        assert first_entry.definition == "An order requiring certain types of financial institution to provide certain information held by them relating to a customer for the purposes of an investigation."

    def test_last_entry(self, entries):
        last_entry = entries[-1]
        assert last_entry.phrase == "Youth court"
        assert last_entry.definition == "A magistrates' court exercising jurisdiction over offences committed by, and other matters related to, children and young persons."
