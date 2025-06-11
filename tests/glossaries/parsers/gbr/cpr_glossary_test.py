import pytest
from more_itertools import first
from scrapy.http.response.html import HtmlResponse

from public_law.glossaries.parsers.gbr.cpr_glossary import parse_entries

ORIG_URL = "https://www.legislation.gov.uk/uksi/2020/759/part/Glossary?view=plain"

@pytest.fixture(scope="module")
def html_response():
    with open("tests/fixtures/gbr/cpr-glossary.html", encoding="utf8") as f:
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
        assert first_entry.phrase == "Account monitoring order"
        assert first_entry.definition == (
            "An order requiring certain types of financial institution to provide certain information held by them relating to a customer for the purposes of an investigation."
        )

    def test_last_entry(self, entries):
        last_entry = entries[-1]
        assert last_entry.phrase == "Youth court"
        assert last_entry.definition == (
            "A magistrates' court exercising jurisdiction over offences committed by, and other matters related to, children and young persons."
        )
