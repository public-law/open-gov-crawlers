from typing import Iterable

from scrapy.http.response.html import HtmlResponse

from ...metadata import Metadata, Subject
from ...models.glossary import GlossaryEntry, GlossaryParseResult
from ...text import URL, LoCSubject
from ...text import NonemptyString as String
from ...text import Sentence, normalize_nonempty
from typed_soup import from_response, TypedSoup


def parse_glossary(html: HtmlResponse) -> GlossaryParseResult:
    entries = _parse_entries(html)

    return GlossaryParseResult(
        metadata=Metadata(
            dcterms_title=String("Glossary"),
            dcterms_language="en",
            dcterms_coverage="NZL",
            # Info about original source
            dcterms_source=String(
                "https://www.justice.govt.nz/about/glossary/"),
            publiclaw_sourceModified="unknown",
            publiclaw_sourceCreator=String("New Zealand Ministry of Justice"),
            dcterms_subject=(
                Subject(
                    uri=LoCSubject("sh85071120"),
                    rdfs_label=String("Justice, Administration of"),
                ),
                Subject(
                    uri=URL("https://www.wikidata.org/wiki/Q16514399"),
                    rdfs_label=String("Administration of justice"),
                ),
            ),
        ),
        entries=entries,
    )


def _parse_entries(html: HtmlResponse) -> tuple[GlossaryEntry, ...]:
    """Parse entries from the HTML response."""
    soup = from_response(html)
    return tuple(
        _process_entry(phrase, defn)
        for phrase, defn in _raw_entries(soup)
        if defn is not None
    )


def _process_entry(phrase: TypedSoup, defn: TypedSoup) -> GlossaryEntry:
    """Process a single glossary entry."""
    return GlossaryEntry(
        phrase=normalize_nonempty(phrase.get_text()),
        definition=Sentence(defn.get_text()),
    )


def _raw_entries(soup: TypedSoup) -> Iterable[tuple[TypedSoup, TypedSoup | None]]:
    """
    Extract raw entries from the soup.
    Returns an iterable of (phrase, definition) pairs.
    """
    for p in soup.find_all("p"):
        children = p.children()
        if len(children) == 1 and children[0].tag_name() == "strong":
            phrase = children[0]
            defn = _get_next_sibling(phrase)
            yield (phrase, defn)


def _get_next_sibling(tag: TypedSoup) -> TypedSoup | None:
    parent = tag.parent()
    if not parent:
        return None
    sibling = parent.next_sibling()
    if sibling and sibling.tag_name() == "p":
        return sibling
    return None
