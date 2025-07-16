import pytest
from scrapy.http.response.html import HtmlResponse

from public_law.legal_texts.parsers.usa.georgia_statutes import (
    parse_statute_entries,
    _extract_georgia_section_number,
    _parse_georgia_citation,
    _contains_georgia_section_number,
    _parse_single_section,
    _find_statute_content
)
from public_law.legal_texts.models.statute import StatuteEntry

# Test HTML content simulating LexisNexis Georgia Code structure
SAMPLE_GEORGIA_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Official Code of Georgia Annotated - LexisNexis</title>
</head>
<body>
    <div id="main-content">
        <div class="statute-content">
            <h2>O.C.G.A. § 16-1-1. Definitions</h2>
            <p>As used in this title, the following terms shall have the meanings specified unless the context clearly indicates otherwise:</p>
            <p>(1) "Conduct" means an action or omission and its accompanying mental state.</p>
            <p>(2) "Criminal negligence" is an act or failure to act which demonstrates a willful, wanton, or reckless disregard for the safety of others who might reasonably be expected to be injured thereby.</p>
            
            <h2>16-1-2. General purposes</h2>
            <p>The general purposes of the provisions governing the definition of offenses are:</p>
            <p>(1) To forbid and prevent conduct that unjustifiably and inexcusably inflicts or threatens substantial harm to individual or public interests;</p>
            <p>(2) To subject to public control persons whose conduct indicates that they are disposed to commit crimes;</p>
        </div>
    </div>
</body>
</html>
"""

COMPLEX_GEORGIA_HTML = """
<html>
<body>
    <div class="lexis-content">
        <section class="code-section">
            <h3>§ 16-5-20. Simple assault</h3>
            <div class="section-text">
                <p>A person commits the offense of simple assault when he or she either:</p>
                <ul>
                    <li>(1) Attempts to commit a violent injury to the person of another; or</li>
                    <li>(2) Commits an act which places another in reasonable apprehension of immediately receiving a violent injury.</li>
                </ul>
            </div>
        </section>
        
        <section class="code-section">
            <h3>Section 16-5-21. Aggravated assault</h3>
            <div class="section-text">
                <p>A person commits the offense of aggravated assault when he or she assaults:</p>
                <p>(1) With intent to murder, to rape, or to rob;</p>
                <p>(2) With a deadly weapon or with any object, device, or instrument which, when used offensively against a person, is likely to or actually does result in serious bodily injury;</p>
            </div>
        </section>
    </div>
</body>
</html>
"""

MINIMAL_GEORGIA_HTML = """
<div>
    <p>O.C.G.A. § 16-1-3. Criminal attempt</p>
    <p>A person commits the offense of criminal attempt when, with intent to commit a specific crime, he performs any act which constitutes a substantial step toward the commission of that crime.</p>
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
    """Create a mock response with Georgia statute HTML."""
    return HtmlResponse(
        url="https://www.lexisnexis.com/hottopics/gacode/Default.asp?file=16-1-1",
        body=SAMPLE_GEORGIA_HTML.encode('utf-8'),
        encoding="utf-8",
    )

@pytest.fixture
def complex_response():
    """Create a mock response with complex Georgia statute content."""
    return HtmlResponse(
        url="https://www.lexisnexis.com/hottopics/gacode/Default.asp?file=16-5-20",
        body=COMPLEX_GEORGIA_HTML.encode('utf-8'),
        encoding="utf-8",
    )

@pytest.fixture
def minimal_response():
    """Create a mock response with minimal statute content."""
    return HtmlResponse(
        url="https://www.lexisnexis.com/hottopics/gacode/Default.asp?file=16-1-3",
        body=MINIMAL_GEORGIA_HTML.encode('utf-8'),
        encoding="utf-8",
    )

@pytest.fixture
def empty_response():
    """Create a mock response with no statute content."""
    return HtmlResponse(
        url="https://example.com/empty",
        body=EMPTY_HTML.encode('utf-8'),
        encoding="utf-8",
    )

