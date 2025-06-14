from typing import Any, Iterable

from scrapy.http.response.html import HtmlResponse
from toolz.functoolz import pipe  # type: ignore

from ...models.glossary import GlossaryEntry

from ....shared.utils           import text
from ....shared.utils.text      import NonemptyString as String


def parse_entries(html: HtmlResponse) -> tuple[GlossaryEntry, ...]:
    """
    Parse glossary entries from HTML response.
    Returns a tuple of GlossaryEntry objects without metadata.
    """
    return tuple(_parse_entries(html))


def _parse_entries(html: HtmlResponse) -> Iterable[GlossaryEntry]:
    """
    TODO: Refactor into a parent class. Write a way to pass lists of
    functions for cleaning up the definitions and phrases.
    """

    def cleanup_definition(defn: str) -> text.Sentence:
        assert isinstance(defn, str)

        return pipe(
            defn,
            text.cleanup,
            text.cleanup,
            text.capitalize_first_char,
            text.Sentence,
        ) # type: ignore

    def cleanup_phrase(phrase: str) -> String:
        assert isinstance(phrase, str)

        return text.pipe(
            phrase
            , text.cleanup
        )
    
    for phrase, defn in _raw_entries(html):
        assert isinstance(phrase, str)
        assert isinstance(defn, str)
        
        yield GlossaryEntry(
            phrase=cleanup_phrase(phrase),
            definition=cleanup_definition(defn),
        )


def _raw_entries(html: HtmlResponse) -> Iterable[tuple[Any, Any]]:
    """
    The core of this parser.

    TODO: Refactor all the glossary parsers to need only this function.
    """
    soup    = text.make_soup(html)
    phrases = [d.string for d in soup.select('div.accordion__header')]
    phrases = [maybe_fix(p) for p in phrases]

    defn_divs = [list(d.children) for d in soup.select('div.accordion__panel')]
    cleaned_up_definitions: list[str] = []
    for div in defn_divs:
        cleaned_up = "\n".join([str(s) for s in div if str(s) != '\n'])
        cleaned_up_definitions.append(cleaned_up)

    return zip(phrases, cleaned_up_definitions) 


def maybe_fix(phrase: str|None) -> str|None:
    """
    Some phrases have extra whitespace at the beginning.
    """
    if phrase is None:
        return None

    FIXED = "Alien Registration Number"

    return FIXED if FIXED in phrase else phrase
