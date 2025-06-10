from datetime import datetime
from typing import Final, Iterable

from bs4 import Tag
import typed_soup
from typed_soup import TypedSoup
from scrapy.http.response.html import HtmlResponse

from public_law.glossaries.models.glossary import GlossaryEntry
from public_law.shared.utils.text import NonemptyString, Sentence, cleanup

# Tag with empty string.
empty_tag: Final = Tag(None, None, "")


def parse_entries(html: HtmlResponse) -> tuple[GlossaryEntry, ...]:
    """Parse entries from the HTML response."""
    soup = typed_soup.from_response(html)
    return tuple(
        _process_entry(phrase, defn)
        for phrase, defn in _raw_entries(soup)
        if phrase and defn
    )


def parse_mod_date(response: HtmlResponse):
    """
    Parse the modification date from the HTML.
    """
    soup = typed_soup.from_response(response)

    # Find first paragraph containing "in force at"
    matching_paragraph = next(
        (p for p in soup("p") if "in force at" in p.get_text()),
        empty_tag
    )

    date_str = (
        matching_paragraph
        .get_text()
        .split("in force at")[1]
        .strip()
        .split(",")[0]
        .strip()
    )

    try:
        return datetime.strptime(date_str, "%d.%m.%Y").date()
    except ValueError:
        return "unknown"


def _capitalize_first(text: str) -> str:
    """Capitalize the first letter of a string."""
    if not text:
        return text
    return text[0].upper() + text[1:]


def _normalize_definition(text: str) -> str:
    """Normalize a definition: capitalize first letter and ensure it ends with a period."""
    text = text.strip()
    if not text:
        return text

    # Capitalize first letter
    text = _capitalize_first(text)

    # Replace semicolon with period if it's the last character
    if text.endswith(';'):
        text = text[:-1] + '.'

    # Ensure it ends with a period
    if not text.endswith('.'):
        text += '.'

    return text


def _normalize_apostrophes(text: str) -> str:
    """Normalize curly apostrophes to straight ones."""
    return text.replace("'", "'").replace("'", "'")


def _process_entry(phrase: str, defn: str) -> GlossaryEntry:
    """Process a single glossary entry."""
    return GlossaryEntry(
        phrase=NonemptyString(_capitalize_first(phrase)),
        definition=Sentence(_normalize_definition(defn)),
    )


def _raw_entries(soup: TypedSoup) -> Iterable[tuple[NonemptyString, NonemptyString]]:
    """
    Extract raw glossary entries from the soup.
    Returns an iterable of (phrase, definition) pairs.
    """
    tbody = soup("tbody")[0]
    for row in tbody("tr"):
        yield parse_row(row)


def parse_row(row: TypedSoup) -> tuple[NonemptyString, NonemptyString]:
    """Parse a row of the table."""
    phrase, definition = map(_cleanup_cell, row("td"))
    return phrase, definition


def _cleanup_cell(cell: TypedSoup) -> NonemptyString:
    """Cleanup a cell: strip whitespace and normalize apostrophes."""
    return cleanup(
        _normalize_apostrophes(cell.get_text(strip=True)))
