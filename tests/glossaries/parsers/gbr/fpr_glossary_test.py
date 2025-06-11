import pytest
from more_itertools import first
from scrapy.http.response.html import HtmlResponse

from public_law.shared.utils.text import NonemptyString
from public_law.glossaries.parsers.gbr.fpr_glossary import parse_entries

ORIG_URL = "https://www.justice.gov.uk/courts/procedure-rules/family/backmatter/fpr_glossary"

@pytest.fixture(scope="module")
def response():
    """Load the HTML fixture for Great Britain FPR Glossary"""
    with open("tests/fixtures/gbr/fpr-glossary.html", "rb") as f:
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
        assert first_entry.phrase == "Affidavit"
        assert first_entry.definition == "A written, sworn, statement of evidence."

    def test_last_entry(self, entries):
        last_entry = entries[-1]
        assert last_entry.phrase == "Without prejudice"
        assert last_entry.definition == "Negotiations with a view to settlement are usually conducted \"without prejudice\" which means that the circumstances in which the content of those negotiations may be revealed to the court are very restricted."
