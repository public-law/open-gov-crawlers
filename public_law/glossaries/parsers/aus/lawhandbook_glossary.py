from typing import List

from scrapy.http.response.html import HtmlResponse
from typed_soup import from_response

from public_law.glossaries.models.glossary import GlossaryEntry
from public_law.shared.utils.text import NonemptyString as String, Sentence


def parse_entries(html: HtmlResponse) -> tuple[GlossaryEntry, ...]:
    """
    Parse glossary entries from the Australia Law Handbook Glossary HTML response.
    
    Returns a tuple of GlossaryEntry objects with cleaned phrases and definitions.
    The entries are in a definition list (<dl>) with <dt> containing <span class="glossterm"> for terms 
    and <dd class="glossdef"> containing <p> for definitions.
    """
    entries: List[GlossaryEntry] = []
    soup = from_response(html)

    # Find all dt/dd pairs in the glossary
    dts = soup("dt")
    dds = soup("dd", class_="glossdef")

    for dt, dd in zip(dts, dds):
        # Extract the text content from the span.glossterm element
        phrase_elem = dt.find("span", class_="glossterm")
        if not phrase_elem:
            continue

        phrase = phrase_elem.get_text(strip=True)

        # Find the definition paragraph
        p_elem = dd.find("p")
        if not p_elem:
            continue

        definition = p_elem.get_text(strip=True)

        if phrase and definition:
            entries.append(
                GlossaryEntry(
                    phrase=String(phrase),
                    definition=Sentence(definition),
                )
            )

    # Do not sort; preserve source order
    return tuple(entries)
