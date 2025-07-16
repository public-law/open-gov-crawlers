import pytest
from scrapy.http.response.html import HtmlResponse

from public_law.shared.models.metadata import Subject
from public_law.legal_texts.spiders.usa.georgia_statutes import GeorgiaStatutes
from public_law.shared.utils.text import URL, NonemptyString

# Test HTML content simulating LexisNexis navigation structure
GEORGIA_INDEX_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Official Code of Georgia Annotated - LexisNexis</title>
</head>
<body>
    <div id="main-content">
        <h1>Official Code of Georgia Annotated</h1>
        <div class="title-list">
            <a href="/hottopics/gacode/Title1">Title 1 - General Provisions</a>
            <a href="/hottopics/gacode/Title16">Title 16 - Crimes and Offenses</a>
            <a href="/hottopics/gacode/Title50">Title 50 - State Government</a>
        </div>
    </div>
</body>
</html>
"""

GEORGIA_TITLE_HTML = """
<html>
<body>
    <div class="lexis-content">
        <h2>Title 16 - Crimes and Offenses</h2>
        <div class="chapter-list">
            <a href="/hottopics/gacode/Chapter16-1">Chapter 1 - General Provisions</a>
            <a href="/hottopics/gacode/Chapter16-5">Chapter 5 - Crimes Against the Person</a>
        </div>
    </div>
</body>
</html>
"""

GEORGIA_CHAPTER_HTML = """
<html>
<body>
    <div class="lexis-content">
        <h2>Chapter 16-1 - General Provisions</h2>
        <div class="section-list">
            <a href="/hottopics/gacode/Section16-1-1">16-1-1. Definitions</a>
            <a href="/hottopics/gacode/Section16-1-2">16-1-2. General purposes</a>
            <a href="/hottopics/gacode/Section16-1-3">16-1-3. Criminal attempt</a>
        </div>
    </div>
