import pytest
from scrapy.http.response.html import HtmlResponse

from public_law.legal_texts.parsers.usa.florida_statutes import (
    parse_statute_entries,
    _extract_section_info,
    _parse_florida_citation,
    _parse_single_section
)
from public_law.legal_texts.models.statute import StatuteEntry

# Test HTML content simulating Florida statutes structure
SAMPLE_FLORIDA_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Florida Statutes - Chapter 768</title>
</head>
<body>
    <div id="statute-content">
        <h2>768.28 Motor vehicle liability insurance</h2>
        <p>Every owner or operator of a motor vehicle operated or used upon the public roads, streets, or highways of this state shall be financially responsible for death, bodily injury, or property damage caused by the negligent operation of such motor vehicle.</p>
        <p>This section establishes the basic requirements for motor vehicle liability insurance in the state of Florida.</p>
        
        <h2>768.29 Automobile insurance coverage requirements</h2>
        <p>The minimum limits of automobile insurance coverage required by this section are as follows:</p>
        <ul>
            <li>$10,000 for personal injury protection benefits</li>
            <li>$10,000 for property damage liability</li>
        </ul>
        <p>These minimums may be adjusted by the legislature as deemed necessary.</p>
    </div>
</body>
</html>
"""

MINIMAL_FLORIDA_HTML = """
<div class="statute">
    <h3>Section 768.30. Test statute provision</h3>
    <p>This is a test statute with minimal content for testing purposes.</p>
</div>
"""

EMPTY_HTML = """
<html>
<body>
    <div>No statute content here</div>
