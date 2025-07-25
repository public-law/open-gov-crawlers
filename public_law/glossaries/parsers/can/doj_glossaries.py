import re
from typing import Any, TypeAlias

from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import Selector, SelectorList

from public_law.shared.exceptions import ParseException
from public_law.shared.models.metadata import Subject
from public_law.glossaries.models.glossary import GlossaryEntry
from public_law.shared.utils.text import (URL, LoCSubject, NonemptyString, Sentence,
                     capitalize_first_char, ensure_ends_with_period,
                     cleanup)

SelectorLike: TypeAlias = SelectorList | HtmlResponse

# TODO list from the spider:
#    https://www.justice.gc.ca/eng/rp-pr/cp-pm/aud-ver/2011/rc-pmr/01.html       # Crashes.
#    https://www.justice.gc.ca/eng/rp-pr/fl-lf/child-enfant/guide/glos.html


SUBJECTS: dict[str, tuple[Subject, Subject]] = {
    "https://www.justice.gc.ca/eng/fl-df/parent/mp-fdp/p11.html": (
        Subject(
            uri=LoCSubject("sh85034952"),
            rdfs_label=NonemptyString("Custody of children"),
        ),
        Subject(
            uri=URL("https://www.wikidata.org/wiki/Q638532"),
            rdfs_label=NonemptyString("Child custody"),
        ),
    ),
    "https://example.com/can_doj_glossary": (
        Subject(
            uri=LoCSubject("sh85034952"),
            rdfs_label=NonemptyString("Custody of children"),
        ),
        Subject(
            uri=URL("https://www.wikidata.org/wiki/Q638532"),
            rdfs_label=NonemptyString("Child custody"),
        ),
    ),
    "https://www.justice.gc.ca/eng/rp-pr/cp-pm/eval/rep-rap/12/lap-paj/p7g.html": (
        Subject(
            uri=LoCSubject("sh85075720"),
            rdfs_label=NonemptyString("Legal aid"),
        ),
        Subject(
            uri=URL("https://www.wikidata.org/wiki/Q707748"),
            rdfs_label=NonemptyString("Legal aid"),
        ),
    ),
    "https://www.justice.gc.ca/eng/rp-pr/cp-pm/eval/rep-rap/2019/elf-esc/p7.html": (
        Subject(
            uri=LoCSubject("sh85077662"),
            rdfs_label=NonemptyString("Litigation"),
        ),
        Subject(
            uri=URL("https://www.wikidata.org/wiki/Q107364261"),
            rdfs_label=NonemptyString("Litigation"),
        ),
    ),
    "https://www.justice.gc.ca/eng/rp-pr/fl-lf/famil/2003_5/glos.html": (
        Subject(
            uri=LoCSubject("sh98001029"),
            rdfs_label=NonemptyString("Parental alienation syndrome"),
        ),
        Subject(
            uri=URL("https://www.wikidata.org/wiki/Q1334131"),
            rdfs_label=NonemptyString("Parental alienation syndrome"),
        ),
    ),
    # "https://www.justice.gc.ca/eng/rp-pr/fl-lf/spousal-epoux/calc/aa.html": (
    #     Subject(
    #         uri=LoCSubject("sh85003572"),
    #         rdfs_label=NonemptyString("Alimony"),
    #     ),
    #     Subject(
    #         uri=URL("https://www.wikidata.org/wiki/Q368305"),
    #         rdfs_label=NonemptyString("Alimony"),
    #     ),
    # ),
    "https://www.justice.gc.ca/eng/rp-pr/fl-lf/spousal-epoux/spag/p18.html": (
        Subject(
            uri=LoCSubject("sh85003572"),
            rdfs_label=NonemptyString("Alimony"),
        ),
        Subject(
            uri=URL("https://www.wikidata.org/wiki/Q368305"),
            rdfs_label=NonemptyString("Alimony"),
        ),
    ),
    "https://laws-lois.justice.gc.ca/eng/glossary/": (
        Subject(
            uri=LoCSubject("sh98001459"),
            rdfs_label=NonemptyString("Law--Canada"),
        ),
        Subject(
            uri=URL("https://www.wikidata.org/wiki/Q181756"),
            rdfs_label=NonemptyString("Law of Canada"),
        ),
    ),
}


def configured_urls() -> list[str]:
    """All the URLs that have been properly set up with subjects."""
    return list(SUBJECTS.keys())


def parse_entries(html: HtmlResponse) -> tuple[GlossaryEntry, ...]:
    """Parse entries from the HTML response."""
    entries: list[GlossaryEntry] = []

    match html.selector.css("main dl"):
        case [first, *_]:
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
                    (result.replace("<dd>", "").replace(
                        "</dd>", "").replace("  ", " "))
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
                    ensure_ends_with_period(cleanup(definition))
                ),
            )
        )

    return tuple(entries)


def parse_name(html: SelectorLike) -> str:
    return fix_title_case(first_match(html, "title::text", "name"))


def first_match(node: SelectorLike, css: str, expected: str) -> str:
    match node.css(css).get():
        case str(result):
            return cleanup(result)
        case _:
            raise ParseException(
                f'Could not parse the {expected} using "{css}"')


def fix_title_case(text: str) -> str:
    return (
        text.replace("GLOSSARY OF LEGAL TERMS", "Glossary of Legal Terms")
        .replace("GLOSSARY OF TERMS", "Glossary of Terms")
        .replace("GLOSSARY", "Glossary")
    )
