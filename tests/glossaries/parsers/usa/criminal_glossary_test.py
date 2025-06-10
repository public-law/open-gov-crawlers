import pytest
from more_itertools import first

from public_law.glossaries.models.glossary import glossary_fixture
from public_law.glossaries.parsers.usa.criminal_glossary import parse_glossary

ORIG_URL = "https://www.sdcourt.ca.gov/sdcourt/criminal2/criminalglossary"

@pytest.fixture(scope="module")
def glossary():
    return glossary_fixture("usa/criminal-glossary.html", ORIG_URL, parse_glossary)

@pytest.fixture
def metadata(glossary):
    return glossary.metadata

@pytest.fixture
def entries(glossary):
    return glossary.entries


class TestMetadata:
    def test_title(self, metadata):
        assert metadata.dcterms_title == "Criminal Glossary"

    def test_language(self, metadata):
        assert metadata.dcterms_language == "en"

    def test_coverage(self, metadata):
        assert metadata.dcterms_coverage == "USA"

    def test_source_creator(self, metadata):
        assert metadata.publiclaw_sourceCreator == "Superior Court of California, County of San Diego"

    def test_source_modified(self, metadata):
        assert metadata.publiclaw_sourceModified == "unknown"


class TestEntries:
    def test_has_entries(self, entries):
        assert len(entries) > 0

    def test_first_entry(self, entries):
        first_entry = first(entries)
        assert first_entry.phrase == "Adjourn"
        assert first_entry.definition == "To close a court session for a time."

    def test_last_entry(self, entries):
        last_entry = entries[-1]
        assert last_entry.phrase == "Witness"
        assert last_entry.definition == "A person who testifies as to what was seen, heard, or otherwise known."