</body>
</html>
"""

@pytest.fixture
def response():
    """Create a mock response with Florida statute HTML."""
    return HtmlResponse(
        url="http://www.leg.state.fl.us/Statutes/index.cfm?FuseAction=View&StatuteNumber=768.28",
        body=SAMPLE_FLORIDA_HTML.encode('utf-8'),
        encoding="utf-8",
    )

@pytest.fixture
def minimal_response():
    """Create a mock response with minimal statute content."""
    return HtmlResponse(
        url="http://www.leg.state.fl.us/Statutes/index.cfm?FuseAction=View&StatuteNumber=768.30",
        body=MINIMAL_FLORIDA_HTML.encode('utf-8'),
        encoding="utf-8",
    )

@pytest.fixture
def empty_response():
    """Create a mock response with no statute content."""
    return HtmlResponse(
        url="http://example.com/empty",
        body=EMPTY_HTML.encode('utf-8'),
        encoding="utf-8",
    )

class TestParseStatuteEntries:
    """Test the main parse_statute_entries function."""
    
    def test_parses_multiple_sections(self, response):
        """Test that parser can extract multiple statute sections."""
        entries = parse_statute_entries(response)
        
        assert len(entries) >= 2
        assert all(isinstance(entry, StatuteEntry) for entry in entries)
    
    def test_extracts_correct_section_numbers(self, response):
        """Test that correct section numbers are extracted."""
        entries = parse_statute_entries(response)
        
        section_numbers = {entry.section for entry in entries}
        assert "768.28" in section_numbers
        assert "768.29" in section_numbers
    
    def test_extracts_statute_text(self, response):
        """Test that statute text content is properly extracted."""
        entries = parse_statute_entries(response)
        
        # Find the first section and check its text
        section_768_28 = next((e for e in entries if e.section == "768.28"), None)
        assert section_768_28 is not None
        assert "motor vehicle" in section_768_28.text.lower()
        assert "financially responsible" in section_768_28.text.lower()
    
    def test_creates_proper_citations(self, response):
        """Test that proper Florida statute citations are created."""
        entries = parse_statute_entries(response)
        
        for entry in entries:
            assert entry.citation.startswith("Fla. Stat. §")
            assert entry.section in entry.citation
    
    def test_handles_minimal_content(self, minimal_response):
        """Test parser with minimal statute content."""
        entries = parse_statute_entries(minimal_response)
        
        assert len(entries) >= 1
        entry = entries[0]
        assert entry.section == "768.30"
        assert "test statute" in entry.text.lower()
    
    def test_handles_empty_content(self, empty_response):
        """Test parser gracefully handles empty content."""
        entries = parse_statute_entries(empty_response)
        
        # Should return empty tuple, not crash
        assert isinstance(entries, tuple)
        assert len(entries) == 0
    
    def test_returns_tuple(self, response):
        """Test that function returns a tuple as expected."""
        entries = parse_statute_entries(response)
        assert isinstance(entries, tuple)
    
    def test_all_entries_have_required_fields(self, response):
        """Test that all entries have required StatuteEntry fields."""
        entries = parse_statute_entries(response)
        
        for entry in entries:
            assert entry.title  # Should not be empty
            assert entry.section  # Should not be empty
            assert entry.text  # Should not be empty
            assert entry.citation  # Should not be empty
            assert entry.url  # Should not be empty
            assert entry.kind == "StatuteEntry"


class TestExtractSectionInfo:
    """Test the _extract_section_info helper function."""
    
    def test_extracts_basic_section_format(self):
        """Test extraction from basic 'Number Title' format."""
        from bs4 import BeautifulSoup
        
        html = "<h2>768.28 Motor vehicle liability insurance</h2>"
        element = BeautifulSoup(html, 'html.parser').h2
        
        result = _extract_section_info(element)
        assert result is not None
        section_num, title = result
        assert section_num == "768.28"
        assert title == "768.28 Motor vehicle liability insurance"
    
    def test_extracts_section_keyword_format(self):
        """Test extraction from 'Section X.Y Title' format."""
        from bs4 import BeautifulSoup
        
        html = "<h3>Section 768.28. Motor vehicle liability insurance</h3>"
        element = BeautifulSoup(html, 'html.parser').h3
        
        result = _extract_section_info(element)
        assert result is not None
        section_num, title = result
        assert section_num == "768.28"
    
    def test_extracts_number_only_format(self):
        """Test extraction from number-only format."""
        from bs4 import BeautifulSoup
        
        html = "<h2>768.28</h2>"
        element = BeautifulSoup(html, 'html.parser').h2
        
        result = _extract_section_info(element)
        assert result is not None
        section_num, title = result
        assert section_num == "768.28"
    
    def test_handles_invalid_input(self):
        """Test that function handles invalid input gracefully."""
        # Test with None
        assert _extract_section_info(None) is None
        
        # Test with empty element
        from bs4 import BeautifulSoup
        empty_element = BeautifulSoup("<div></div>", 'html.parser').div
        assert _extract_section_info(empty_element) is None
        
        # Test with non-matching text
        html = "<h2>Some random text</h2>"
        element = BeautifulSoup(html, 'html.parser').h2
        assert _extract_section_info(element) is None


class TestParseFLoridaCitation:
    """Test the _parse_florida_citation helper function."""
    
    def test_parses_standard_citation(self):
        """Test parsing of standard Florida citation format."""
        title_info, chapter_info = _parse_florida_citation("768.28")
        
        assert title_info == "Chapter 768"
        assert chapter_info == "Chapter 768"
    
    def test_parses_different_chapters(self):
        """Test parsing citations from different chapters."""
        title_info, chapter_info = _parse_florida_citation("316.001")
        
        assert title_info == "Chapter 316"
        assert chapter_info == "Chapter 316"
    
    def test_handles_invalid_format(self):
        """Test handling of invalid citation formats."""
        # Invalid format should return None values
        title_info, chapter_info = _parse_florida_citation("invalid")
        assert title_info is None
        assert chapter_info is None
        
        title_info, chapter_info = _parse_florida_citation("768")
        assert title_info is None
        assert chapter_info is None
    
    def test_handles_empty_input(self):
        """Test handling of empty input."""
        title_info, chapter_info = _parse_florida_citation("")
        assert title_info is None
        assert chapter_info is None


class TestParseSingleSection:
    """Test the _parse_single_section helper function."""
    
    def test_parses_complete_section(self):
        """Test parsing a complete section element."""
        from bs4 import BeautifulSoup
        
        html = """
        <div>
            <h2>768.28 Motor vehicle liability insurance</h2>
            <p>Every owner or operator of a motor vehicle must be financially responsible.</p>
        </div>
        """
        element = BeautifulSoup(html, 'html.parser').div
        
        entry = _parse_single_section(element, "http://example.com")
        
        assert entry is not None
        assert entry.section == "768.28"
        assert "financially responsible" in entry.text
        assert entry.citation == "Fla. Stat. § 768.28"
        assert entry.title == "Chapter 768"
    
    def test_handles_list_input(self):
        """Test parsing when input is a list of elements."""
        from bs4 import BeautifulSoup
        
        html = """
        <h2>768.28 Motor vehicle liability insurance</h2>
        <p>First paragraph of statute text.</p>
        <p>Second paragraph of statute text.</p>
        """
        soup = BeautifulSoup(html, 'html.parser')
        elements = [soup.h2, soup.find_all('p')[0], soup.find_all('p')[1]]
        
        entry = _parse_single_section(elements, "http://example.com")
        
        assert entry is not None
        assert entry.section == "768.28"
        assert "First paragraph" in entry.text
        assert "Second paragraph" in entry.text
    
    def test_handles_insufficient_content(self):
        """Test that function returns None for insufficient content."""
        from bs4 import BeautifulSoup
        
        # Too short text
        html = "<div><h2>768.28</h2><p>Short</p></div>"
        element = BeautifulSoup(html, 'html.parser').div
        
        entry = _parse_single_section(element, "http://example.com")
        assert entry is None
    
    def test_handles_missing_section_info(self):
        """Test that function returns None when section info can't be extracted."""
        from bs4 import BeautifulSoup
        
        html = "<div><h2>No section number here</h2><p>Some longer text content here for testing purposes.</p></div>"
        element = BeautifulSoup(html, 'html.parser').div
        
        entry = _parse_single_section(element, "http://example.com")
        assert entry is None