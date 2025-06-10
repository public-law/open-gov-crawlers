from more_itertools import first, last, nth
import pytest

from public_law.shared.utils.dates import today
from public_law.shared.models.metadata import Subject
from public_law.glossaries.models.glossary import glossary_fixture
# The System Under Test
from public_law.glossaries.parsers.can.parliamentary_glossary import parse_glossary
from public_law.shared.utils.text import URL, NonemptyString

ORIG_URL = URL(
    "https://lop.parl.ca/About/Parliament/Education/glossary-intermediate-students-e.html"
)

@pytest.fixture(scope="module")
def glossary():
    return glossary_fixture("can/parliamentary-glossary.html", ORIG_URL, parse_glossary)

@pytest.fixture
def metadata(glossary):
    return glossary.metadata

@pytest.fixture
def entries(glossary):
    return glossary.entries


class TestTheMetadata:
    def test_the_name(self, metadata):
        assert (
            metadata.dcterms_title
            == "Glossary of Parliamentary Terms for Intermediate Students"
        )

    def test_the_url(self, metadata):
        assert metadata.dcterms_source == ORIG_URL

    def test_the_author(self, metadata):
        assert metadata.dcterms_creator == "https://public.law"

    def test_coverage(self, metadata):
        assert metadata.dcterms_coverage == "CAN"

    def test_creator(self, metadata):
        assert metadata.publiclaw_sourceCreator == "Parliament of Canada"

    def test_the_source_modified_date(self, metadata):
        assert metadata.publiclaw_sourceModified == "unknown"

    def test_the_scrape_date(self, metadata):
        assert metadata.dcterms_modified == today()

    def test_subjects(self, metadata):
        assert metadata.dcterms_subject == (
            Subject(
                uri=URL("http://id.loc.gov/authorities/subjects/sh85075807"),
                rdfs_label=NonemptyString("Legislative bodies"),
            ),
            Subject(
                uri=URL("https://www.wikidata.org/wiki/Q35749"),
                rdfs_label=NonemptyString("Parliament"),
            ),
        )


class TestTheEntries:
    def test_phrase(self, entries):
        assert first(entries).phrase == "adjournment proceedings"

    def test_definition(self, entries):
        assert first(entries).definition == (
            "A 30-minute period before the end of a daily sitting in the "
            "House of Commons when Members of Parliament can debate matters "
            "raised in Question Period or written questions that have not "
            "been answered within 45 days."
        )

    def test_proper_number_of_entries(self, entries):
        assert len(entries) == 86

    def test_the_last_entry(self, entries):
        last_entry = last(entries)

        assert last_entry.phrase == "whip"
        assert last_entry.definition == (
            "The Member who is responsible for keeping other "
            "members of the same party informed about House "
            "business and ensuring their attendance in the "
            "Chamber, especially when a vote is anticipated."
        )

    def test_the_third_to_the_last_entry(self, entries):
        entry = nth(entries, 83)

        assert entry
        assert entry.phrase == "Usher of the Black Rod"
