from more_itertools import first, last
import pytest
from scrapy.http.response.html import HtmlResponse

from public_law.shared.utils.text import NonemptyString
from public_law.glossaries.parsers.aus.dv_glossary import parse_entries

GLOSSARY_URL = "https://www.aihw.gov.au/reports-data/behaviours-risk-factors/domestic-violence/glossary"

@pytest.fixture(scope="module")
def response():
    """Load the HTML fixture for Australia DV Glossary"""
    with open("tests/fixtures/aus/dv-glossary.html", "rb") as f:
        html_content = f.read()
    
    return HtmlResponse(
        url=GLOSSARY_URL,
        body=html_content,
        encoding="utf-8",
    )

@pytest.fixture
def entries(response):
    return parse_entries(response)


class TestParseEntries:
    def test_first_entry_phrase(self, entries):
        assert first(entries).phrase == "arranged marriage"

    def test_first_entry_definition(self, entries):
        assert first(entries).definition == (
            "Distinct from <strong>forced marriage</strong>, an arranged marriage is organised "
            "by the families of both spouses, but consent is still present, "
            "and the spouses have the right to accept or reject the marriage arrangement."
        )

    def test_last_entry_phrase(self, entries):
        assert last(entries).phrase == "vulnerable groups"

    def test_last_entry_definition(self, entries):
        last_entry = last(entries)

        assert last_entry.definition == (
            "Population groups that are more likely to experience (or to have experienced) "
            "family, domestic and sexual violence, or that face additional barriers in "
            "coping with and recovering from family, domestic and sexual violence."
        )

    def test_proper_number_of_entries(self, entries):
        assert len(entries) == 37

    def test_returns_tuple(self, entries):
        assert isinstance(entries, tuple)

    def test_all_entries_have_required_fields(self, entries):
        for entry in entries:
            assert isinstance(entry.phrase, NonemptyString)
            assert hasattr(entry, 'definition')