class TestParseStatuteEntries:
    """Test the main parse_statute_entries function honoring Georgia v. Public.Resource.Org."""
    
    def test_parses_multiple_sections(self, response):
        """Test that parser can extract multiple Georgia statute sections."""
        entries = parse_statute_entries(response)
        
        assert len(entries) >= 2
        assert all(isinstance(entry, StatuteEntry) for entry in entries)
    
    def test_extracts_correct_section_numbers(self, response):
        """Test that correct Georgia section numbers are extracted."""
        entries = parse_statute_entries(response)
        
        section_numbers = {entry.section for entry in entries}
        assert "16-1-1" in section_numbers
        assert "16-1-2" in section_numbers
    
    def test_extracts_statute_text(self, response):
        """Test that Georgia statute text content is properly extracted."""
        entries = parse_statute_entries(response)
        
        # Find the definitions section
        section_16_1_1 = next((e for e in entries if e.section == "16-1-1"), None)
        assert section_16_1_1 is not None
        assert "conduct" in section_16_1_1.text.lower()
        assert "criminal negligence" in section_16_1_1.text.lower()
    
    def test_creates_proper_georgia_citations(self, response):
        """Test that proper Georgia statute citations are created."""
        entries = parse_statute_entries(response)
        
        for entry in entries:
            assert entry.citation.startswith("O.C.G.A. §")
            assert entry.section in entry.citation
    
    def test_extracts_title_and_chapter_info(self, response):
        """Test that title and chapter information is properly extracted."""
        entries = parse_statute_entries(response)
        
        for entry in entries:
            assert entry.title.startswith("Title")
            assert "16" in entry.title  # Title 16 for criminal law
            if entry.chapter:
                assert entry.chapter.startswith("Chapter")
    
    def test_handles_complex_content(self, complex_response):
        """Test parser with complex LexisNexis content."""
        entries = parse_statute_entries(complex_response)
        
        assert len(entries) >= 2
        
        # Check simple assault section
        simple_assault = next((e for e in entries if e.section == "16-5-20"), None)
        assert simple_assault is not None
        assert "simple assault" in simple_assault.text.lower()
        assert "violent injury" in simple_assault.text.lower()
        
        # Check aggravated assault section
        agg_assault = next((e for e in entries if e.section == "16-5-21"), None)
        assert agg_assault is not None
        assert "aggravated assault" in agg_assault.text.lower()
        assert "deadly weapon" in agg_assault.text.lower()
    
    def test_handles_minimal_content(self, minimal_response):
        """Test parser with minimal statute content."""
        entries = parse_statute_entries(minimal_response)
        
        assert len(entries) >= 1
        entry = entries[0]
        assert entry.section == "16-1-3"
        assert "criminal attempt" in entry.text.lower()
        assert entry.citation == "O.C.G.A. § 16-1-3"
    
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
    
    def test_honors_supreme_court_victory_context(self, response):
        """Test that parser operates in context of Georgia v. Public.Resource.Org victory."""
        # This test ensures the parser works with public domain Georgia code
        entries = parse_statute_entries(response)
        
        # Should successfully parse public domain Georgia statutes
        assert len(entries) > 0
        
        # All entries should have proper Georgia citations
        for entry in entries:
            assert "O.C.G.A." in entry.citation
            assert entry.url  # Should preserve source URL


class TestExtractGeorgiaSectionNumber:
    """Test the _extract_georgia_section_number helper function."""
    
    def test_extracts_basic_format(self):
        """Test extraction from basic Georgia format."""
        assert _extract_georgia_section_number("16-1-1") == "16-1-1"
        assert _extract_georgia_section_number("16-5-20") == "16-5-20"
        assert _extract_georgia_section_number("50-18-96") == "50-18-96"
    
    def test_extracts_official_format(self):
        """Test extraction from official O.C.G.A. format."""
        assert _extract_georgia_section_number("O.C.G.A. § 16-1-1") == "16-1-1"
        assert _extract_georgia_section_number("O.C.G.A. § 16-5-20") == "16-5-20"
        assert _extract_georgia_section_number("O.C.G.A.§16-1-1") == "16-1-1"
    
    def test_extracts_section_symbol_format(self):
        """Test extraction from section symbol format."""
        assert _extract_georgia_section_number("§ 16-1-1") == "16-1-1"
        assert _extract_georgia_section_number("§16-5-20") == "16-5-20"
    
    def test_extracts_section_word_format(self):
        """Test extraction from 'Section' word format."""
        assert _extract_georgia_section_number("Section 16-1-1") == "16-1-1"
        assert _extract_georgia_section_number("Section 16-5-20") == "16-5-20"
    
    def test_handles_invalid_input(self):
        """Test that function handles invalid input gracefully."""
        assert _extract_georgia_section_number("") is None
        assert _extract_georgia_section_number(None) is None
        assert _extract_georgia_section_number("no section here") is None
        assert _extract_georgia_section_number("16-1") is None  # Incomplete
        assert _extract_georgia_section_number("16-1-1-1") is None  # Too many parts
    
    def test_extracts_from_complex_text(self):
        """Test extraction from complex text with other content."""
        text = "This is a long paragraph about O.C.G.A. § 16-1-1 which defines terms."
        assert _extract_georgia_section_number(text) == "16-1-1"
        
        text = "See Section 16-5-20 for simple assault provisions."
        assert _extract_georgia_section_number(text) == "16-5-20"


