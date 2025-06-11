import pytest
from scrapy.http.response.html import HtmlResponse

from public_law.glossaries.spiders.nzl.justice_glossary import JusticeGlossarySpider
from public_law.shared.models.metadata import Metadata, Subject
from public_law.shared.utils.text import URL, LoCSubject, NonemptyString

ORIG_URL = "https://www.justice.govt.nz/about/glossary/"

@pytest.fixture(scope="module")
def response():
    with open("tests/fixtures/nzl/justice-glossary.html", "rb") as f:
        html_content = f.read()
    return HtmlResponse(
        url=ORIG_URL,
        body=html_content,
        encoding="utf-8",
    )

@pytest.fixture
def spider():
    return JusticeGlossarySpider()

@pytest.fixture
def metadata(spider, response):
    return spider.get_metadata(response)

class TestGetMetadata:
    def test_returns_metadata_object(self, metadata):
        assert isinstance(metadata, Metadata)

    def test_dcterms_title(self, metadata):
        assert metadata.dcterms_title == "Glossary"

    def test_dcterms_language(self, metadata):
        assert metadata.dcterms_language == "en"

    def test_dcterms_coverage(self, metadata):
        assert metadata.dcterms_coverage == "NZL"

    def test_dcterms_source(self, metadata):
        assert metadata.dcterms_source == URL(ORIG_URL)

    def test_publiclaw_source_creator(self, metadata):
        assert metadata.publiclaw_sourceCreator == "New Zealand Ministry of Justice"

    def test_publiclaw_source_modified(self, metadata):
        assert metadata.publiclaw_sourceModified == "unknown"

    def test_dcterms_subject(self, metadata):
        assert isinstance(metadata.dcterms_subject, tuple)
        assert len(metadata.dcterms_subject) == 2
        subjects = metadata.dcterms_subject
        # Check Justice, Administration of subject
        justice_admin = next((s for s in subjects if str(s.rdfs_label) == "Justice, Administration of"), None)
        assert justice_admin is not None
        assert justice_admin.uri == LoCSubject("sh85071120")
        # Check Administration of justice subject
        admin_justice = next((s for s in subjects if str(s.rdfs_label) == "Administration of justice"), None)
        assert admin_justice is not None
        assert admin_justice.uri == URL("https://www.wikidata.org/wiki/Q16514399")

class TestSpiderIntegration:
    def test_spider_name(self, spider):
        assert spider.name == "nzl_justice_glossary"

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
        assert result.metadata.dcterms_title == "Glossary"
        assert result.metadata.dcterms_coverage == "NZL" 
