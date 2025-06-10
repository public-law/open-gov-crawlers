from datetime import date
import pytest
from more_itertools import first

from public_law.glossaries.models.glossary import glossary_fixture
from public_law.glossaries.parsers.gbr.cpr_glossary import parse_glossary

ORIG_URL = "https://www.legislation.gov.uk/uksi/2020/759/part/Glossary?view=plain"

@pytest.fixture(scope="module")
def glossary():
    return glossary_fixture("gbr/cpr-glossary.html", ORIG_URL, parse_glossary)

@pytest.fixture
def metadata(glossary):
    return glossary.metadata

@pytest.fixture
def entries(glossary):
    return glossary.entries


class TestMetadata:
    def test_title(self, metadata):
        assert metadata.dcterms_title == "Criminal Procedure Rules Glossary"

    def test_language(self, metadata):
        assert metadata.dcterms_language == "en"

    def test_coverage(self, metadata):
        assert metadata.dcterms_coverage == "GBR"

    def test_source_creator(self, metadata):
        assert metadata.publiclaw_sourceCreator == "The National Archives"

    def test_source_modified(self, metadata):
        assert metadata.publiclaw_sourceModified == date(2020, 10, 5)


class TestEntries:
    def test_has_entries(self, entries):
        assert len(entries) > 0

    def test_first_entry(self, entries):
        first_entry = first(entries)
        assert first_entry.phrase == "Account monitoring order"
        assert first_entry.definition == "An order requiring certain types of financial institution to provide certain information held by them relating to a customer for the purposes of an investigation."

    def test_last_entry(self, entries):
        last_entry = entries[-1]
        assert last_entry.phrase == "Youth court"
        assert last_entry.definition == "A magistrates' court exercising jurisdiction over offences committed by, and other matters related to, children and young persons."
