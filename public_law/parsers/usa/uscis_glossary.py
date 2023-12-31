from typing import Any, Iterable

from scrapy.http.response.html import HtmlResponse
from toolz.functoolz import pipe  # type: ignore

from ...metadata import Metadata, Subject
from ...models.glossary import GlossaryEntry, GlossaryParseResult
from ...text import URL, LoCSubject, NonemptyString as String, WikidataTopic, make_soup
from ...text import (
    Sentence,
    capitalize_first_char,
    normalize_nonempty,
)
from public_law import text


def parse_glossary(html: HtmlResponse) -> GlossaryParseResult:
    """
    The top-level, public function of this module. It performs the
    complete parse of the HTTP response.
    """
    metadata = _make_metadata(html)
    entries  = tuple(_parse_entries(html))

    return GlossaryParseResult(metadata, entries)


def _make_metadata(html: HtmlResponse) -> Metadata:
    source_url = URL(html.url)

    subjects = (
                Subject(LoCSubject("sh85042790"), String("Emigration and immigration law")),
                Subject(WikidataTopic("Q231147"),  String("immigration law")), 
            )
    
    return Metadata(
            dcterms_title=String("USCIS Glossary"),
            dcterms_language="en",
            dcterms_coverage="USA",
            # Info about original source
            dcterms_source=source_url,
            publiclaw_sourceModified="unknown",
            publiclaw_sourceCreator=String("U.S. Citizenship and Immigration Services"),
            dcterms_subject=subjects,
        )


def _parse_entries(html: HtmlResponse) -> Iterable[GlossaryEntry]:
    """
    TODO: Refactor into a parent class. Write a way to pass lists of
    functions for cleaning up the definitions and phrases.
    """

    def cleanup_definition(defn: str) -> Sentence:
        assert isinstance(defn, str)

        return pipe(
            defn,
            normalize_nonempty,
            normalize_nonempty,
            capitalize_first_char,
            Sentence,
        ) # type: ignore

    def cleanup_phrase(phrase: str) -> String:
        assert isinstance(phrase, str)

        return text.pipe(
            phrase
            , normalize_nonempty
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
    soup    = make_soup(html)
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
