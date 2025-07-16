from typing import Optional
import re

from scrapy.http.response.html import HtmlResponse
from bs4 import BeautifulSoup

from public_law.legal_texts.models.statute import StatuteEntry
from public_law.shared.utils.html import from_response
from public_law.shared.utils.text import NonemptyString, normalize_whitespace, URI


def parse_statute_entries(response: HtmlResponse) -> tuple[StatuteEntry, ...]:
    """Parse statute entries from Georgia Code (LexisNexis) page.
    
    This parser handles the Official Code of Georgia Annotated as hosted by LexisNexis,
    following the landmark Georgia v. Public.Resource.Org Supreme Court victory (2020)
    which established public access rights to official legal materials.
    
    Args:
        response: HtmlResponse containing Georgia statute HTML from LexisNexis
        
    Returns:
        Tuple of StatuteEntry objects extracted from the page
    """
    soup = from_response(response)
    entries = []
    
    # Find the main statute content area - LexisNexis uses various container patterns
    statute_content = _find_statute_content(soup)
    
    if not statute_content:
        # Log for debugging but return empty tuple rather than crash
        print(f"Warning: No statute content found on {response.url}")
        return tuple()
    
    # Look for individual statute sections within the content
    sections = _find_statute_sections(statute_content)
    
    for section_element in sections:
        try:
            entry = _parse_single_section(section_element, response.url)
            if entry:
                entries.append(entry)
        except Exception as e:
            # Log but continue processing other sections
            print(f"Warning: Failed to parse Georgia section: {e}")
            continue
    
    return tuple(entries)


def _find_statute_content(soup: BeautifulSoup) -> Optional[BeautifulSoup]:
    """Find the main statute content area in LexisNexis HTML structure."""
    
    # Try multiple strategies for LexisNexis content discovery
    content_selectors = [
        # Common LexisNexis patterns
        'div[id*="content"]',
        'div[class*="content"]',
        'div[class*="statute"]',
        'div[class*="code"]',
        'main',
        'article',
        # Fallback patterns
        'div[class*="text"]',
        'div[id*="main"]',
        'div[class*="body"]',
    ]
    
    for selector in content_selectors:
        content = soup.select_one(selector)
        if content and content.get_text(strip=True):
            return content
    
    # Final fallback - use the entire body if no specific content area found
    body = soup.find('body')
    return body if body else soup


def _find_statute_sections(content_element: BeautifulSoup) -> list:
    """Find all statute section elements in the content."""
    
    # Georgia statutes typically use patterns like "16-1-1" (Title-Chapter-Section)
    # Try different strategies to find statute sections
    
    # Strategy 1: Look for elements containing Georgia section numbers
    sections_with_numbers = []
    for element in content_element.find_all(['div', 'section', 'article', 'p', 'h1', 'h2', 'h3', 'h4']):
        text = element.get_text(strip=True)
        if _contains_georgia_section_number(text):
            sections_with_numbers.append(element)
    
    if sections_with_numbers:
        return sections_with_numbers
    
    # Strategy 2: Look for headings that might contain section information
    headings = content_element.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    if headings:
        # For each heading, include the following content until the next heading
        full_sections = []
        for i, heading in enumerate(headings):
            section_content = [heading]
            current = heading.next_sibling
            next_heading = headings[i + 1] if i + 1 < len(headings) else None
            
            while current and current != next_heading:
                if hasattr(current, 'name') and current.name:  # Skip text nodes
                    section_content.append(current)
                current = current.next_sibling
                
            if len(section_content) > 1:  # Only include if there's content beyond the heading
                full_sections.append(section_content)
        
        if full_sections:
            return full_sections
    
    # Strategy 3: Look for common LexisNexis patterns
    lexis_patterns = [
        '[class*="section"]',
        '[class*="statute"]',
        '[id*="section"]',
        '[id*="statute"]',
    ]
    
    for pattern in lexis_patterns:
        elements = content_element.select(pattern)
        if elements:
            return elements
    
    # Strategy 4: Fallback - treat the entire content as one section if it contains Georgia patterns
    if _contains_georgia_section_number(content_element.get_text()):
        return [content_element]
    
    return []


def _contains_georgia_section_number(text: str) -> bool:
    """Check if text contains a Georgia statute section number pattern."""
    if not text:
        return False
    
    # Georgia uses patterns like:
    # "16-1-1", "O.C.G.A. § 16-1-1", "§ 16-1-1", "Section 16-1-1"
    georgia_patterns = [
        r'\b\d{1,2}-\d{1,3}-\d{1,4}\b',  # Basic format: 16-1-1
        r'O\.C\.G\.A\.\s*§\s*\d{1,2}-\d{1,3}-\d{1,4}',  # Official format
        r'§\s*\d{1,2}-\d{1,3}-\d{1,4}',  # Section symbol format
        r'Section\s+\d{1,2}-\d{1,3}-\d{1,4}',  # Word format
    ]
    
    for pattern in georgia_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    
    return False


