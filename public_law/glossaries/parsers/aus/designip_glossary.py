from typing import Tuple

from bs4 import Tag
from scrapy.http.response.html import HtmlResponse

from public_law.glossaries.models.glossary import GlossaryEntry
from public_law.shared.utils.text import (
    NonemptyString as String,
    Sentence,
    make_soup,
    normalize_whitespace,
    ensure_starts_with_capital,
)


def parse_entries(response: HtmlResponse) -> Tuple[GlossaryEntry, ...]:
    """
    Parse glossary entries from the Australia Design IP Glossary HTML response.
    
    Returns a tuple of GlossaryEntry objects with cleaned phrases and definitions.
    """
    soup = make_soup(response)

    def process_paragraph(p: Tag) -> GlossaryEntry | None:
        strong = p.find("strong")
        if not strong or not isinstance(strong, Tag):
            return None

        # Extract the phrase from the <strong> tag
        phrase = strong.get_text().strip()

        # Extract the definition by removing the <strong> tag and its contents
        strong.decompose()
        definition = normalize_whitespace(p.get_text().strip())
        # Remove em dash prefix if present
        definition = definition.removeprefix("– ")
        # Remove zero-width space characters (both Unicode and HTML entity)
        definition = definition.replace(
            "\u200b", "").replace("&ZeroWidthSpace;", "")
        # Ensure proper capitalization
        definition = ensure_starts_with_capital(definition)

        # Skip empty entries
        if not phrase or not definition:
            return None

        return GlossaryEntry(
            phrase=String(phrase),
            definition=Sentence(definition),
        )

    # Use list comprehension with filter to process paragraphs
    entries = [
        entry for p in soup("p")
        if isinstance(p, Tag)
        if (entry := process_paragraph(p)) is not None
    ]

    return tuple(entries)
