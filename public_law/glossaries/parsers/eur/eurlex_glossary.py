from datetime import date
from typing import Iterable, cast
from urllib.parse import urljoin

from scrapy.http.response.html import HtmlResponse

from public_law.shared.models.metadata import Metadata, Subject
from public_law.glossaries.models.glossary import GlossaryEntry, GlossaryParseResult
from public_law.shared.utils.text import (
    LoCSubject,
    NonemptyString as String,
    Sentence,
    URL,
    make_soup,
    normalize_whitespace,
    cleanup,
)


def parse_glossary(response: HtmlResponse) -> GlossaryParseResult:
    """Parse a single EUR-Lex glossary term page."""
    return GlossaryParseResult(
        metadata=_make_metadata(response),
        entries=_parse_entry(response),
    )


def _make_metadata(response: HtmlResponse) -> Metadata:
    """Create metadata for the EUR-Lex glossary."""
    return Metadata(
        dcterms_title=String("EUR-Lex Glossary of Summaries"),
        dcterms_language="en",
        dcterms_coverage="GBR",  # Using GBR as EUR not available in enum
        dcterms_source=String("https://eur-lex.europa.eu/summary/glossary.html"),
        dcterms_creator=String("Publications Office of the European Union"),
        publiclaw_sourceModified=date.today(),  # Current date since we don't have mod date
        publiclaw_sourceCreator=String("Publications Office of the European Union"),
        dcterms_subject=(
            Subject(
                uri=LoCSubject("sh85044899"),
                rdfs_label=String("European Union"),
            ),
            Subject(
                uri=URL("https://www.wikidata.org/wiki/Q458"),
                rdfs_label=String("European Union"),
            ),
        ),
    )


def _parse_entry(response: HtmlResponse) -> tuple[GlossaryEntry, ...]:
    """Parse a single glossary entry from an individual term page."""
    soup = make_soup(response)

    # Find the title in h1.ti-main
    title_elem = soup.find("h1", class_="ti-main")
    if not title_elem:
        return tuple()

    phrase = normalize_whitespace(title_elem.get_text().strip())

    # Find the definition in p.normal
    definition_elem = soup.find("p", class_="normal")
    if not definition_elem:
        return tuple()

    definition = normalize_whitespace(definition_elem.get_text().strip())

    if not phrase or not definition:
        return tuple()

    return (GlossaryEntry(
        phrase=String(phrase),
        definition=Sentence(definition),
    ),)


def parse_glossary_index(response: HtmlResponse) -> list[str]:
    """
    Parse the main glossary index page to extract all term URLs.
    This is a utility function to get all the individual glossary term URLs.
    """
    soup = make_soup(response)
    base_url = response.url

    # Find all links in the glossary content using CSS selector
    urls: list[str] = []
    # Use CSS selector to find all links with href containing glossary path
    for link in soup.select('a[href*="/legal-content/glossary/"]'):
        href_attr = link.get('href')
        if href_attr:
            full_url = urljoin(base_url, str(href_attr))
            urls.append(full_url)

    return list(set(urls))  # Remove duplicates 
