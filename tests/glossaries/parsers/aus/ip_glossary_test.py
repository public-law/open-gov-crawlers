import pytest
from more_itertools import first, last
from scrapy.http.response.html import HtmlResponse

from public_law.shared.utils.text import NonemptyString
from public_law.glossaries.parsers.aus.ip_glossary import parse_entries

ORIG_URL = "https://www.ipaustralia.gov.au/tools-resources/ip-glossary"

@pytest.fixture(scope="module")
def response():
    """Load the HTML fixture for Australia IP Glossary"""
    with open("tests/fixtures/aus/ip-glossary.html", "rb") as f:
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
    def test_first_entry_phrase(self, entries):
        assert first(entries).phrase == "Assignee"

    def test_first_entry_definition(self, entries):
        assert (
            first(entries).definition
            == "The person/s or corporate body to whom all or limited rights under an IP right are legally transferred."
        )

    def test_proper_number_of_entries(self, entries):
        assert len(entries) == 53

    def test_last_entry(self, entries):
        last_entry = last(entries)

        assert last_entry.phrase == "Voluntary request for examination"
        assert last_entry.definition == (
            "You as the applicant for an IP right (e.g. innovation patent) "
            "request the registrar to conduct an examination of your application. "
            "This is normally done if you believe that your rights have been infringed."
        )

    def test_returns_tuple(self, entries):
        assert isinstance(entries, tuple)

    def test_all_entries_have_required_fields(self, entries):
        for entry in entries:
            assert isinstance(entry.phrase, NonemptyString)
            assert hasattr(entry, 'definition')
