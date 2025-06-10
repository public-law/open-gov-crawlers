from datetime import date
import pytest
from more_itertools import first

from public_law.glossaries.models.glossary import glossary_fixture
from public_law.glossaries.parsers.aus.designip_glossary import parse_glossary

ORIG_URL = "http://manuals.ipaustralia.gov.au/design/glossary"

@pytest.fixture(scope="module")
def glossary():
    return glossary_fixture("aus/designip-glossary.html", ORIG_URL, parse_glossary)

@pytest.fixture
def metadata(glossary):
    return glossary.metadata

@pytest.fixture
def entries(glossary):
    return glossary.entries


class TestMetadata:
    def test_title(self, metadata):
        assert metadata.dcterms_title == "Design Examiners Manual Glossary"

    def test_language(self, metadata):
        assert metadata.dcterms_language == "en"

    def test_coverage(self, metadata):
        assert metadata.dcterms_coverage == "AUS"

    def test_source_creator(self, metadata):
        assert metadata.publiclaw_sourceCreator == "IP Australia"

    def test_source_modified(self, metadata):
        assert metadata.publiclaw_sourceModified == date(2024, 10, 14)


class TestEntries:
    def test_has_entries(self, entries):
        assert len(entries) > 0

    def test_entry_count(self, entries):
        assert len(entries) == 87

    def test_first_entry(self, entries):
        first_entry = first(entries)
        assert first_entry.phrase == "ART"
        assert first_entry.definition == "Administrative Review Tribunal."

    def test_second_entry(self, entries):
        second_entry = entries[1]
        assert second_entry.phrase == "Address for correspondence"
        assert second_entry.definition == "An additional address to which IP Australia may forward correspondence. Note that this is not a requirement, whereas an address for service is a requirement."

    def test_last_entry(self, entries):
        last_entry = entries[-1]
        assert last_entry.phrase == "Withdraw (as in withdraw a design)"
        assert last_entry.definition == "Where an applicant elects to discontinue their application under s 32 of the Act."
