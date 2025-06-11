import pytest
from more_itertools import first, last
from scrapy.http.response.html import HtmlResponse

from public_law.shared.utils.dates import today
from public_law.shared.models.metadata import Subject
from public_law.shared.utils.text import URL, NonemptyString
from public_law.glossaries.spiders.aus.dv_glossary import DVGlossary

GLOSSARY_URL = "https://www.aihw.gov.au/reports-data/behaviours-risk-factors/domestic-violence/glossary"

@pytest.fixture(scope="module")
def spider():
    return DVGlossary()

@pytest.fixture(scope="module") 
def response():
    """Load the HTML fixture for Australia DV Glossary"""
    with open("tests/fixtures/aus/dv-glossary.html", "rb") as f:
        html_content = f.read()
    
    return HtmlResponse(
        url=GLOSSARY_URL,
        body=html_content,
        encoding="utf-8",
    )

@pytest.fixture
def metadata(spider, response):
    """Cached metadata fixture to avoid repetitive calls"""
    return spider.get_metadata(response)


class TestGetMetadata:
    def test_title(self, metadata):
        assert metadata.dcterms_title == "Family, domestic and sexual violence glossary"

    def test_source_url(self, metadata):
        assert metadata.dcterms_source == GLOSSARY_URL

    def test_creator(self, metadata):
        assert metadata.dcterms_creator == "https://public.law"

    def test_coverage(self, metadata):
        assert metadata.dcterms_coverage == "AUS"

    def test_language(self, metadata):
        assert metadata.dcterms_language == "en"

    def test_source_modified_date(self, metadata):
        assert metadata.publiclaw_sourceModified == "unknown"

    def test_source_creator(self, metadata):
        assert metadata.publiclaw_sourceCreator == "Australian Institute of Health and Welfare"

    def test_scrape_date(self, metadata):
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


class TestSpiderIntegration:
    def test_spider_name(self, spider):
        assert spider.name == "aus_dv_glossary"

    def test_start_urls(self, spider):
        assert spider.start_urls == [GLOSSARY_URL]

    def test_parse_glossary_integration(self, spider, response):
        """Test that parse_glossary method works with the new architecture"""
        result = spider.parse_glossary(response)
        
        # Test structure
        assert hasattr(result, 'metadata')
        assert hasattr(result, 'entries')
        
        # Test metadata
        assert result.metadata.dcterms_title == "Family, domestic and sexual violence glossary"
        assert result.metadata.dcterms_coverage == "AUS"
        
        # Test entries  
        assert len(result.entries) == 37
        assert first(result.entries).phrase == "arranged marriage"
        
        last_entry = last(result.entries)
        assert last_entry.phrase == "vulnerable groups" 
