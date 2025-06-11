from more_itertools import first, last
import pytest
from scrapy.http.response.html import HtmlResponse

from public_law.shared.utils.text import NonemptyString
from public_law.glossaries.parsers.irl.courts_glossary import parse_entries


@pytest.fixture(scope="module")
def response():
    """Load the HTML fixture for IRL Courts Glossary"""
    with open("tests/fixtures/irl/courts-glossary.html", "rb") as f:
        html_content = f.read()
    
    return HtmlResponse(
        url="https://www.courts.ie/glossary",
        body=html_content,
        encoding="utf-8",
    )

@pytest.fixture
def entries(response):
    return parse_entries(response)


class TestParseEntries:
    def test_first_entry_definition(self, entries):
        assert first(entries).definition == "A written statement made on oath."

    def test_gets_proper_number_of_entries(self, entries):
        assert len(entries) == 43

    def test_last_entry(self, entries):
        last_entry = last(entries)

        assert last_entry.phrase == "Supervision order"
        assert last_entry.definition == (
            "An order allowing Tusla to monitor a child considered to be at risk. "
            "The child is not removed from his or her home environment. A supervision "
            "order is for a fixed period of time not longer than 12 months initially."
        )

    def test_returns_tuple(self, entries):
        assert isinstance(entries, tuple)

    def test_all_entries_have_required_fields(self, entries):
        for entry in entries:
            assert isinstance(entry.phrase, NonemptyString)
            assert hasattr(entry, 'definition')