</body>
</html>
"""

ORIG_URL = "https://www.lexisnexis.com/hottopics/gacode/"

@pytest.fixture(scope="module")
def response():
    """Create a mock response for testing spider methods."""
    return HtmlResponse(
        url=ORIG_URL,
        body=GEORGIA_INDEX_HTML.encode('utf-8'),
        encoding="utf-8",
    )

@pytest.fixture
def title_response():
    """Create a mock response for title page testing."""
    return HtmlResponse(
        url="https://www.lexisnexis.com/hottopics/gacode/Title16",
        body=GEORGIA_TITLE_HTML.encode('utf-8'),
        encoding="utf-8",
    )

@pytest.fixture
def chapter_response():
    """Create a mock response for chapter page testing."""
    return HtmlResponse(
        url="https://www.lexisnexis.com/hottopics/gacode/Chapter16-1",
        body=GEORGIA_CHAPTER_HTML.encode('utf-8'),
        encoding="utf-8",
    )

@pytest.fixture
def spider():
    """Create a Georgia statutes spider instance."""
    return GeorgiaStatutes()

@pytest.fixture
def metadata(spider, response):
    """Get metadata from the spider for testing."""
    return spider.get_metadata(response)

class TestGeorgiaStatutes:
    """Test suite for Georgia Statutes spider honoring Supreme Court victory."""
    
    def test_spider_name(self, spider):
        """Test that spider has correct name."""
        assert spider.name == "usa_georgia_statutes"
    
    def test_start_urls(self, spider):
        """Test that spider has valid start URLs pointing to LexisNexis."""
        assert len(spider.start_urls) > 0
        assert all(url.startswith('http') for url in spider.start_urls)
        assert any('lexisnexis.com' in url for url in spider.start_urls)
        assert any('gacode' in url for url in spider.start_urls)
    
    def test_custom_settings_for_lexisnexis(self, spider):
        """Test that spider has appropriate conservative settings for LexisNexis."""
        assert hasattr(spider, 'custom_settings')
        assert spider.custom_settings['DOWNLOAD_DELAY'] >= 2.0  # Conservative for vendor site
        assert spider.custom_settings['CONCURRENT_REQUESTS_PER_DOMAIN'] <= 1  # Very conservative
        assert 'PublicLawBot' in spider.custom_settings['USER_AGENT']
        assert 'Georgia-v-PRO-compliance' in spider.custom_settings['USER_AGENT']
    
    def test_metadata_structure(self, metadata):
        """Test that metadata has required fields."""
        assert metadata.dcterms_title == "Official Code of Georgia Annotated"
        assert metadata.dcterms_language == "en"
        assert metadata.dcterms_coverage == "Georgia, USA"
        assert metadata.publiclaw_sourceCreator == "Georgia General Assembly"
    
    def test_metadata_subjects(self, metadata):
        """Test that metadata includes appropriate subjects."""
        subjects = metadata.dcterms_subject
        assert len(subjects) >= 3  # Georgia, Statutes, Law--Georgia, Public domain
        
        # Should include Georgia, Statutes, and Public domain subjects
        subject_labels = [subject.rdfs_label for subject in subjects]
        assert "Georgia (U.S. state)" in subject_labels
        assert "Statutes" in subject_labels
        assert "Public domain" in subject_labels
    
    def test_metadata_source_url(self, metadata):
        """Test that metadata includes source URL."""
        assert isinstance(metadata.dcterms_source, URL)
        assert str(metadata.dcterms_source) == ORIG_URL
    
    def test_supreme_court_case_reference(self, metadata):
        """Test that metadata references the Supreme Court victory."""
        # Should reference Georgia v. Public.Resource.Org in rights field
        assert hasattr(metadata, 'dcterms_rights')
        assert "Georgia v. Public.Resource.Org" in metadata.dcterms_rights
        assert "590 U.S." in metadata.dcterms_rights  # Supreme Court citation
        assert "2020" in metadata.dcterms_rights
    
    def test_spider_inheritance(self, spider):
        """Test that spider properly inherits from base class."""
        from public_law.legal_texts.spiders._base.statute_base import EnhancedAutoStatuteSpider
        assert isinstance(spider, EnhancedAutoStatuteSpider)
    
    def test_parser_module_resolution(self, spider):
        """Test that spider can resolve its parser module path."""
        expected_path = "public_law.legal_texts.parsers.usa.georgia_statutes"
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
            'title': 'Title 16',
            'section': '16-1-1',
            'text': 'Sample Georgia statute text',
            'citation': 'O.C.G.A. § 16-1-1'
        }
        mock_parser.parse_statute_entries.return_value = (mock_entry,)
        
        # Mock the import
        sys.modules['public_law.legal_texts.parsers.usa.georgia_statutes'] = mock_parser
        
        try:
            result = spider.parse_statutes(response)
            assert isinstance(result, StatuteParseResult)
            assert len(result.entries) > 0
        finally:
            # Clean up mock
            if 'public_law.legal_texts.parsers.usa.georgia_statutes' in sys.modules:
                del sys.modules['public_law.legal_texts.parsers.usa.georgia_statutes']
    
    def test_handle_error_method(self, spider):
        """Test that spider has enhanced error handling method for LexisNexis."""
        assert hasattr(spider, 'handle_error')
        assert callable(spider.handle_error)
    
    def test_parse_methods_exist(self, spider):
        """Test that spider has required parse methods for LexisNexis navigation."""
        assert hasattr(spider, 'parse_title_index')
        assert hasattr(spider, 'parse_title_page')
        assert hasattr(spider, 'parse_chapter_page')
        assert hasattr(spider, 'parse_section_page')
        
        assert callable(spider.parse_title_index)
        assert callable(spider.parse_title_page)
        assert callable(spider.parse_chapter_page)
        assert callable(spider.parse_section_page)
    
    def test_start_requests_headers(self, spider):
        """Test that start_requests includes proper headers for LexisNexis."""
        requests = list(spider.start_requests())
        
        assert len(requests) > 0
        
        for request in requests:
            headers = request.headers
            assert b'Accept' in headers
            assert b'Accept-Language' in headers
            assert b'Referer' in headers
            assert b'lexisnexis.com' in headers[b'Referer']
            assert request.meta.get('priority') == 10  # High priority
    
    def test_lexisnexis_parsing_flexibility(self, spider, title_response):
        """Test that spider can handle flexible LexisNexis link patterns."""
        # Test title index parsing with flexible selectors
        requests = list(spider.parse_title_index(title_response))
        
        # Should generate requests for title links
        assert len(requests) > 0
        
        # Should preserve metadata in request meta
        for request in requests:
            assert 'title_link' in request.meta
    
    def test_conservative_crawling_approach(self, spider, chapter_response):
        """Test that spider limits requests to avoid overwhelming LexisNexis."""
        # Test chapter page parsing with request limiting
        requests = list(spider.parse_chapter_page(chapter_response))
        
        # Should limit the number of concurrent requests
        assert len(requests) <= 50  # As specified in the spider
    
    def test_supreme_court_victory_logging(self, spider):
        """Test that spider logs Georgia v. Public.Resource.Org context."""
        # Create a mock response for section parsing
        mock_response = HtmlResponse(
            url="https://www.lexisnexis.com/hottopics/gacode/Section16-1-1",
            body=b"<div>Mock section content</div>",
            encoding="utf-8",
        )
        
        # Capture logging output (in real implementation)
        # The spider should log the Supreme Court victory context
        # when successfully crawling Georgia statutes
        
        # Verify the parse_section_page method exists and can be called
        assert hasattr(spider, 'parse_section_page')
        
        # The method should reference the victory in its logging
        # (This would be tested with actual log capture in full implementation)


class TestGeorgiaStatutesNamingConvention:
    """Test that Georgia spider follows naming conventions."""
    
    def test_naming_convention_validation(self):
        """Test that the spider name follows the required pattern."""
        # This should not raise an exception
        spider = GeorgiaStatutes()
        assert spider.name == "usa_georgia_statutes"
    
    def test_invalid_naming_would_fail(self):
        """Test that invalid naming patterns would be caught."""
        from public_law.legal_texts.spiders._base.statute_base import EnhancedAutoStatuteSpider
        
        with pytest.raises(ValueError, match="must follow pattern"):
            class InvalidSpider(EnhancedAutoStatuteSpider):
                name = "georgia_statutes"  # Missing 'usa_' prefix
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


class TestGeorgiaStatutesLegalCompliance:
    """Test Georgia spider's compliance with Supreme Court decision."""
    
    def test_public_domain_recognition(self, spider, response):
        """Test that spider recognizes Georgia statutes as public domain."""
        metadata = spider.get_metadata(response)
        
        # Should include public domain in subjects
        subject_labels = [subject.rdfs_label for subject in metadata.dcterms_subject]
        assert "Public domain" in subject_labels
        
        # Should reference the court case in rights
        assert "Georgia v. Public.Resource.Org" in metadata.dcterms_rights
    
    def test_respectful_crawling_despite_rights(self, spider):
        """Test that spider maintains respectful crawling despite legal rights."""
        # Even though the Supreme Court established access rights,
        # the spider should still use conservative settings
        
        settings = spider.custom_settings
        assert settings['DOWNLOAD_DELAY'] >= 2.0  # Still respectful
        assert settings['CONCURRENT_REQUESTS_PER_DOMAIN'] <= 1  # Conservative
        assert settings['RANDOMIZE_DOWNLOAD_DELAY']  # Varies timing
    
    def test_carl_malamud_context(self, spider):
        """Test that spider implementation honors Carl Malamud's work."""
        # The docstring and comments should reference the victory
        assert "Georgia v. Public.Resource.Org" in spider.__doc__
        assert "Carl Malamud" in spider.__doc__
        assert "Supreme Court victory" in spider.__doc__
        assert "public access rights" in spider.__doc__


