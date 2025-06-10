from more_itertools import first, last
import pytest

from public_law.shared.utils.dates import today
from public_law.shared.models.metadata import Subject
from public_law.glossaries.models.glossary import glossary_fixture
from public_law.glossaries.parsers.usa.courts_glossary import parse_glossary
from public_law.shared.utils.text import URL, NonemptyString

ORIG_URL = "https://www.uscourts.gov/glossary"

@pytest.fixture(scope="module")
def glossary():
    return glossary_fixture("usa/courts-glossary.html", ORIG_URL, parse_glossary)

@pytest.fixture
def metadata(glossary):
    return glossary.metadata

@pytest.fixture
def entries(glossary):
    return glossary.entries


class TestMetadata:
    def test_the_name(self, metadata):
        assert metadata.dcterms_title == "Glossary of Legal Terms"

    def test_the_url(self, metadata):
        assert metadata.dcterms_source == ORIG_URL

    def test_the_author(self, metadata):
        assert metadata.dcterms_creator == "https://public.law"

    def test_coverage(self, metadata):
        assert metadata.dcterms_coverage == "USA"

    def test_the_source_modified_date(self, metadata):
        assert metadata.publiclaw_sourceModified == "unknown"

    def test_the_scrape_date(self, metadata):
        assert metadata.dcterms_modified == today()

    def test_subjects(self, metadata):
        assert metadata.dcterms_subject == (
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
    def test_phrase(self, entries):
        assert first(entries).phrase == "Acquittal"

    def test_definition(self, entries):
        assert first(entries).definition == (
            "A jury verdict that a criminal defendant is not guilty, "
            "or the finding of a judge that the evidence is insufficient "
            "to support a conviction."
        )

    def test_proper_number_of_entries(self, entries):
        assert len(entries) == 237

    def test_the_last_entry(self, entries):
        last_entry = last(entries)

        assert last_entry.phrase == "Writ of certiorari"
        assert last_entry.definition == (
            "An order issued by the U.S. Supreme Court directing "
            "the lower court to transmit records for a case which "
            "it will hear on appeal."
        )
