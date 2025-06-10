import pytest
from more_itertools import first, last
from scrapy.http.response.html import HtmlResponse

from public_law.glossaries.models.glossary import GlossaryEntry, GlossaryParseResult
from public_law.glossaries.spiders.usa.uscis_glossary import USCISGlossary
from public_law.shared.models.metadata import Metadata, Subject
from public_law.shared.utils.dates import today
from public_law.shared.utils.text import URL, NonemptyString

ORIG_URL = "https://www.uscis.gov/tools/glossary"

@pytest.fixture(scope="module")
def response():
    """Create a mock response for testing."""
    with open("tests/fixtures/usa/uscis-glossary.html", "rb") as f:
        html_content = f.read()
    
    return HtmlResponse(
        url=ORIG_URL,
        body=html_content,
        encoding="utf-8",
    )

@pytest.fixture(scope="module")
def spider():
    """Create a spider instance for testing."""
    return USCISGlossary()

@pytest.fixture(scope="module")
def metadata(spider, response):
    """Get metadata from spider for testing."""
    return spider.get_metadata(response)

@pytest.fixture(scope="module")  
def glossary_result(spider, response):
    """Get full parse result from spider for integration testing."""
    return spider.parse_glossary(response)


class TestMetadata:
    """Test the spider's get_metadata() method."""

    def test_returns_metadata_instance(self, metadata):
        assert isinstance(metadata, Metadata)

    def test_title(self, metadata):
        assert metadata.dcterms_title == "USCIS Glossary"

    def test_url(self, metadata):
        assert metadata.dcterms_source == URL("https://www.uscis.gov/tools/glossary")

    def test_source_creator(self, metadata):
        assert metadata.publiclaw_sourceCreator == "U.S. Citizenship and Immigration Services"

    def test_coverage(self, metadata):
        assert metadata.dcterms_coverage == "USA"

    def test_language(self, metadata):
        assert metadata.dcterms_language == "en"

    def test_source_modified_date(self, metadata):
        assert metadata.publiclaw_sourceModified == "unknown"

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


class TestIntegration:
    """Test the full spider functionality including parse_glossary()."""

    def test_parse_glossary_returns_result(self, glossary_result):
        assert isinstance(glossary_result, GlossaryParseResult)

    def test_parse_glossary_has_metadata(self, glossary_result):
        assert isinstance(glossary_result.metadata, Metadata)

    def test_parse_glossary_has_entries(self, glossary_result):
        assert isinstance(glossary_result.entries, tuple)
        assert len(glossary_result.entries) == 266

    def test_parse_glossary_entries_are_glossary_entries(self, glossary_result):
        assert all(isinstance(entry, GlossaryEntry) for entry in glossary_result.entries)

    def test_parse_glossary_first_entry(self, glossary_result):
        first_entry = first(glossary_result.entries)
        assert first_entry.phrase == "Alien Registration Number"

    def test_parse_glossary_last_entry(self, glossary_result):
        last_entry = last(glossary_result.entries)
        assert last_entry.phrase == "Withdrawal"

    def test_metadata_creator_is_public_law(self, glossary_result):
        assert glossary_result.metadata.dcterms_creator == URL("https://public.law")

    def test_metadata_modified_is_today(self, glossary_result):
        assert glossary_result.metadata.dcterms_modified == today() 
