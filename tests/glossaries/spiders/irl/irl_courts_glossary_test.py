import pytest
from more_itertools import first, last
from scrapy.http.response.html import HtmlResponse

from public_law.shared.utils.dates import today
from public_law.shared.models.metadata import Subject
from public_law.shared.utils.text import URL, NonemptyString
from public_law.glossaries.spiders.irl.courts_glossary import IRLCourtsGlossary


@pytest.fixture(scope="module")
def spider():
    return IRLCourtsGlossary()

@pytest.fixture(scope="module") 
def response():
    """Load the HTML fixture for IRL Courts Glossary"""
    with open("tests/fixtures/irl/courts-glossary.html", "rb") as f:
        html_content = f.read()
    
    return HtmlResponse(
        url="https://www.courts.ie/glossary",
        body=html_content,
        encoding="utf-8",
    )

@pytest.fixture
def metadata(spider, response):
    """Cached metadata fixture to avoid repetitive calls"""
    return spider.get_metadata(response)


class TestGetMetadata:
    def test_title(self, metadata):
        assert metadata.dcterms_title == "Glossary of Legal Terms"

    def test_source_url(self, metadata):
        assert metadata.dcterms_source == "https://www.courts.ie/glossary"

    def test_creator(self, metadata):
        assert metadata.dcterms_creator == "https://public.law"

    def test_coverage(self, metadata):
        assert metadata.dcterms_coverage == "IRL"

    def test_language(self, metadata):
        assert metadata.dcterms_language == "en"

    def test_source_modified_date(self, metadata):
        assert metadata.publiclaw_sourceModified == "unknown"

    def test_source_creator(self, metadata):
        assert metadata.publiclaw_sourceCreator == "The Courts Service of Ireland"

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


class TestSpiderIntegration:
    def test_spider_name(self, spider):
        assert spider.name == "irl_courts_glossary"

    def test_start_urls(self, spider):
        assert spider.start_urls == ["https://www.courts.ie/glossary"]

    def test_parse_glossary_integration(self, spider, response):
        """Test that parse_glossary method works with the new architecture"""
        result = spider.parse_glossary(response)
        
        # Test structure
        assert hasattr(result, 'metadata')
        assert hasattr(result, 'entries')
        
        # Test metadata
        assert result.metadata.dcterms_title == "Glossary of Legal Terms"
        assert result.metadata.dcterms_coverage == "IRL"
        
        # Test entries  
        assert len(result.entries) == 43
        assert first(result.entries).definition == "A written statement made on oath."
        
        last_entry = last(result.entries)
        assert last_entry.phrase == "Supervision order" 
