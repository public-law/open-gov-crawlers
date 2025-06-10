from more_itertools import first, last
import pytest

from public_law.shared.utils.dates import today
from public_law.shared.models.metadata import Subject
from public_law.glossaries.models.glossary import glossary_fixture
# The System Under Test
from public_law.glossaries.parsers.aus.dv_glossary import parse_glossary
from public_law.shared.utils.text import URL, NonemptyString

GLOSSARY_URL = URL(
    "https://www.aihw.gov.au/reports-data/behaviours-risk-factors/domestic-violence/glossary"
)

@pytest.fixture(scope="module")
def glossary():
    return glossary_fixture("aus/dv-glossary.html", GLOSSARY_URL, parse_glossary)

@pytest.fixture
def metadata(glossary):
    return glossary.metadata


class TestTheMetadata:
    def test_the_name(self, metadata):
        assert metadata.dcterms_title == "Family, domestic and sexual violence glossary"

    def test_the_url(self, metadata):
        assert metadata.dcterms_source == GLOSSARY_URL

    def test_the_author(self, metadata):
        assert metadata.dcterms_creator == "https://public.law"

    def test_coverage(self, metadata):
        assert metadata.dcterms_coverage == "AUS"

    def test_creator(self, metadata):
        assert (
            metadata.publiclaw_sourceCreator
            == "Australian Institute of Health and Welfare"
        )

    def test_the_source_modified_date(self, metadata):
        assert metadata.publiclaw_sourceModified == "unknown"

    def test_the_scrape_date(self, metadata):
        assert metadata.dcterms_modified == today()

    def test_subjects(self, metadata):
        assert metadata.dcterms_subject == (
            Subject(
                uri=URL("http://id.loc.gov/authorities/subjects/sh85047071"),
                rdfs_label=NonemptyString("Family violence"),
            ),
            Subject(
                uri=URL("https://www.wikidata.org/wiki/Q156537"),
                rdfs_label=NonemptyString("Domestic violence"),
            ),
        )


class TestTheEntries:
    def test_phrase(self, glossary):
        assert first(glossary.entries).phrase == "arranged marriage"

    def test_definition(self, glossary):
        assert first(glossary.entries).definition == (
            "Distinct from <strong>forced marriage</strong>, an arranged marriage is organised "
            "by the families of both spouses, but consent is still present, "
            "and the spouses have the right to accept or reject the marriage arrangement."
        )

    def test_the_last_entry_phrase(self, glossary):
        assert last(glossary.entries).phrase == "vulnerable groups"

    def test_the_last_entry_definition(self, glossary):
        last_entry = last(glossary.entries)

        assert last_entry.definition == (
            "Population groups that are more likely to experience (or to have experienced) "
            "family, domestic and sexual violence, or that face additional barriers in "
            "coping with and recovering from family, domestic and sexual violence."
        )

    def test_proper_number_of_entries(self, glossary):
        assert len(glossary.entries) == 37
