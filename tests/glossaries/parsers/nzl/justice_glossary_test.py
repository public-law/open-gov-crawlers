from more_itertools import first, last
import pytest

from public_law.shared.utils.dates import today
from public_law.shared.models.metadata import Subject
from public_law.glossaries.models.glossary import glossary_fixture
from public_law.glossaries.parsers.nzl.justice_glossary import parse_glossary
from public_law.shared.utils.text import URL, NonemptyString

ORIG_URL = "https://www.justice.govt.nz/about/glossary/"

@pytest.fixture(scope="module")
def glossary():
    return glossary_fixture("nzl/justice-glossary.html", ORIG_URL, parse_glossary)

@pytest.fixture
def metadata(glossary):
    return glossary.metadata

@pytest.fixture
def entries(glossary):
    return glossary.entries


class TestMetadata:
    def test_name(self, metadata):
        assert metadata.dcterms_title == "Glossary"

    def test_url(self, metadata):
        assert metadata.dcterms_source == ORIG_URL

    def test_author(self, metadata):
        assert metadata.dcterms_creator == "https://public.law"

    def test_coverage(self, metadata):
        assert metadata.dcterms_coverage == "NZL"

    def test_source_modified_date(self, metadata):
        assert metadata.publiclaw_sourceModified == "unknown"

    def test_scrape_date(self, metadata):
        assert metadata.dcterms_modified == today()

    def test_subjects(self, metadata):
        assert metadata.dcterms_subject == (
            Subject(
                uri=URL("http://id.loc.gov/authorities/subjects/sh85071120"),
                rdfs_label=NonemptyString("Justice, Administration of"),
            ),
            Subject(
                uri=URL("https://www.wikidata.org/wiki/Q16514399"),
                rdfs_label=NonemptyString("Administration of justice"),
            ),
        )


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
