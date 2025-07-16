from typing import Iterable, List

from scrapy.http.response.html import HtmlResponse
from typed_soup import from_response, TypedSoup

from public_law.glossaries.models.glossary import GlossaryEntry
from public_law.shared.utils.text import NonemptyString as String, Sentence


def parse_entries(html: HtmlResponse) -> tuple[GlossaryEntry, ...]:
    """
    Parse glossary entries from the Australia DV Glossary HTML response.
    
    Returns a tuple of GlossaryEntry objects with cleaned phrases and definitions.
    """
    return tuple(__parse_entries(html))


def __parse_entries(html: HtmlResponse) -> Iterable[GlossaryEntry]:
    """Parse individual glossary entries with cleanup."""

    for phrase, defn in __raw_entries(html):
        # Clean up the phrase by removing trailing ": " and creating a NonemptyString
        cleaned_phrase = phrase.rstrip(": ")

        fixed_phrase = String(cleaned_phrase)
        fixed_definition = Sentence(defn)

        yield GlossaryEntry(fixed_phrase, fixed_definition)


def __raw_entries(response: HtmlResponse) -> Iterable[tuple[str, str]]:
    """
    Extract raw phrase/definition pairs from the HTML.
    
    The core extraction logic for this parser.
    """
    soup = from_response(response)
    paragraphs = soup("p")

    # Get all strong elements from paragraphs that have content
    strongs: List[TypedSoup] = []
    for p in paragraphs:
        strong = p.find("strong")
        if strong is not None and strong.string is not None:
            strongs.append(strong)

    # Filter out "Indigenous" entries
    strongs = [
        s for s in strongs
        if s.string != "Indigenous"
    ]

    # Extract phrase and definition
    for s in strongs:
        phrase = s.string or ""
        definition = s.get_content_after_element()

        yield (phrase, definition)
