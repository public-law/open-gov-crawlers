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
    LoCSubject,
    URL,
    NonemptyString,
    Sentence,
    capitalize_first_char,
    ensure_ends_with_period,
    normalize_nonempty,
)

SelectorLike: TypeAlias = SelectorList | HtmlResponse

# TODO list from the spider:
#    https://www.justice.gc.ca/eng/rp-pr/cp-pm/aud-ver/2011/rc-pmr/01.html       # Crashes.
#    https://www.justice.gc.ca/eng/rp-pr/fl-lf/child-enfant/guide/glos.html


SUBJECTS: dict[str, tuple[Subject, Subject]] = {
    "https://www.justice.gc.ca/eng/fl-df/parent/mp-fdp/p11.html": (
        Subject(
            uri=LoCSubject("sh85034952"),  # type: ignore
            rdfs_label=NonemptyString("Custody of children"),
        ),
        Subject(
            uri=URL("https://www.wikidata.org/wiki/Q638532"),
            rdfs_label=NonemptyString("Child custody"),
        ),
    ),
    "https://www.justice.gc.ca/eng/rp-pr/cp-pm/eval/rep-rap/12/lap-paj/p7g.html": (
        Subject(
            uri=LoCSubject("sh85075720"),  # type: ignore
            rdfs_label=NonemptyString("Legal aid"),
        ),
        Subject(
            uri=URL("https://www.wikidata.org/wiki/Q707748"),
            rdfs_label=NonemptyString("Legal aid"),
        ),
    ),
    "https://www.justice.gc.ca/eng/rp-pr/cp-pm/eval/rep-rap/2019/elf-esc/p7.html": (
        Subject(
            uri=LoCSubject("sh85077662"),  # type: ignore
            rdfs_label=NonemptyString("Litigation"),
        ),
        Subject(
            uri=URL("https://www.wikidata.org/wiki/Q107364261"),
            rdfs_label=NonemptyString("Litigation"),
        ),
    ),
    "https://www.justice.gc.ca/eng/rp-pr/fl-lf/famil/2003_5/glos.html": (
        Subject(
            uri=LoCSubject("sh98001029"),  # type: ignore
            rdfs_label=NonemptyString("Parental alienation syndrome"),
        ),
        Subject(
            uri=URL("https://www.wikidata.org/wiki/Q1334131"),
            rdfs_label=NonemptyString("Parental alienation syndrome"),
        ),
    ),
    # "https://www.justice.gc.ca/eng/rp-pr/fl-lf/spousal-epoux/calc/aa.html": (
    #     Subject(
    #         uri=LoCSubject("sh85003572"),  # type: ignore
    #         rdfs_label=NonemptyString("Alimony"),
    #     ),
    #     Subject(
    #         uri=URL("https://www.wikidata.org/wiki/Q368305"),
    #         rdfs_label=NonemptyString("Alimony"),
    #     ),
    # ),
    "https://www.justice.gc.ca/eng/rp-pr/fl-lf/spousal-epoux/spag/p18.html": (
        Subject(
            uri=LoCSubject("sh85003572"),  # type: ignore
            rdfs_label=NonemptyString("Alimony"),
        ),
        Subject(
            uri=URL("https://www.wikidata.org/wiki/Q368305"),
            rdfs_label=NonemptyString("Alimony"),
        ),
    ),
    "https://laws-lois.justice.gc.ca/eng/glossary/": (
        Subject(
            uri=LoCSubject("sh98001459"),  # type: ignore
            rdfs_label=NonemptyString("Law--Canada"),
        ),
        Subject(
            uri=URL("https://www.wikidata.org/wiki/Q181756"),
            rdfs_label=NonemptyString("Law of Canada"),
        ),
    ),
}


def configured_urls() -> tuple[str]:
    """All the URLs that have been properly set up with subjects."""
    return tuple(SUBJECTS.keys())


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

    parsed_entries = tuple(entries)
    url = cast(str, html.url)

    match SUBJECTS.get(url):
        case tuple(subjects):
            dc_subject = subjects
        case None:
            raise ParseException(f"No subjects configured for {url}")

    metadata = Metadata(
        dcterms_source=URL(url),
        dcterms_title=NonemptyString(name),
        dcterms_language="en",
        dcterms_coverage="CAN",
        publiclaw_sourceModified=date.fromisoformat(pub_date),
        publiclaw_sourceCreator=NonemptyString("Department of Justice Canada"),
        publiclaw_readingEase=reading_ease(parsed_entries),
        dcterms_subject=dc_subject,
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