class TestParseGeorgiaCitation:
    """Test the _parse_georgia_citation helper function."""
    
    def test_parses_standard_citation(self):
        """Test parsing of standard Georgia citation format."""
        title_info, chapter_info = _parse_georgia_citation("16-1-1")
        
        assert title_info == "Title 16"
        assert chapter_info == "Chapter 1"
    
    def test_parses_different_titles(self):
        """Test parsing citations from different titles."""
        title_info, chapter_info = _parse_georgia_citation("50-18-96")
        
        assert title_info == "Title 50"
        assert chapter_info == "Chapter 18"
        
        title_info, chapter_info = _parse_georgia_citation("7-1-1000")
        
        assert title_info == "Title 7"
        assert chapter_info == "Chapter 1"
    
    def test_handles_invalid_format(self):
        """Test handling of invalid citation formats."""
        title_info, chapter_info = _parse_georgia_citation("invalid")
        assert title_info is None
        assert chapter_info is None
        
        title_info, chapter_info = _parse_georgia_citation("16-1")
        assert title_info is None
        assert chapter_info is None
        
        title_info, chapter_info = _parse_georgia_citation("")
        assert title_info is None
        assert chapter_info is None


class TestContainsGeorgiaSectionNumber:
    """Test the _contains_georgia_section_number helper function."""
    
    def test_detects_basic_format(self):
        """Test detection of basic Georgia section numbers."""
        assert _contains_georgia_section_number("16-1-1")
        assert _contains_georgia_section_number("Contains 16-5-20 in text")
        assert _contains_georgia_section_number("50-18-96")
    
    def test_detects_official_format(self):
        """Test detection of official O.C.G.A. format."""
        assert _contains_georgia_section_number("O.C.G.A. § 16-1-1")
        assert _contains_georgia_section_number("According to O.C.G.A. § 16-5-20")
    
    def test_detects_section_symbol_format(self):
        """Test detection of section symbol format."""
        assert _contains_georgia_section_number("§ 16-1-1")
        assert _contains_georgia_section_number("See § 16-5-20")
    
    def test_detects_section_word_format(self):
        """Test detection of Section word format."""
        assert _contains_georgia_section_number("Section 16-1-1")
        assert _contains_georgia_section_number("Refer to Section 16-5-20")
    
    def test_rejects_non_georgia_patterns(self):
        """Test that non-Georgia patterns are rejected."""
        assert not _contains_georgia_section_number("768.28")  # Florida format
        assert not _contains_georgia_section_number("RCW 9.41.010")  # Washington format
        assert not _contains_georgia_section_number("no section here")
        assert not _contains_georgia_section_number("")
        assert not _contains_georgia_section_number(None)


class TestParseSingleSection:
    """Test the _parse_single_section helper function."""
    
    def test_parses_complete_section(self):
        """Test parsing a complete section element."""
        from bs4 import BeautifulSoup
        
        html = """
        <div>
            <h2>O.C.G.A. § 16-1-1. Definitions</h2>
            <p>As used in this title, the following terms shall have the meanings specified.</p>
            <p>This section provides important definitions for criminal law.</p>
        </div>
        """
        element = BeautifulSoup(html, 'html.parser').div
        
        entry = _parse_single_section(element, "https://example.com")
        
        assert entry is not None
        assert entry.section == "16-1-1"
        assert "definitions" in entry.text.lower()
        assert entry.citation == "O.C.G.A. § 16-1-1"
        assert entry.title == "Title 16"
        assert entry.chapter == "Chapter 1"
    
    def test_handles_list_input(self):
        """Test parsing when input is a list of elements."""
        from bs4 import BeautifulSoup
        
        html = """
        <h2>16-5-20. Simple assault</h2>
        <p>A person commits the offense of simple assault when he or she either:</p>
        <p>(1) Attempts to commit a violent injury to the person of another; or</p>
        <p>(2) Commits an act which places another in reasonable apprehension.</p>
        """
        soup = BeautifulSoup(html, 'html.parser')
        elements = [soup.h2] + soup.find_all('p')
        
        entry = _parse_single_section(elements, "https://example.com")
        
        assert entry is not None
        assert entry.section == "16-5-20"
        assert "simple assault" in entry.text.lower()
        assert "violent injury" in entry.text.lower()
        assert "reasonable apprehension" in entry.text.lower()
    
    def test_handles_insufficient_content(self):
        """Test that function returns None for insufficient content."""
        from bs4 import BeautifulSoup
        
        # Too short text
        html = "<div><h2>16-1-1</h2><p>Short</p></div>"
        element = BeautifulSoup(html, 'html.parser').div
        
        entry = _parse_single_section(element, "https://example.com")
        assert entry is None
    
    def test_handles_missing_section_info(self):
        """Test that function returns None when section info can't be extracted."""
        from bs4 import BeautifulSoup
        
        html = "<div><h2>No section number here</h2><p>Some longer text content here for testing purposes that should be long enough to pass the length check but has no Georgia section pattern.</p></div>"
        element = BeautifulSoup(html, 'html.parser').div
        
        entry = _parse_single_section(element, "https://example.com")
        assert entry is None