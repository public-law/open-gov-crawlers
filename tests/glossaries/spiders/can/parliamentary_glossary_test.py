import pytest
from scrapy.http.response.html import HtmlResponse

from public_law.glossaries.spiders.can.parliamentary_glossary import ParliamentaryGlossary
from public_law.shared.models.metadata import Metadata, Subject
from public_law.shared.utils.text import URL, LoCSubject, NonemptyString
from public_law.shared.utils.dates import today

ORIG_URL = "https://lop.parl.ca/About/Parliament/Education/glossary-intermediate-students-e.html"

@pytest.fixture(scope="module")
def response():
    """Load the HTML fixture for Canada Parliamentary Glossary"""
    with open("tests/fixtures/can/parliamentary-glossary.html", "rb") as f:
        html_content = f.read()
    
    return HtmlResponse(
        url=ORIG_URL,
        body=html_content,
        encoding="utf-8",
    )

@pytest.fixture
def spider():
    return ParliamentaryGlossary()

@pytest.fixture
def metadata(spider, response):
    return spider.get_metadata(response)

class TestGetMetadata:
    def test_returns_metadata_object(self, metadata):
        assert isinstance(metadata, Metadata)

    def test_dcterms_title(self, metadata):
        assert metadata.dcterms_title == "Glossary of Parliamentary Terms for Intermediate Students"

    def test_dcterms_language(self, metadata):
        assert metadata.dcterms_language == "en"

    def test_dcterms_coverage(self, metadata):
        assert metadata.dcterms_coverage == "CAN"

    def test_dcterms_source(self, metadata):
        assert metadata.dcterms_source == URL(ORIG_URL)

    def test_publiclaw_source_modified(self, metadata):
        assert metadata.publiclaw_sourceModified == "unknown"

    def test_publiclaw_source_creator(self, metadata):
        assert metadata.publiclaw_sourceCreator == "Parliament of Canada"

    def test_dcterms_subject(self, metadata):
        assert isinstance(metadata.dcterms_subject, tuple)
        assert len(metadata.dcterms_subject) == 2
        
        subjects = metadata.dcterms_subject
        
        # Check Legislative bodies subject
        legislative_subject = next((s for s in subjects if str(s.rdfs_label) == "Legislative bodies"), None)
        assert legislative_subject is not None
        assert legislative_subject.uri == LoCSubject("sh85075807")
        
        # Check Parliament subject  
        parliament_subject = next((s for s in subjects if str(s.rdfs_label) == "Parliament"), None)
        assert parliament_subject is not None
        assert parliament_subject.uri == URL("https://www.wikidata.org/wiki/Q35749")

class TestSpiderIntegration:
    def test_spider_name(self, spider):
        assert spider.name == "can_parliamentary_glossary"

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
