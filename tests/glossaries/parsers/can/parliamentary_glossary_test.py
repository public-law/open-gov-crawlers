import pytest
from more_itertools import first, last, nth
from scrapy.http.response.html import HtmlResponse

from public_law.shared.utils.text import NonemptyString
from public_law.glossaries.parsers.can.parliamentary_glossary import parse_entries

ORIG_URL = "https://lop.parl.ca/About/Parliament/Education/glossary-intermediate-students-e.html"

@pytest.fixture(scope="module")
def response():
    """Load the HTML fixture for Canada Parliamentary Glossary"""
    with open("tests/fixtures/can/parliamentary-glossary.html", "rb") as f:
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

    def test_proper_number_of_entries(self, entries):
        assert len(entries) == 86

    def test_first_entry(self, entries):
        first_entry = first(entries)
        assert first_entry.phrase == "adjournment proceedings"
        assert first_entry.definition == (
            "A 30-minute period before the end of a daily sitting in the "
            "House of Commons when Members of Parliament can debate matters "
            "raised in Question Period or written questions that have not "
            "been answered within 45 days."
        )

    def test_last_entry(self, entries):
        last_entry = last(entries)
        assert last_entry.phrase == "whip"
        assert last_entry.definition == (
            "The Member who is responsible for keeping other "
            "members of the same party informed about House "
            "business and ensuring their attendance in the "
            "Chamber, especially when a vote is anticipated."
        )

    def test_usher_of_black_rod_entry(self, entries):
        """Test that the 'Usher...' entry is properly fixed to 'Usher of the Black Rod'"""
        entry = nth(entries, 83)
        assert entry
        assert entry.phrase == "Usher of the Black Rod"

    def test_committees_entry_skipped(self, entries):
        """Test that 'Committees' entry is properly skipped"""
        phrases = [str(entry.phrase) for entry in entries]
        assert "Committees" not in phrases

    def test_returns_tuple(self, entries):
        assert isinstance(entries, tuple)

    def test_all_entries_have_required_fields(self, entries):
        for entry in entries:
            assert isinstance(entry.phrase, NonemptyString)
            assert hasattr(entry, 'definition')
            assert len(entry.phrase) > 0
            assert len(entry.definition) > 0
