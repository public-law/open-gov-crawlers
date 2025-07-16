import pytest
from scrapy.http.response.html import HtmlResponse

from public_law.shared.models.metadata import Subject
from public_law.legal_texts.spiders.usa.florida_statutes import FloridaStatutes
from public_law.shared.utils.text import URL, NonemptyString

# Test HTML content simulating Florida statutes structure
SAMPLE_FLORIDA_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Florida Statutes</title>
</head>
<body>
    <div id="statute-content">
        <h2>768.28 Motor vehicle liability insurance</h2>
        <p>Every owner or operator of a motor vehicle operated or used upon the public roads, streets, or highways of this state shall be financially responsible for death, bodily injury, or property damage caused by the negligent operation of such motor vehicle.</p>
        
        <h2>768.29 Automobile insurance coverage</h2>
        <p>The minimum limits of automobile insurance coverage required by this section are as follows: $10,000 for personal injury protection benefits and $10,000 for property damage liability.</p>
    </div>
</body>
</html>
"""

ORIG_URL = "http://www.leg.state.fl.us/Statutes/index.cfm?FuseAction=View&StatuteNumber=768.28"

@pytest.fixture(scope="module")
def response():
    """Create a mock response for testing spider methods."""
    return HtmlResponse(
        url=ORIG_URL,
        body=SAMPLE_FLORIDA_HTML.encode('utf-8'),
        encoding="utf-8",
    )

@pytest.fixture
def spider():
    """Create a Florida statutes spider instance."""
    return FloridaStatutes()

@pytest.fixture
def metadata(spider, response):
    """Get metadata from the spider for testing."""
    return spider.get_metadata(response)

class TestFloridaStatutes:
    """Test suite for Florida Statutes spider."""
    
    def test_spider_name(self, spider):
        """Test that spider has correct name."""
        assert spider.name == "usa_florida_statutes"
    
    def test_start_urls(self, spider):
        """Test that spider has valid start URLs."""
        assert len(spider.start_urls) > 0
        assert all(url.startswith('http') for url in spider.start_urls)
        assert any('leg.state.fl.us' in url for url in spider.start_urls)
    
    def test_custom_settings(self, spider):
        """Test that spider has appropriate custom settings."""
        assert hasattr(spider, 'custom_settings')
        assert spider.custom_settings['DOWNLOAD_DELAY'] >= 1.0
        assert spider.custom_settings['CONCURRENT_REQUESTS_PER_DOMAIN'] <= 2
    
    def test_metadata_structure(self, metadata):
        """Test that metadata has required fields."""
        assert metadata.dcterms_title == "Florida Statutes"
        assert metadata.dcterms_language == "en"
        assert metadata.dcterms_coverage == "Florida, USA"
        assert metadata.publiclaw_sourceCreator == "Florida Legislature"
    
    def test_metadata_subjects(self, metadata):
        """Test that metadata includes appropriate subjects."""
        subjects = metadata.dcterms_subject
        assert len(subjects) >= 2
        
        # Should include Florida and Statutes subjects
        subject_labels = [subject.rdfs_label for subject in subjects]
        assert "Florida" in subject_labels
        assert "Statutes" in subject_labels
    
    def test_metadata_source_url(self, metadata):
        """Test that metadata includes source URL."""
        assert isinstance(metadata.dcterms_source, URL)
        assert str(metadata.dcterms_source) == ORIG_URL
    
    def test_spider_inheritance(self, spider):
        """Test that spider properly inherits from base class."""
        from public_law.legal_texts.spiders._base.statute_base import EnhancedAutoStatuteSpider
        assert isinstance(spider, EnhancedAutoStatuteSpider)
    
    def test_parser_module_resolution(self, spider):
        """Test that spider can resolve its parser module path."""
        expected_path = "public_law.legal_texts.parsers.usa.florida_statutes"
        actual_path = spider._resolve_parser_module()
        assert actual_path == expected_path
    
    def test_parse_statutes_returns_correct_type(self, spider, response):
        """Test that parse_statutes returns StatuteParseResult."""
        from public_law.legal_texts.models.statute import StatuteParseResult
        
        # Mock the parser module to avoid import errors in tests
        import sys
        from unittest.mock import MagicMock, Mock
        
        # Create mock parser module
        mock_parser = MagicMock()
        mock_entry = Mock()
        mock_entry.asdict.return_value = {
            'title': 'Chapter 768',
            'section': '768.28',
            'text': 'Sample statute text',
            'citation': 'Fla. Stat. § 768.28'
        }
        mock_parser.parse_statute_entries.return_value = (mock_entry,)
        
        # Mock the import
        sys.modules['public_law.legal_texts.parsers.usa.florida_statutes'] = mock_parser
        
        try:
            result = spider.parse_statutes(response)
            assert isinstance(result, StatuteParseResult)
            assert len(result.entries) > 0
        finally:
            # Clean up mock
            if 'public_law.legal_texts.parsers.usa.florida_statutes' in sys.modules:
                del sys.modules['public_law.legal_texts.parsers.usa.florida_statutes']
    
    def test_handle_error_method(self, spider):
        """Test that spider has error handling method."""
        assert hasattr(spider, 'handle_error')
        assert callable(spider.handle_error)
    
    def test_parse_methods_exist(self, spider):
        """Test that spider has required parse methods."""
        assert hasattr(spider, 'parse_title_index')
        assert hasattr(spider, 'parse_title_page')
        assert hasattr(spider, 'parse_chapter_page')
        assert hasattr(spider, 'parse_section_page')
        
        assert callable(spider.parse_title_index)
        assert callable(spider.parse_title_page)
        assert callable(spider.parse_chapter_page)
        assert callable(spider.parse_section_page)


class TestFloridaStatutesNamingConvention:
    """Test that spider follows naming conventions."""
    
    def test_naming_convention_validation(self):
        """Test that the spider name follows the required pattern."""
        # This should not raise an exception
        spider = FloridaStatutes()
        assert spider.name == "usa_florida_statutes"
    
    def test_invalid_naming_would_fail(self):
        """Test that invalid naming patterns would be caught."""
        from public_law.legal_texts.spiders._base.statute_base import EnhancedAutoStatuteSpider
        
        with pytest.raises(ValueError, match="must follow pattern"):
            class InvalidSpider(EnhancedAutoStatuteSpider):
                name = "florida_statutes"  # Missing 'usa_' prefix
                start_urls = ["http://example.com"]
                
                def get_metadata(self, response):
                    pass
    
    def test_missing_name_would_fail(self):
        """Test that missing name attribute would be caught."""
        from public_law.legal_texts.spiders._base.statute_base import EnhancedAutoStatuteSpider
        
        with pytest.raises(TypeError, match="must define a 'name' class attribute"):
            class InvalidSpider(EnhancedAutoStatuteSpider):
                start_urls = ["http://example.com"]
                
                def get_metadata(self, response):
                    pass
    
    def test_missing_start_urls_would_fail(self):
        """Test that missing start_urls attribute would be caught."""
        from public_law.legal_texts.spiders._base.statute_base import EnhancedAutoStatuteSpider
        
        with pytest.raises(TypeError, match="must define a 'start_urls' class attribute"):
            class InvalidSpider(EnhancedAutoStatuteSpider):
                name = "usa_test_statutes"
                
                def get_metadata(self, response):
                    pass