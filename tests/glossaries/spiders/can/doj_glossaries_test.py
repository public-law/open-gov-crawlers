import pytest
from datetime import date
from scrapy.http.response.html import HtmlResponse

from public_law.glossaries.spiders.can.doj_glossaries import DOJGlossariesSpider
from public_law.shared.models.metadata import Metadata
from public_law.shared.utils.text import URL, LoCSubject

# Test URLs from the original fixtures
P7G_URL = "https://www.justice.gc.ca/eng/rp-pr/cp-pm/eval/rep-rap/12/lap-paj/p7g.html"
P11_URL = "https://www.justice.gc.ca/eng/fl-df/parent/mp-fdp/p11.html"
GLOS_URL = "https://www.justice.gc.ca/eng/rp-pr/fl-lf/famil/2003_5/glos.html"
INDEX_URL = "https://laws-lois.justice.gc.ca/eng/glossary/"
P18_URL = "https://www.justice.gc.ca/eng/rp-pr/fl-lf/spousal-epoux/spag/p18.html"

@pytest.fixture(scope="module")
def p7g_response():
    """Load the HTML fixture for P7G DOJ Glossary"""
    with open("tests/fixtures/can/p7g.html", "rb") as f:
        html_content = f.read()
    
    return HtmlResponse(
        url=P7G_URL,
        body=html_content,
        encoding="utf-8",
    )

@pytest.fixture(scope="module")
def p11_response():
    """Load the HTML fixture for P11 DOJ Glossary"""
    with open("tests/fixtures/can/p11.html", "rb") as f:
        html_content = f.read()
    
    return HtmlResponse(
        url=P11_URL,
        body=html_content,
        encoding="utf-8",
    )

@pytest.fixture(scope="module")
def glos_response():
    """Load the HTML fixture for GLOS DOJ Glossary"""
    with open("tests/fixtures/can/glos.html", "rb") as f:
        html_content = f.read()
    
    return HtmlResponse(
        url=GLOS_URL,
        body=html_content,
        encoding="utf-8",
    )

@pytest.fixture(scope="module")
def index_response():
    """Load the HTML fixture for INDEX DOJ Glossary"""
    with open("tests/fixtures/can/index.html", "rb") as f:
        html_content = f.read()
    
    return HtmlResponse(
        url=INDEX_URL,
        body=html_content,
        encoding="utf-8",
    )

@pytest.fixture(scope="module")
def p18_response():
    """Load the HTML fixture for P18 DOJ Glossary"""
    with open("tests/fixtures/can/p18.html", "rb") as f:
        html_content = f.read()
    
    return HtmlResponse(
        url=P18_URL,
        body=html_content,
        encoding="utf-8",
    )

@pytest.fixture
def spider():
    return DOJGlossariesSpider()

@pytest.fixture
def p7g_metadata(spider, p7g_response):
    return spider.get_metadata(p7g_response)

@pytest.fixture
def p11_metadata(spider, p11_response):
    return spider.get_metadata(p11_response)

@pytest.fixture 
def glos_metadata(spider, glos_response):
    return spider.get_metadata(glos_response)

@pytest.fixture
def index_metadata(spider, index_response):
    return spider.get_metadata(index_response)

@pytest.fixture
def p18_metadata(spider, p18_response):
    return spider.get_metadata(p18_response)


class TestGetMetadata:
    def test_returns_metadata_object(self, p7g_metadata):
        assert isinstance(p7g_metadata, Metadata)

    def test_dcterms_language(self, p7g_metadata):
        assert p7g_metadata.dcterms_language == "en"

    def test_dcterms_coverage(self, p7g_metadata):
        assert p7g_metadata.dcterms_coverage == "CAN"

    def test_publiclaw_source_creator(self, p7g_metadata):
        assert p7g_metadata.publiclaw_sourceCreator == "Department of Justice Canada"

    def test_dcterms_source_p7g(self, p7g_metadata):
        assert p7g_metadata.dcterms_source == URL(P7G_URL)

    def test_dcterms_source_p11(self, p11_metadata):
        assert p11_metadata.dcterms_source == URL(P11_URL)

    def test_dcterms_title_p7g(self, p7g_metadata):
        assert p7g_metadata.dcterms_title == "Glossary of Legal Terms - Legal Aid Program Evaluation"

    def test_dcterms_title_glos(self, glos_metadata):
        assert glos_metadata.dcterms_title == "Glossary - Managing Contact Difficulties: A Child-Centred Approach (2003-FCY-5E)"

    def test_dcterms_title_index(self, index_metadata):
        assert index_metadata.dcterms_title == "Glossary"

    def test_dcterms_title_p18(self, p18_metadata):
        assert p18_metadata.dcterms_title == "Glossary of Terms - Spousal Support Advisory Guidelines July 2008"

    def test_publiclaw_source_modified_p7g(self, p7g_metadata):
        assert p7g_metadata.publiclaw_sourceModified == date(2022, 5, 13)

    def test_dcterms_subject_p7g(self, p7g_metadata):
        assert isinstance(p7g_metadata.dcterms_subject, tuple)
        assert len(p7g_metadata.dcterms_subject) == 2
        
        subjects = p7g_metadata.dcterms_subject
        
        # Check Legal aid subject 
        legal_aid_subject = next((s for s in subjects if str(s.rdfs_label) == "Legal aid"), None)
        assert legal_aid_subject is not None
        assert legal_aid_subject.uri == LoCSubject("sh85075720")

    def test_dcterms_subject_p11(self, p11_metadata):
        subjects = p11_metadata.dcterms_subject
        
        # Check Custody of children subject
        custody_subject = next((s for s in subjects if str(s.rdfs_label) == "Custody of children"), None)
        assert custody_subject is not None
        assert custody_subject.uri == LoCSubject("sh85034952")

    def test_dcterms_subject_glos(self, glos_metadata):
        subjects = glos_metadata.dcterms_subject
        
        # Check Parental alienation syndrome subject
        pas_subject = next((s for s in subjects if str(s.rdfs_label) == "Parental alienation syndrome"), None)
        assert pas_subject is not None
        assert pas_subject.uri == LoCSubject("sh98001029")


class TestSpiderIntegration:
    def test_spider_name(self, spider):
        assert spider.name == "can_doj_glossary"

    def test_start_urls(self, spider):
        # Should have all configured URLs
        assert len(spider.start_urls) > 0
        assert P7G_URL in spider.start_urls
        assert P11_URL in spider.start_urls
        assert GLOS_URL in spider.start_urls
        assert INDEX_URL in spider.start_urls
        assert P18_URL in spider.start_urls

    def test_inherits_from_enhanced_base(self, spider):
        from public_law.glossaries.spiders._base.enhanced_base import EnhancedAutoGlossarySpider
        assert isinstance(spider, EnhancedAutoGlossarySpider)

    def test_parse_glossary_integration_p7g(self, spider, p7g_response):
        result = spider.parse_glossary(p7g_response)
        
        # Test that we get a proper result with metadata and entries
        assert hasattr(result, 'metadata')
        assert hasattr(result, 'entries')
        assert len(result.entries) == 36
        assert result.metadata.dcterms_title == "Glossary of Legal Terms - Legal Aid Program Evaluation"

    def test_parse_glossary_integration_p11(self, spider, p11_response):
        result = spider.parse_glossary(p11_response)
        
        # Test that we get a proper result with metadata and entries
        assert hasattr(result, 'metadata')
        assert hasattr(result, 'entries')
        assert len(result.entries) > 0
        assert result.metadata.dcterms_coverage == "CAN" 
