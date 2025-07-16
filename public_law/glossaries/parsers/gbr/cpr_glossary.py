from typing import Final, Iterable

from bs4 import Tag
import typed_soup
from typed_soup import TypedSoup
from scrapy.http.response.html import HtmlResponse

from public_law.glossaries.models.glossary import GlossaryEntry
from public_law.shared.utils.text import NonemptyString, Sentence, cleanup, normalize_apostrophes
from public_law.shared.utils.text import NonemptyString as String

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

def _capitalize_first(text: str) -> str:
    if not text:
        return text
    return text[0].upper() + text[1:]

def _normalize_definition(text: str) -> str:
    text = text.strip()
    if not text:
        return text
    text = _capitalize_first(text)
    if text.endswith(';'):
        text = text[:-1] + '.'
    if not text.endswith('.'):
        text += '.'
    return text

def _process_entry(phrase: str, defn: str) -> GlossaryEntry:
    return GlossaryEntry(
        phrase=String(_capitalize_first(phrase)),
        definition=Sentence(_normalize_definition(defn)),
    )

def _raw_entries(soup: TypedSoup) -> Iterable[tuple[NonemptyString, NonemptyString]]:
    tbody = soup("tbody")[0]
    for row in tbody("tr"):
        yield parse_row(row)

def parse_row(row: TypedSoup) -> tuple[NonemptyString, NonemptyString]:
    phrase, definition = map(_cleanup_cell, row("td"))
    return phrase, definition

def _cleanup_cell(cell: TypedSoup) -> NonemptyString:
    return cleanup(normalize_apostrophes(cell.get_text(strip=True)))
