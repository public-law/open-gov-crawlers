from more_itertools import first, last
import pytest
from scrapy.http.response.html import HtmlResponse

from public_law.glossaries.parsers.nzl.justice_glossary import parse_entries

ORIG_URL = "https://www.justice.govt.nz/about/glossary/"

@pytest.fixture(scope="module")
def html_response():
    with open("tests/fixtures/nzl/justice-glossary.html", encoding="utf8") as f:
        html = f.read()
    return HtmlResponse(
        url=ORIG_URL,
        body=html,
        encoding="utf-8",
    )

@pytest.fixture(scope="module")
def entries(html_response):
    return parse_entries(html_response)


class TestEntries:
    def test_phrase(self, entries):
        assert first(entries).phrase == "acquit"

    def test_definition(self, entries):
        assert (
            first(entries).definition
            == "To decide officially in court that a person is not guilty."
        )

    def test_proper_number_of_entries(self, entries):
        assert len(entries) == 154

    def test_last_entry(self, entries):
        last_entry = last(entries)

        assert last_entry.phrase == "Youth Court"
        assert last_entry.definition == (
            "The Youth Court has jurisdiction to deal with "
            "young people charged with criminal offences."
        )