def _parse_single_section(element, base_url: str) -> Optional[StatuteEntry]:
    """Parse a single Georgia statute section element into a StatuteEntry.
    
    Args:
        element: BeautifulSoup element or list of elements containing the statute section
        base_url: Base URL for the statute
        
    Returns:
        StatuteEntry object or None if parsing fails
    """
    # Handle case where element is a list (from strategy 2 above)
    if isinstance(element, list):
        section_elements = element
        heading = section_elements[0] if section_elements else None
        content_elements = section_elements[1:] if len(section_elements) > 1 else []
        full_text = ' '.join(el.get_text(strip=True) for el in section_elements if hasattr(el, 'get_text'))
    else:
        heading = element
        content_elements = []
        full_text = element.get_text(strip=True) if hasattr(element, 'get_text') else str(element)
    
    if not full_text or len(full_text.strip()) < 20:
        return None
    
    # Extract section number using Georgia patterns
    section_number = _extract_georgia_section_number(full_text)
    if not section_number:
        return None
    
    # Extract section title (if available)
    section_title = _extract_section_title(heading, full_text, section_number)
    
    # Extract the main statute text
    if content_elements:
        # Combine text from multiple elements, excluding the title
        section_text = ' '.join(el.get_text(strip=True) for el in content_elements if el.get_text(strip=True))
    else:
        # Get text from the main element, excluding the section number and title
        section_text = full_text
        if section_title and section_text.startswith(section_title):
            section_text = section_text[len(section_title):].strip()
        
        # Remove section number from the beginning if it's there
        section_number_pattern = f"^{re.escape(section_number)}[.\\s]*"
        section_text = re.sub(section_number_pattern, "", section_text).strip()
    
    if not section_text or len(section_text.strip()) < 10:
        return None
    
    # Parse Georgia citation to extract title and chapter information
    title_info, chapter_info = _parse_georgia_citation(section_number)
    
    # Create the official citation
    citation = f"O.C.G.A. § {section_number}"
    
    try:
        return StatuteEntry(
            title=NonemptyString(title_info or f"Title {section_number.split('-')[0]}"),
            chapter=NonemptyString(chapter_info) if chapter_info else None,
            section=NonemptyString(section_number),
            text=NonemptyString(normalize_whitespace(section_text)),
            citation=NonemptyString(citation),
            url=URI(base_url),
            effective_date=None,  # Could be extracted if available in LexisNexis
            last_updated=None,    # Could be extracted if available
            part=None,
            article=None,
            subsection=None,
        )
    except Exception as e:
        print(f"Warning: Failed to create Georgia StatuteEntry: {e}")
        return None


def _extract_georgia_section_number(text: str) -> Optional[str]:
    """Extract Georgia section number from text."""
    if not text:
        return None
    
    # Try different patterns to extract the section number
    patterns = [
        r'O\.C\.G\.A\.\s*§\s*(\d{1,2}-\d{1,3}-\d{1,4})',  # O.C.G.A. § 16-1-1
        r'§\s*(\d{1,2}-\d{1,3}-\d{1,4})',                 # § 16-1-1
        r'Section\s+(\d{1,2}-\d{1,3}-\d{1,4})',           # Section 16-1-1
        r'\b(\d{1,2}-\d{1,3}-\d{1,4})\b',                 # Just the number
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return None


def _extract_section_title(heading_element, full_text: str, section_number: str) -> Optional[str]:
    """Extract section title from heading element or full text."""
    
    # Try to get title from heading element
    if heading_element and hasattr(heading_element, 'get_text'):
        heading_text = heading_element.get_text(strip=True)
        if heading_text and section_number in heading_text:
            # Remove section number to get just the title
            title = re.sub(f".*{re.escape(section_number)}[.\\s]*", "", heading_text).strip()
            if title:
                return title
    
    # Try to extract title from the beginning of full text
    lines = full_text.split('\n')
    for line in lines[:3]:  # Check first few lines
        line = line.strip()
        if section_number in line:
            # Try to extract title part after section number
            title_match = re.search(f"{re.escape(section_number)}[.\\s]+(.+?)(?:\\.|$)", line)
            if title_match:
                title = title_match.group(1).strip()
                if title and len(title) > 5:  # Reasonable title length
                    return title
    
    return None


def _parse_georgia_citation(section_number: str) -> tuple[Optional[str], Optional[str]]:
    """Parse Georgia section number to extract title and chapter information.
    
    Georgia statutes are organized as Title-Chapter-Section (e.g., 16-1-1)
    where 16 is the title, 1 is the chapter, and 1 is the section.
    
    Returns:
        Tuple of (title_info, chapter_info)
    """
    if not section_number:
        return None, None
    
    match = re.match(r'^(\d{1,2})-(\d{1,3})-(\d{1,4})$', section_number)
    if match:
        title_num = match.group(1)
        chapter_num = match.group(2)
        section_num = match.group(3)
        
        title_info = f"Title {title_num}"
        chapter_info = f"Chapter {chapter_num}"
        
        return title_info, chapter_info
    
    return None, None