from typing import Iterable

from scrapy.http.response.html import HtmlResponse

from public_law.glossaries.models.glossary import GlossaryEntry
from public_law.shared.utils.text import Sentence, cleanup
from typed_soup import from_response, TypedSoup


def parse_entries(html: HtmlResponse) -> tuple[GlossaryEntry, ...]:
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
        phrase=cleanup(phrase.get_text()),
        definition=Sentence(defn.get_text()),
    )


def _raw_entries(soup: TypedSoup) -> Iterable[tuple[TypedSoup, TypedSoup | None]]:
    """
    Extract raw entries from the soup.
    Returns an iterable of (phrase, definition) pairs.
    """
    for p in soup("p"):
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
