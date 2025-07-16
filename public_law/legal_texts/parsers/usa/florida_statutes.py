from typing import Optional

from scrapy.http.response.html import HtmlResponse
from bs4 import BeautifulSoup

from public_law.legal_texts.models.statute import StatuteEntry
from public_law.shared.utils.html import from_response
from public_law.shared.utils.text import NonemptyString, normalize_whitespace, URI


def parse_statute_entries(response: HtmlResponse) -> tuple[StatuteEntry, ...]:
    """Parse statute entries from Florida statutes page.
    
    This is a pure function that extracts StatuteEntry objects from the HTML
    response containing Florida statute content.
    
    Args:
        response: HtmlResponse containing Florida statute HTML
        
    Returns:
        Tuple of StatuteEntry objects extracted from the page
    """
    soup = from_response(response)
    entries = []
    
    # Find the main statute content area
    # Florida statutes typically have a specific structure we need to parse
    statute_content = soup.find('div', id='statute-content') or soup.find('main')
    
    if not statute_content:
        # Fallback: look for common statute indicators
        statute_content = soup.find('div', class_='statute') or soup
    
    # Look for individual statute sections
    sections = _find_statute_sections(statute_content)
    
    for section_element in sections:
        try:
            entry = _parse_single_section(section_element, response.url)
            if entry:
                entries.append(entry)
        except Exception as e:
            # Log but continue processing other sections
            # Note: In a real implementation, you'd use proper logging
            print(f"Warning: Failed to parse section: {e}")
            continue
    
    return tuple(entries)


def _find_statute_sections(content_element) -> list:
    """Find all statute section elements in the content."""
    # Try different strategies to find statute sections based on Florida's HTML structure
    
    # Strategy 1: Look for elements with section numbers
    sections = content_element.find_all('div', class_='statute-section')
    if sections:
        return sections
    
    # Strategy 2: Look for headings that contain section numbers
    sections = content_element.find_all(['h1', 'h2', 'h3', 'h4'], 
                                       string=lambda text: text and 'section' in text.lower())
    if sections:
        # For each heading, include the following content until the next heading
        full_sections = []
        for heading in sections:
            section_content = [heading]
            current = heading.next_sibling
            while current and current.name not in ['h1', 'h2', 'h3', 'h4']:
                if current.name:  # Skip text nodes
                    section_content.append(current)
                current = current.next_sibling
            full_sections.append(section_content)
        return full_sections
    
    # Strategy 3: Fallback - treat the entire content as one section
    return [content_element] if content_element else []


def _parse_single_section(element, base_url: str) -> Optional[StatuteEntry]:
    """Parse a single statute section element into a StatuteEntry.
    
    Args:
        element: BeautifulSoup element containing the statute section
        base_url: Base URL for the statute
        
    Returns:
        StatuteEntry object or None if parsing fails
    """
    # Handle case where element is a list (from strategy 2 above)
    if isinstance(element, list):
        section_elements = element
        heading = section_elements[0] if section_elements else None
        content_elements = section_elements[1:] if len(section_elements) > 1 else []
    else:
        section_elements = [element]
        heading = element
        content_elements = []
    
    # Extract section number and title
    section_info = _extract_section_info(heading)
    if not section_info:
        return None
    
    section_number, section_title = section_info
    
    # Extract the main text content
    if content_elements:
        # Combine text from multiple elements
        section_text = ' '.join(el.get_text(strip=True) for el in content_elements if el.get_text(strip=True))
    else:
        # Get text from the main element, excluding the header
        section_text = element.get_text(strip=True) if hasattr(element, 'get_text') else str(element)
        # Remove the section number/title from the beginning if it's there
        if section_title and section_text.startswith(section_title):
            section_text = section_text[len(section_title):].strip()
    
    if not section_text or len(section_text.strip()) < 10:
        return None
    
    # Extract hierarchical information from section number
    # Florida sections typically look like "768.28" (Title.Section)
    title_info, chapter_info = _parse_florida_citation(section_number)
    
    # Create the citation
    citation = f"Fla. Stat. § {section_number}"
    
    try:
        return StatuteEntry(
            title=NonemptyString(title_info or "Unknown Title"),
            chapter=NonemptyString(chapter_info) if chapter_info else None,
            section=NonemptyString(section_number),
            text=NonemptyString(normalize_whitespace(section_text)),
            citation=NonemptyString(citation),
            url=URI(base_url),
            effective_date=None,  # Could be extracted if available
            last_updated=None,    # Could be extracted if available
            part=None,
            article=None,
            subsection=None,
        )
    except Exception as e:
        print(f"Warning: Failed to create StatuteEntry: {e}")
        return None


def _extract_section_info(heading_element) -> Optional[tuple[str, str]]:
    """Extract section number and title from a heading element.
    
    Returns:
        Tuple of (section_number, section_title) or None if not found
    """
    if not heading_element or not hasattr(heading_element, 'get_text'):
        return None
    
    text = heading_element.get_text(strip=True)
    if not text:
        return None
    
    # Look for patterns like "768.28 Motor vehicle liability insurance"
    # or "Section 768.28. Motor vehicle liability insurance"
    import re
    
    # Pattern 1: Just number and title
    match = re.match(r'^(\d+\.\d+)\s+(.+)$', text)
    if match:
        return match.group(1), text
    
    # Pattern 2: "Section X.Y Title"
    match = re.match(r'^Section\s+(\d+\.\d+)\.?\s*(.*)$', text, re.IGNORECASE)
    if match:
        return match.group(1), text
    
    # Pattern 3: Just a section number
    match = re.match(r'^(\d+\.\d+)$', text)
    if match:
        return match.group(1), text
    
    return None


def _parse_florida_citation(section_number: str) -> tuple[Optional[str], Optional[str]]:
    """Parse Florida section number to extract title and chapter information.
    
    Florida statutes are organized as Title.Section (e.g., 768.28)
    where 768 is the chapter number.
    
    Returns:
        Tuple of (title_info, chapter_info)
    """
    import re
    
    match = re.match(r'^(\d+)\.(\d+)$', section_number)
    if match:
        chapter_num = match.group(1)
        section_num = match.group(2)
        
        # Florida organizes chapters into titles, but the mapping would need
        # to be looked up. For now, we'll use the chapter as the title.
        title_info = f"Chapter {chapter_num}"
        chapter_info = f"Chapter {chapter_num}"
        
        return title_info, chapter_info
    
    return None, None