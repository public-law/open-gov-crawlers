# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false

import re
from datetime import date
from typing import Any, TypeAlias, cast

from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import Selector, SelectorList

from ...exceptions import ParseException
from ...metadata import Metadata, Subject
from ...models.glossary import GlossaryEntry, GlossaryParseResult, reading_ease
from ...text import (
    URL,
    NonemptyString,
    Sentence,
    capitalize_first_char,
    ensure_ends_with_period,
    normalize_nonempty,
)

SelectorLike: TypeAlias = SelectorList | HtmlResponse


SUBJECTS: dict[str, tuple[Subject, Subject]] = {
    "https://www.justice.gc.ca/eng/fl-df/parent/mp-fdp/p11.html": (
        Subject(
            uri=URL("https://id.loc.gov/authorities/subjects/sh85034952"),
            rdfs_label=NonemptyString("Custody of children"),
        ),
        Subject(
            uri=URL("https://www.wikidata.org/wiki/Q638532"),
            rdfs_label=NonemptyString("Child custody"),
        ),
    ),
    "https://www.justice.gc.ca/eng/rp-pr/cp-pm/eval/rep-rap/12/lap-paj/p7g.html": (
        Subject(
            uri=URL("http://id.loc.gov/authorities/subjects/sh85075720"),
            rdfs_label=NonemptyString("Legal aid"),
        ),
        Subject(
            uri=URL("https://www.wikidata.org/wiki/Q707748"),
            rdfs_label=NonemptyString("Legal aid"),
        ),
    ),
}


def parse_glossary(html: HtmlResponse) -> GlossaryParseResult:
    name = parse_name(html)
    pub_date = first_match(html, "dl#wb-dtmd time::text", "Pub. date")

    entries: list[GlossaryEntry] = []

    match html.css("main dl"):
        case [first, *_] if isinstance(first, Selector):
            first_dl_list = first
        case _:
            raise ParseException("Expected a <dl>")

    prop: Any
    for prop in first_dl_list.xpath("dt"):
        assert isinstance(prop, Selector)

        match prop.xpath("./following-sibling::dd").get():
            case str(result):
                # Get the inner text and preserve inner HTML.
                definition = capitalize_first_char(
                    (result.replace("<dd>", "").replace("</dd>", "").replace("  ", " "))
                )
            case _:
                raise ParseException("Could not parse the definition")

        match prop.xpath("normalize-space(descendant::text())").get():
            case str(result):
                phrase = NonemptyString(re.sub(r":$", "", result))
            case _:
                raise ParseException("Could not parse the phrase")

        entries.append(
            GlossaryEntry(
                phrase=phrase,
                definition=Sentence(
                    ensure_ends_with_period(normalize_nonempty(definition))
                ),
            )
        )

    url = cast(str, html.url)
    parsed_entries = tuple(entries)

    metadata = Metadata(
        dcterms_source=NonemptyString(url),
        dcterms_title=NonemptyString(name),
        dcterms_language="en",
        dcterms_coverage="CAN",
        publiclaw_sourceModified=date.fromisoformat(pub_date),
        publiclaw_sourceCreator=NonemptyString("Department of Justice Canada"),
        publiclaw_readingEase=reading_ease(parsed_entries),
        dcterms_subject=SUBJECTS.get(url, tuple()),
    )

    return GlossaryParseResult(
        metadata=metadata,
        entries=parsed_entries,
    )


def parse_name(html: SelectorLike) -> str:
    return first_match(html, "title::text", "name")


def first_match(node: SelectorLike, css: str, expected: str) -> str:
    match node.css(css).get():
        case str(result):
            return normalize_nonempty(result)
        case _:
            raise ParseException(f'Could not parse the {expected} using "{css}"')
