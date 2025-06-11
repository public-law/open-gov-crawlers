from typing import Any, Iterable

from more_itertools import chunked
from scrapy.http.response.html import HtmlResponse
from toolz.functoolz import pipe  # type: ignore

from public_law.shared.utils import text
from public_law.glossaries.models.glossary import GlossaryEntry
from public_law.shared.utils.text import NonemptyString as String, Sentence


def parse_entries(html: HtmlResponse) -> tuple[GlossaryEntry, ...]:
    """
    Parse glossary entries from the IRL Courts Glossary HTML response.
    
    Returns a tuple of GlossaryEntry objects with cleaned phrases and definitions.
    """

    def cleanup_definition(definition: str) -> Sentence:
        return pipe(
            definition,
            text.cleanup,
            text.lstrip(":"),                                              # type: ignore
            text.ensure_ends_with_period,
            text.cleanup,
            text.capitalize_first_char,
            Sentence,
        )

    def cleanup_phrase(phrase: str) -> String:
        return text.pipe(
            phrase,
            text.rstrip(":"),                                             # type: ignore
            text.cleanup,
        )

    return tuple(
        GlossaryEntry(
            phrase=cleanup_phrase(phrase),
            definition=cleanup_definition(defn),
        )
        for phrase, defn in _raw_entries(html)
    )

def _raw_entries(html: HtmlResponse) -> Iterable[tuple[Any, Any]]:
    """
    Extract raw phrase/definition pairs from the HTML.
    
    The core extraction logic for this parser.
    """
    return chunked(
        html.xpath("//p/strong/parent::p/text() | //strong/text()").getall(), 2  # type: ignore
    )
