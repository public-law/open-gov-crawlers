from more_itertools import first, last
import pytest

from public_law.shared.utils.dates import today
from public_law.shared.models.metadata import Subject
from public_law.glossaries.models.glossary import glossary_fixture, GlossaryParseResult
from public_law.glossaries.parsers.irl.courts_glossary import parse_glossary
from public_law.shared.utils.text import URL, NonemptyString


ORIG_URL = "https://www.courts.ie/glossary"

@pytest.fixture(scope="module")
def glossary():
    print("🔥 GLOSSARY FIXTURE RUNNING - parsing HTML file!")
    return glossary_fixture("irl/courts-glossary.html", ORIG_URL, parse_glossary)

@pytest.fixture
def metadata(glossary):
    return glossary.metadata

@pytest.fixture
def entries(glossary):
    return glossary.entries  # Now this is already a tuple, so no conversion needed


class TestTheMetadata:
    def test_name(self, metadata):
        assert metadata.dcterms_title == "Glossary of Legal Terms"

    def test_url(self, metadata):
        assert metadata.dcterms_source == "https://www.courts.ie/glossary"

    def test_author(self, metadata):
        assert metadata.dcterms_creator == "https://public.law"

    def test_gets_coverage(self, metadata):
        assert metadata.dcterms_coverage == "IRL"

    def test_source_modified_date(self, metadata):
        assert metadata.publiclaw_sourceModified == "unknown"

    def test_scrape_date(self, metadata):
        assert metadata.dcterms_modified == today()

    def test_subjects(self, metadata):
        assert metadata.dcterms_subject == (
            Subject(
                uri=URL("http://id.loc.gov/authorities/subjects/sh85033571"),
                rdfs_label=NonemptyString("Courts"),
            ),
            Subject(
                uri=URL("https://www.wikidata.org/wiki/Q41487"),
                rdfs_label=NonemptyString("Court"),
            ),
        )


class TestTheEntries:
    def test_definition(self, entries):
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