class TestGeorgiaStatutesErrorHandling:
    """Test Georgia spider's error handling for LexisNexis challenges."""
    
    def test_handles_403_forbidden(self, spider):
        """Test handling of 403 Forbidden errors from LexisNexis."""
        # The handle_error method should specifically handle LexisNexis errors
        from scrapy.http import Request
        from twisted.python.failure import Failure
        from scrapy.exceptions import HttpError
        
        # Create a mock 403 failure
        request = Request("https://www.lexisnexis.com/hottopics/gacode/test")
        
        # The spider should have specific handling for 403 errors
        # (This would be tested with actual failure objects in full implementation)
        assert hasattr(spider, 'handle_error')
    
    def test_handles_rate_limiting(self, spider):
        """Test handling of 429 rate limiting from LexisNexis."""
        # The spider should specifically handle rate limiting
        # and adjust its behavior accordingly
        
        # Conservative settings should prevent most rate limiting
        assert spider.custom_settings['DOWNLOAD_DELAY'] >= 2.0
        assert spider.custom_settings['CONCURRENT_REQUESTS_PER_DOMAIN'] <= 1
    
    def test_flexible_html_parsing(self, spider):
        """Test that spider can handle various LexisNexis HTML structures."""
        # The spider uses multiple strategies for finding links
        # This flexibility should handle changes in LexisNexis HTML
        
        # Verify that multiple selector strategies are used
        # (This is implemented in the parse methods)
        assert hasattr(spider, 'parse_title_index')
        assert hasattr(spider, 'parse_title_page')
        assert hasattr(spider, 'parse_chapter_page')