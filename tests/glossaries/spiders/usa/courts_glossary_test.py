import pytest
from scrapy.http.response.html import HtmlResponse

from public_law.shared.utils.dates import today
from public_law.shared.models.metadata import Subject
from public_law.glossaries.spiders.usa.courts_glossary import CourtsGlossary
from public_law.shared.utils.text import URL, NonemptyString

ORIG_URL = "https://www.uscourts.gov/glossary"

@pytest.fixture(scope="module")
def response():
    """Create a mock response for testing spider methods."""
    with open("tests/fixtures/usa/courts-glossary.html", "rb") as f:
        html_content = f.read()
    
    return HtmlResponse(
        url=ORIG_URL,
        body=html_content,
        encoding="utf-8",
    )

@pytest.fixture
def spider():
    """Create a courts glossary spider instance."""
    return CourtsGlossary()


class TestCourtsGlossarySpiderMetadata:
    """Test the spider's get_metadata method."""
    
    def test_title(self, spider, response):
        metadata = spider.get_metadata(response)
        assert metadata.dcterms_title == "Glossary of Legal Terms"

    def test_source_url(self, spider, response):
        metadata = spider.get_metadata(response)
        assert metadata.dcterms_source == ORIG_URL

    def test_creator(self, spider, response):
        metadata = spider.get_metadata(response)
        assert metadata.dcterms_creator == "https://public.law"

    def test_coverage(self, spider, response):
        metadata = spider.get_metadata(response)
        assert metadata.dcterms_coverage == "USA"

    def test_source_modified_date(self, spider, response):
        metadata = spider.get_metadata(response)
        assert metadata.publiclaw_sourceModified == "unknown"

    def test_scrape_date(self, spider, response):
        metadata = spider.get_metadata(response)
        assert metadata.dcterms_modified == today()

    def test_subjects(self, spider, response):
        metadata = spider.get_metadata(response)
        assert metadata.dcterms_subject == (
            Subject(
                uri=URL("http://id.loc.gov/authorities/subjects/sh85033575"),
                rdfs_label=NonemptyString("Courts--United States"),
            ),
            Subject(
                uri=URL("https://www.wikidata.org/wiki/Q194907"),
                rdfs_label=NonemptyString("United States federal courts"),
            ),
        )


class TestCourtsGlossarySpiderIntegration:
    """Test the full spider integration (parse_glossary method)."""
    
    def test_parse_glossary_returns_correct_structure(self, spider, response):
        result = spider.parse_glossary(response)
        
        # Should have both metadata and entries
        assert hasattr(result, 'metadata')
        assert hasattr(result, 'entries')
        
        # Should have the right number of entries
        assert len(result.entries) == 237
        
        # Should have proper metadata
        assert result.metadata.dcterms_title == "Glossary of Legal Terms" 
