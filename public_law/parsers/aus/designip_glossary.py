from datetime import date
from typing import Tuple

from bs4 import Tag
from scrapy.http.response.html import HtmlResponse

from public_law.metadata import Metadata, Subject
from public_law.models.glossary import GlossaryEntry, GlossaryParseResult
from public_law.text import (
    LoCSubject,
    NonemptyString as String,
    Sentence,
    URL,
    make_soup,
    normalize_whitespace,
    ensure_starts_with_capital,
)


def parse_glossary(response: HtmlResponse) -> GlossaryParseResult:
    """Parse the Design IP glossary from the HTML response."""
    return GlossaryParseResult(
        metadata=_make_metadata(response),
        entries=_parse_entries(response),
    )


def _make_metadata(response: HtmlResponse) -> Metadata:
    """Create metadata for the Design IP glossary."""
    return Metadata(
        dcterms_title=String("Design Examiners Manual Glossary"),
        dcterms_language="en",
        dcterms_coverage="AUS",
        dcterms_source=String(response.url),
        dcterms_creator=String("IP Australia"),
        publiclaw_sourceModified=date(2024, 10, 14),
        publiclaw_sourceCreator=String("IP Australia"),
        dcterms_subject=(
            Subject(
                uri=LoCSubject("sh85067167"),
                rdfs_label=String("Intellectual property"),
            ),
            Subject(
                uri=URL("https://www.wikidata.org/wiki/Q131257"),
                rdfs_label=String("Intellectual property"),
            ),
        ),
    )


def _parse_entries(response: HtmlResponse) -> Tuple[GlossaryEntry, ...]:
    """Parse glossary entries from the HTML response."""
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
        entry for p in soup.find_all("p")
        if isinstance(p, Tag)
        if (entry := process_paragraph(p)) is not None
    ]

    return tuple(entries)
