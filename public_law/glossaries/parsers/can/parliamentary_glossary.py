from scrapy.http.response.html import HtmlResponse

from public_law.glossaries.models.glossary import GlossaryEntry
from public_law.shared.utils.text import NonemptyString as String, Sentence
from public_law.shared.utils.text import make_soup, normalize_whitespace


def parse_entries(html: HtmlResponse) -> tuple[GlossaryEntry, ...]:
    """Parse entries from the HTML response."""
    soup = make_soup(html)

    # Skip the "Committees" entry.
    terms = [t for t in soup("dt") if t.text != 'Committees']

    # Fix the "Usher..." entry.
    raw_phrases = [t.text for t in terms]
    phrases = ["Usher of the Black Rod" if p.startswith(
        "Usher") else p for p in raw_phrases]

    raw_entries = zip(phrases, soup("dd"))

    return tuple(
        GlossaryEntry(
            phrase=String(normalize_whitespace(phrase)),
            definition=Sentence(defn.text),
        )
        for phrase, defn in raw_entries
    )
