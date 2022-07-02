# pyright: reportUnknownMemberType=false

from dataclasses import dataclass
from datetime import date
import re
from typing import Any, TypeAlias

from scrapy.selector.unified import Selector
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import SelectorList

from public_law.text import capitalize_first_char, NonemptyString, normalize_whitespace
from public_law.metadata import Metadata


SelectorLike: TypeAlias = SelectorList | HtmlResponse


class ParseException(Exception):
    pass


@dataclass(frozen=True)
class GlossaryEntry:
    """Represents one term and its definition in a particular Glossary"""

    phrase: NonemptyString
    definition: NonemptyString


@dataclass(frozen=True)
class GlossarySourceParseResult:
    """All the info about a glossary source"""

    metadata: Metadata
    entries: list[GlossaryEntry]

    def __iter__(self):
        """Iterate over the entries in this glossary source.
        This customizes the produced dict to properly process the
        metadata.

        TODO: Figure out a way to convert this to a dict without the
        custom __iter__.
        """

        new_dict = {
            "metadata": dict(self.metadata),
            "entries": self.entries,
        }
        return iter(new_dict.items())


def parse_glossary(html: HtmlResponse) -> GlossarySourceParseResult:
    name = parse_name(html)
    pub_date = first_match(html, "dl#wb-dtmd time::text", "Pub. date")

    entries: list[GlossaryEntry] = []

    # dl_lists: list[Any] = html.css("main dl")
    # if len(dl_lists) == 0:
    #     raise ParseException("No DL lists found")

    # if isinstance(dl_lists[0], Selector):
    #     first_dl_list = dl_lists[0]
    # else:
    #     raise ParseException("Expected a <dl>")

    match html.css("main dl"):
        case [first, *_] if isinstance(
            first, Selector  # pylint:disable=used-before-assignment
        ):  # pyright: reportUnknownVariableType=false
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
                phrase = re.sub(r":$", "", result)
            case _:
                raise ParseException("Could not parse the phrase")

        entries.append(
            GlossaryEntry(
                phrase=NonemptyString(phrase),
                definition=NonemptyString(definition),
            )
        )

    url: str = html.url

    metadata = Metadata(
        dc_source=NonemptyString(url),
        dc_title=NonemptyString(name),
        dc_language="en",
        dcterms_coverage=NonemptyString("Canada"),
        publiclaw_sourceModified=date.fromisoformat(pub_date),
        publiclaw_sourceCreator=NonemptyString("Department of Justice Canada"),
    )

    return GlossarySourceParseResult(
        metadata=metadata,
        entries=entries,
    )


def parse_name(html: SelectorLike) -> str:
    return first_match(html, "title::text", "name")


def first_match(node: SelectorLike, css: str, expected: str) -> str:
    match node.css(css).get():
        case str(result):
            return normalize_whitespace(result)
        case _:
            raise ParseException(f'Could not parse the {expected} using "{css}"')
