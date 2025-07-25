from typing import Iterable

from scrapy.http.response.html import HtmlResponse

from public_law.glossaries.models.glossary import GlossaryEntry
from public_law.shared.utils.text import NonemptyString as String, Sentence
from typed_soup import from_response, TypedSoup


def parse_entries(html: HtmlResponse) -> tuple[GlossaryEntry, ...]:
    """Parse entries from the HTML response."""
    soup = from_response(html)
    return tuple(
        _process_entry(phrase, defn)
        for phrase, defn in _raw_entries(soup)
        if phrase and defn
    )


def _process_entry(phrase: str, defn: str) -> GlossaryEntry:
    """Process a single glossary entry."""
    return GlossaryEntry(
        phrase=String(phrase),
        definition=Sentence(defn),
    )


def _raw_entries(soup: TypedSoup) -> Iterable[tuple[str, str]]:
    """
    Extract raw entries from the soup.
    Returns an iterable of (phrase, definition) pairs.
    """
    # Find all definition lists
    dls = soup("dl")
    if not dls:
        return

    for dl in dls:
        # Each dl contains dt/dd pairs
        dts = dl("dt")
        dds = dl("dd")

        # Ensure we have matching pairs
        if len(dts) != len(dds):
            continue

        for dt, dd in zip(dts, dds):
            # Get the phrase from the dt, handling both text and strong tags
            phrase_elem = dt.find("strong") or dt
            phrase = phrase_elem.get_text(strip=True)
            if phrase == "Date modified:":
                continue

            # Get the definition from the dd
            definition = dd.get_text(strip=True)

            if phrase and definition:
                yield (phrase, definition)
