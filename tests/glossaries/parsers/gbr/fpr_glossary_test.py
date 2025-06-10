from datetime import date
import pytest
from more_itertools import first

from public_law.glossaries.models.glossary import glossary_fixture
from public_law.glossaries.parsers.gbr.fpr_glossary import parse_glossary

ORIG_URL = "https://www.justice.gov.uk/courts/procedure-rules/family/backmatter/fpr_glossary"

@pytest.fixture(scope="module")
def glossary():
    return glossary_fixture("gbr/fpr-glossary.html", ORIG_URL, parse_glossary)

@pytest.fixture
def metadata(glossary):
    return glossary.metadata

@pytest.fixture
def entries(glossary):
    return glossary.entries


class TestMetadata:
    def test_title(self, metadata):
        assert metadata.dcterms_title == "Family Procedure Rules Glossary"

    def test_language(self, metadata):
        assert metadata.dcterms_language == "en"

    def test_coverage(self, metadata):
        assert metadata.dcterms_coverage == "GBR"

    def test_source_creator(self, metadata):
        assert metadata.publiclaw_sourceCreator == "Ministry of Justice"

    def test_source_modified(self, metadata):
        assert metadata.publiclaw_sourceModified == date(2017, 1, 30)


class TestEntries:
    def test_has_entries(self, entries):
        assert len(entries) > 0

    def test_first_entry(self, entries):
        first_entry = first(entries)
        assert first_entry.phrase == "Affidavit"
        assert first_entry.definition == "A written, sworn, statement of evidence."

    def test_last_entry(self, entries):
        last_entry = entries[-1]
        assert last_entry.phrase == "Without prejudice"
        assert last_entry.definition == "Negotiations with a view to settlement are usually conducted \"without prejudice\" which means that the circumstances in which the content of those negotiations may be revealed to the court are very restricted."
