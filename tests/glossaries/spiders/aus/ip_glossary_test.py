import pytest
from datetime import date
from more_itertools import first, last
from scrapy.http.response.html import HtmlResponse

from public_law.shared.utils.dates import today
from public_law.shared.models.metadata import Subject
from public_law.shared.utils.text import URL, NonemptyString
from public_law.glossaries.spiders.aus.ip_glossary import IPGlossary

ORIG_URL = "https://www.ipaustralia.gov.au/tools-resources/ip-glossary"

@pytest.fixture(scope="module")
def spider():
    return IPGlossary()

@pytest.fixture(scope="module") 
def response():
    """Load the HTML fixture for Australia IP Glossary"""
    with open("tests/fixtures/aus/ip-glossary.html", "rb") as f:
        html_content = f.read()
    
    return HtmlResponse(
        url=ORIG_URL,
        body=html_content,
        encoding="utf-8",
    )

@pytest.fixture
def metadata(spider, response):
    """Cached metadata fixture to avoid repetitive calls"""
    return spider.get_metadata(response)


class TestGetMetadata:
    def test_title(self, metadata):
        assert metadata.dcterms_title == "IP Glossary"

    def test_source_url(self, metadata):
        assert metadata.dcterms_source == ORIG_URL

    def test_creator(self, metadata):
        assert metadata.dcterms_creator == "https://public.law"

    def test_coverage(self, metadata):
        assert metadata.dcterms_coverage == "AUS"

    def test_language(self, metadata):
        assert metadata.dcterms_language == "en"

    def test_source_creator(self, metadata):
        assert metadata.publiclaw_sourceCreator == "IP Australia"

    def test_source_modified_date(self, metadata):
        assert metadata.publiclaw_sourceModified == date(2021, 3, 26)

    def test_scrape_date(self, metadata):
        assert metadata.dcterms_modified == today()

    def test_subjects(self, metadata):
        assert metadata.dcterms_subject == (
            Subject(
                uri=URL("http://id.loc.gov/authorities/subjects/sh85067167"),
                rdfs_label=NonemptyString("Intellectual property"),
            ),
            Subject(
                uri=URL("https://www.wikidata.org/wiki/Q131257"),
                rdfs_label=NonemptyString("Intellectual property"),
            ),
        )


class TestSpiderIntegration:
    def test_spider_name(self, spider):
        assert spider.name == "aus_ip_glossary"

    def test_start_urls(self, spider):
        assert spider.start_urls == [
            "https://raw.githubusercontent.com/public-law/datasets/master/Australia/ip-glossary.html"
        ]

    def test_parse_glossary_integration(self, spider, response):
        """Test that parse_glossary method works with the new architecture"""
        result = spider.parse_glossary(response)
        
        # Test structure
        assert hasattr(result, 'metadata')
        assert hasattr(result, 'entries')
        
        # Test metadata
        assert result.metadata.dcterms_title == "IP Glossary"
        assert result.metadata.dcterms_coverage == "AUS"
        
        # Test entries  
        assert len(result.entries) == 53
        first_entry = first(result.entries)
        assert first_entry.phrase == "Assignee"
        
        last_entry = last(result.entries)
        assert last_entry.phrase == "Voluntary request for examination" 
