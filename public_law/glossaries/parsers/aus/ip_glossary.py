from scrapy.http.response.html import HtmlResponse

from public_law.glossaries.models.glossary import GlossaryEntry
from public_law.shared.utils.text import NonemptyString as String, Sentence, make_soup, cleanup


def parse_entries(html: HtmlResponse) -> tuple[GlossaryEntry, ...]:
    """
    Parse glossary entries from the Australia IP Glossary HTML response.
    
    Returns a tuple of GlossaryEntry objects with cleaned phrases and definitions.
    """
    soup = make_soup(html)
    raw_entries = zip(soup("dt"), soup("dd"))

    return tuple(
        GlossaryEntry(
            phrase=cleanup(phrase.text),
            definition=Sentence(defn.text),
        )
        for phrase, defn in raw_entries
    )
