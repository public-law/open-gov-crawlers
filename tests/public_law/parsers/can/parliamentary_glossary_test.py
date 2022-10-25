# pyright: reportSelfClsParameterName=false
from more_itertools import first, last, nth

from public_law.dates import today
from public_law.metadata import Subject
from public_law.models.glossary import glossary_fixture
from public_law.text import URL, NonemptyString

# The System Under Test
from public_law.parsers.can.parliamentary_glossary import parse_glossary


ORIG_URL = URL(
    "https://lop.parl.ca/About/Parliament/Education/glossary-intermediate-students-e.html"
)
GLOSSARY = glossary_fixture("can/parliamentary-glossary.html", ORIG_URL, parse_glossary)
METADATA = GLOSSARY.metadata
ENTRIES = tuple(GLOSSARY.entries)


class TestTheMetadata:
    def test_the_name(_):
        assert (
            METADATA.dcterms_title
            == "Glossary of Parliamentary Terms for Intermediate Students"
        )

    def test_the_url(_):
        assert METADATA.dcterms_source == ORIG_URL

    def test_the_author(_):
        assert METADATA.dcterms_creator == "https://public.law"

    def test_coverage(_):
        assert METADATA.dcterms_coverage == "CAN"

    def test_creator(_):
        assert METADATA.publiclaw_sourceCreator == "Parliament of Canada"

    def test_the_source_modified_date(_):
        assert METADATA.publiclaw_sourceModified == "unknown"

    def test_the_scrape_date(_):
        assert METADATA.dcterms_modified == today()

    def test_subjects(_):
        assert METADATA.dcterms_subject == (
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
    def test_phrase(_):
        assert first(ENTRIES).phrase == "adjournment proceedings"

    def test_definition(_):
        assert first(ENTRIES).definition == (
            "A 30-minute period before the end of a daily sitting in the "
            "House of Commons when Members of Parliament can debate matters "
            "raised in Question Period or written questions that have not "
            "been answered within 45 days."
        )

    def test_proper_number_of_entries(_):
        assert len(tuple(ENTRIES)) == 86

    def test_the_last_entry(_):
        last_entry = last(ENTRIES)

        assert last_entry.phrase == "whip"
        assert last_entry.definition == (
            "The Member who is responsible for keeping other "
            "members of the same party informed about House "
            "business and ensuring their attendance in the "
            "Chamber, especially when a vote is anticipated."
        )

    def test_the_third_to_the_last_entry(_):
        entry = nth(ENTRIES, 83)

        assert entry
        assert entry.phrase == "Usher of the Black Rod"
