import pytest
from datetime import date
from scrapy.http.response.html import HtmlResponse

from public_law.glossaries.spiders.gbr.cpr_glossary import CPRGlossarySpider
from public_law.shared.models.metadata import Metadata, Subject
from public_law.shared.utils.text import URL, LoCSubject, WikidataTopic, NonemptyString

ORIG_URL = "https://www.legislation.gov.uk/uksi/2020/759/part/Glossary?view=plain"

@pytest.fixture(scope="module")
def response():
    """Load the HTML fixture for Great Britain CPR Glossary"""
    with open("tests/fixtures/gbr/cpr-glossary.html", "rb") as f:
        html_content = f.read()
    
    return HtmlResponse(
        url=ORIG_URL,
        body=html_content,
        encoding="utf-8",
    )

@pytest.fixture
def spider():
    return CPRGlossarySpider()

@pytest.fixture
def metadata(spider, response):
    return spider.get_metadata(response)


class TestGetMetadata:
    def test_returns_metadata_object(self, metadata):
        assert isinstance(metadata, Metadata)

    def test_dcterms_title(self, metadata):
        assert metadata.dcterms_title == "Criminal Procedure Rules Glossary"

    def test_dcterms_language(self, metadata):
        assert metadata.dcterms_language == "en"

    def test_dcterms_coverage(self, metadata):
        assert metadata.dcterms_coverage == "GBR"

    def test_dcterms_source(self, metadata):
        assert metadata.dcterms_source == URL(ORIG_URL)

    def test_publiclaw_source_creator(self, metadata):
        assert metadata.publiclaw_sourceCreator == "The National Archives"

    def test_publiclaw_source_modified(self, metadata):
        assert metadata.publiclaw_sourceModified == date(2020, 10, 5)

    def test_dcterms_subject(self, metadata):
        assert isinstance(metadata.dcterms_subject, tuple)
        assert len(metadata.dcterms_subject) == 4
        
        subjects = metadata.dcterms_subject
        
        # Check Courts subject
        courts_subject = next((s for s in subjects if str(s.rdfs_label) == "Courts"), None)
        assert courts_subject is not None
        assert courts_subject.uri == LoCSubject("sh85033571")
        
        # Check Court subject
        court_subject = next((s for s in subjects if str(s.rdfs_label) == "Court"), None)
        assert court_subject is not None
        assert court_subject.uri == WikidataTopic("Q41487")
        
        # Check Criminal Procedure subject
        criminal_proc_subject = next((s for s in subjects if str(s.rdfs_label) == "Criminal Procedure"), None)
        assert criminal_proc_subject is not None
        assert criminal_proc_subject.uri == LoCSubject("sh85034086")
        
        # Check Criminal Procedure Wikidata subject
        criminal_proc_wd_subject = next((s for s in subjects if str(s.rdfs_label) == "Criminal Procedure" and hasattr(s.uri, 'topic_id')), None)
        assert criminal_proc_wd_subject is not None
        assert criminal_proc_wd_subject.uri == WikidataTopic("Q146071")


class TestSpiderIntegration:
    def test_spider_name(self, spider):
        assert spider.name == "gbr_cpr_glossary"

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
        assert result.metadata.dcterms_title == "Criminal Procedure Rules Glossary"
        assert result.metadata.dcterms_coverage == "GBR" 
