from datetime import date, datetime
from typing import Final, Iterable, Literal

from bs4 import BeautifulSoup, Tag
import typed_soup
from typed_soup import TypedSoup
from scrapy.http.response.html import HtmlResponse

from ...metadata import Metadata, Subject
from ...models.glossary import GlossaryEntry, GlossaryParseResult
from ...text import URL, LoCSubject, NonemptyString, WikidataTopic
from ...text import NonemptyString as String
from ...text import Sentence, normalize_nonempty

# Tag with empty string.
empty_tag: Final = Tag(None, None, "")


def parse_glossary(html: HtmlResponse) -> GlossaryParseResult:
    """
    The top-level, public function of this module. It performs the
    complete parse of the HTTP response.
    """
    metadata = _make_metadata(html)
    entries = _parse_entries(html)

    return GlossaryParseResult(metadata, entries)


def _make_metadata(html: HtmlResponse) -> Metadata:
    source_url = URL(html.url)
    subjects = (
        Subject(LoCSubject("sh85033571"), String("Courts")),
        Subject(WikidataTopic("Q41487"),  String("Court")),
        Subject(LoCSubject("sh85034086"), String("Criminal Procedure")),
        Subject(WikidataTopic("Q146071"), String("Criminal Procedure")),
    )

    return Metadata(
        dcterms_title=String("Criminal Procedure Rules Glossary"),
        dcterms_language="en",
        dcterms_coverage="GBR",
        # Info about original source
        dcterms_source=source_url,
        publiclaw_sourceModified=_parse_mod_date(html),
        publiclaw_sourceCreator=String("The National Archives"),
        dcterms_subject=subjects,
    )


def _parse_mod_date(response: HtmlResponse):
    """
    Parse the modification date from the HTML.
    """
    soup = BeautifulSoup(response.body, "html.parser")

    # Find first paragraph containing "in force at"
    matching_paragraph = next(
        (p for p in soup.find_all("p") if "in force at" in p.get_text()),
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
    return text.replace("’", "'").replace("‘", "'")


def _parse_entries(html: HtmlResponse) -> tuple[GlossaryEntry, ...]:
    """Parse entries from the HTML response."""
    soup = typed_soup.from_response(html)
    return tuple(
        _process_entry(phrase, defn)
        for phrase, defn in _raw_entries(soup)
        if phrase and defn
    )


def _process_entry(phrase: str, defn: str) -> GlossaryEntry:
    """Process a single glossary entry."""
    return GlossaryEntry(
        phrase=String(_capitalize_first(phrase)),
        definition=Sentence(_normalize_definition(defn)),
    )


def _raw_entries(soup: TypedSoup):
    """
    Extract raw entries from the soup.
    Returns an iterable of (phrase, definition) pairs.
    """
    if not (table := soup.find("table")):
        return

    rows = table.find_all("tr")[1:]  # Skip header row
    for row in [r for r in rows if len(r.find_all("td")) == 2]:
        cells = row.find_all("td")
        phrase = _cleanup_cell(cells[0])
        definition = _cleanup_cell(cells[1])

        yield (phrase, definition)


def _cleanup_cell(cell: TypedSoup) -> NonemptyString:
    """Cleanup a cell: strip whitespace and normalize apostrophes."""
    return normalize_nonempty(
        _normalize_apostrophes(cell.get_text(strip=True)))
