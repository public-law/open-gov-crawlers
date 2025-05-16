from datetime import date
from typing import cast, List
from datetime import datetime

from bs4 import Tag
from scrapy.http.response.html import HtmlResponse

from ...metadata import Metadata, Subject
from ...models.glossary import GlossaryEntry, GlossaryParseResult
from ...text import URL, LoCSubject, WikidataTopic
from ...text import NonemptyString as String
from ...text import Sentence, ensure_ends_with_period, make_soup, normalize_nonempty


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


def _parse_mod_date(html: HtmlResponse) -> date:
    """
    Parse the modification date from the HTML.
    The date is in the commencement information section.
    """
    try:
        soup = make_soup(html)
        # Look for text containing "in force at"
        for p in soup.find_all("p"):
            if "in force at" in p.text:
                date_str = p.text.split("in force at")[
                    1].strip().split(",")[0].strip()
                return datetime.strptime(date_str, "%d.%m.%Y").date()
        return datetime.now().date()
    except Exception:
        return datetime.now().date()


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
    """
    Parse the glossary entries from the HTML response.
    The entries are in a table with two columns: phrase and definition.
    """
    soup = make_soup(html)
    table = soup.find("table")
    if not table or not isinstance(table, Tag):
        return tuple()

    entries: List[GlossaryEntry] = []
    for row in table.find_all("tr")[1:]:  # Skip header row
        cells = row.find_all("td")
        if len(cells) != 2:
            continue

        phrase = normalize_nonempty(
            _normalize_apostrophes(cells[0].text.strip()))
        definition = normalize_nonempty(
            _normalize_apostrophes(cells[1].text.strip()))

        if phrase and definition:
            entries.append(
                GlossaryEntry(
                    phrase=String(_capitalize_first(phrase)),
                    definition=Sentence(_normalize_definition(definition)),
                )
            )

    return tuple(entries)
