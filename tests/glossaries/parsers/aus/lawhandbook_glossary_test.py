from datetime import date
import pytest
from more_itertools import first

from public_law.glossaries.models.glossary import glossary_fixture
from public_law.glossaries.parsers.aus.lawhandbook_glossary import parse_glossary

ORIG_URL = "https://lawhandbook.sa.gov.au/go01.php"

@pytest.fixture(scope="module")
def glossary():
    return glossary_fixture("aus/lawhandbook-glossary.html", ORIG_URL, parse_glossary)

@pytest.fixture
def metadata(glossary):
    return glossary.metadata

@pytest.fixture
def entries(glossary):
    return glossary.entries


class TestMetadata:
    def test_title(self, metadata):
        assert metadata.dcterms_title == "Law Handbook Glossary"

    def test_language(self, metadata):
        assert metadata.dcterms_language == "en"

    def test_coverage(self, metadata):
        assert metadata.dcterms_coverage == "AUS"

    def test_source_creator(self, metadata):
        assert metadata.publiclaw_sourceCreator == "Legal Services Commission of South Australia"

    def test_source_modified(self, metadata):
        assert metadata.publiclaw_sourceModified == "unknown"


class TestEntries:
    def test_has_entries(self, entries):
        assert len(entries) > 0

    def test_first_entry(self, entries):
        first_entry = first(entries)
        assert first_entry.phrase == "abduction"
        assert first_entry.definition == "Unlawful removal of a person (often a child) from their home environment."

    def test_last_entry(self, entries):
        last_entry = entries[-1]
        assert last_entry.phrase == "written off"
        assert last_entry.definition == "Of a debt: cancelled, releasing the debtor from obligation to pay."
