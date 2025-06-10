from more_itertools import first, last
import pytest

from public_law.shared.utils.dates import today
from public_law.shared.models.metadata import Subject
from public_law.glossaries.models.glossary import glossary_fixture
from public_law.glossaries.parsers.usa.uscis_glossary import parse_glossary
from public_law.shared.utils.text import URL, NonemptyString

ORIG_URL = "https://www.uscis.gov/tools/glossary"

@pytest.fixture(scope="module")
def glossary():
    return glossary_fixture("usa/uscis-glossary.html", ORIG_URL, parse_glossary)

@pytest.fixture
def metadata(glossary):
    return glossary.metadata

@pytest.fixture
def entries(glossary):
    return glossary.entries


class TestMetadata:
    def test_title(self, metadata):
        assert metadata.dcterms_title == "USCIS Glossary"

    def test_url(self, metadata):
        assert metadata.dcterms_source == "https://www.uscis.gov/tools/glossary"

    def test_author(self, metadata):
        assert metadata.dcterms_creator == "https://public.law"

    def test_source_creator(self, metadata):
        assert metadata.publiclaw_sourceCreator == "U.S. Citizenship and Immigration Services"

    def test_coverage(self, metadata):
        assert metadata.dcterms_coverage == "USA"

    def test_source_modified_date(self, metadata):
        assert metadata.publiclaw_sourceModified == "unknown"

    def test_scrape_date(self, metadata):
        assert metadata.dcterms_modified == today()

    def test_subjects(self, metadata):
        assert metadata.dcterms_subject == (
            Subject(
                uri=URL("http://id.loc.gov/authorities/subjects/sh85042790"),
                rdfs_label=NonemptyString("Emigration and immigration law"),
            ),
            Subject(
                uri=URL("https://www.wikidata.org/wiki/Q231147"),
                rdfs_label=NonemptyString("immigration law"),
            ),
        )


class TestEntries:
    def test_phrase(self, entries):
        assert first(entries).phrase == "Alien Registration Number"

    def test_definition(self, entries):
        assert (
            first(entries).definition == (
                '<p>A unique seven-, eight- or nine-digit number assigned to a noncitizen '
                'by the Department of Homeland Security. Also see '
                '<a aria-label="Show glossary definition for USCIS Number" data-entity-substitution="canonical" data-entity-type="node" data-lang="en" data-linktype="glossary" data-nid="50674" href="#">USCIS Number</a>.'
                '</p>'
            )
        )

    def test_entry_count(self, entries):
        assert len(entries) == 266

    def test_last_phrase(self, entries):
        last_entry = last(entries)
        assert last_entry.phrase == "Withdrawal"

    def test_last_definition(self, entries):
        last_entry = last(entries)
        assert last_entry.definition == (
            '<p>This is an arriving noncitizen’s voluntary retraction of an application '
            'for admission to the United States in lieu of a removal hearing before an '
            'immigration judge or an expedited removal.</p>'
        )
