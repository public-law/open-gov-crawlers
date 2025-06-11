import pytest
from scrapy.http.response.html import HtmlResponse

from public_law.glossaries.spiders.can.patents_glossary import PatentsGlossarySpider
from public_law.shared.models.metadata import Metadata, Subject
from public_law.shared.utils.text import LoCSubject, WikidataTopic, NonemptyString, URL

ORIG_URL = "https://ised-isde.canada.ca/site/canadian-intellectual-property-office/en/patents/glossary"

@pytest.fixture(scope="module")
def response():
    """Load the HTML fixture for Canada Patents Glossary"""
    with open("tests/fixtures/can/patents-glossary.html", "rb") as f:
        html_content = f.read()
    
    return HtmlResponse(
        url=ORIG_URL,
        body=html_content,
        encoding="utf-8",
    )

@pytest.fixture
def spider():
    return PatentsGlossarySpider()

@pytest.fixture
def metadata(spider, response):
    return spider.get_metadata(response)

class TestGetMetadata:
    def test_returns_metadata_object(self, metadata):
        assert isinstance(metadata, Metadata)

    def test_dcterms_title(self, metadata):
        assert metadata.dcterms_title == "Canadian Patent Glossary"

    def test_dcterms_language(self, metadata):
        assert metadata.dcterms_language == "en"

    def test_dcterms_coverage(self, metadata):
        assert metadata.dcterms_coverage == "CAN"

    def test_dcterms_source(self, metadata):
        assert metadata.dcterms_source == URL(ORIG_URL)

    def test_publiclaw_source_modified(self, metadata):
        assert metadata.publiclaw_sourceModified == "unknown"

    def test_publiclaw_source_creator(self, metadata):
        assert metadata.publiclaw_sourceCreator == "Canadian Intellectual Property Office"

    def test_dcterms_subject(self, metadata):
        assert isinstance(metadata.dcterms_subject, tuple)
        assert len(metadata.dcterms_subject) == 2
        
        subjects = metadata.dcterms_subject
        
        # Check Patents subject
        patents_subject = next((s for s in subjects if str(s.rdfs_label) == "Patents"), None)
        assert patents_subject is not None
        assert patents_subject.uri == LoCSubject("sh85098655")
        
        # Check Patent Law subject  
        patent_law_subject = next((s for s in subjects if str(s.rdfs_label) == "Patent Law"), None)
        assert patent_law_subject is not None
        assert patent_law_subject.uri == WikidataTopic("Q3039731")

class TestSpiderIntegration:
    def test_spider_name(self, spider):
        assert spider.name == "can_patents_glossary"

    def test_start_urls(self, spider):
        assert len(spider.start_urls) == 1
        assert spider.start_urls[0] == ORIG_URL

    def test_inherits_from_enhanced_base(self, spider):
        from public_law.shared.spiders.enhanced_base import EnhancedAutoGlossarySpider
        assert isinstance(spider, EnhancedAutoGlossarySpider)

    def test_parse_glossary_integration(self, spider, response):
        result = spider.parse_glossary(response)
        
        # Test that we get a proper result with metadata and entries
        assert hasattr(result, 'metadata')
        assert hasattr(result, 'entries')
        assert len(result.entries) > 0 
