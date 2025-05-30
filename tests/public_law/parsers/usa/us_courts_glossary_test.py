from more_itertools import first, last

from public_law.dates import today
from public_law.metadata import Subject
from public_law.models.glossary import glossary_fixture
from public_law.parsers.usa.courts_glossary import parse_glossary
from public_law.text import URL, NonemptyString

ORIG_URL = "https://www.uscourts.gov/glossary"
GLOSSARY = glossary_fixture(
    "usa/courts-glossary.html", ORIG_URL, parse_glossary)
METADATA = GLOSSARY.metadata
ENTRIES = tuple(GLOSSARY.entries)


class TestMetadata:
    def test_the_name(_):
        assert METADATA.dcterms_title == "Glossary of Legal Terms"

    def test_the_url(_):
        assert METADATA.dcterms_source == ORIG_URL

    def test_the_author(_):
        assert METADATA.dcterms_creator == "https://public.law"

    def test_coverage(_):
        assert METADATA.dcterms_coverage == "USA"

    def test_the_source_modified_date(_):
        assert METADATA.publiclaw_sourceModified == "unknown"

    def test_the_scrape_date(_):
        assert METADATA.dcterms_modified == today()

    def test_subjects(_):
        assert METADATA.dcterms_subject == (
            Subject(
                uri=URL("http://id.loc.gov/authorities/subjects/sh85033575"),
                rdfs_label=NonemptyString("Courts--United States"),
            ),
            Subject(
                uri=URL("https://www.wikidata.org/wiki/Q194907"),
                rdfs_label=NonemptyString("United States federal courts"),
            ),
        )


class TestEntries:
    def test_phrase(_):
        assert first(ENTRIES).phrase == "Acquittal"

    def test_definition(_):
        assert first(ENTRIES).definition == (
            "A jury verdict that a criminal defendant is not guilty, "
            "or the finding of a judge that the evidence is insufficient "
            "to support a conviction."
        )

    def test_proper_number_of_entries(_):
        assert len(tuple(ENTRIES)) == 237

    def test_the_last_entry(_):
        last_entry = last(ENTRIES)

        assert last_entry.phrase == "Writ of certiorari"
        assert last_entry.definition == (
            "An order issued by the U.S. Supreme Court directing "
            "the lower court to transmit records for a case which "
            "it will hear on appeal."
        )
