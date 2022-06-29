# pyright: reportUnknownMemberType=false


from typing import Any, List, NamedTuple, Union

from scrapy.selector.unified import Selector
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import SelectorList

from public_law.text import NonemptyString, normalize_whitespace
from public_law.dates import todays_date


class ParseException(Exception):
    pass


class GlossaryEntry(NamedTuple):
    """Represents one term and its definition in a particular Glossary"""

    phrase: NonemptyString
    definition: NonemptyString

    def __repr__(self) -> str:
        return self._asdict().__repr__()


class GlossarySourceParseResult(NamedTuple):
    """All the info about a glossary source"""

    source_url: str
    name: str
    author: str
    pub_date: str
    scrape_date: str
    entries: List[GlossaryEntry]


def parse_glossary(html: HtmlResponse) -> GlossarySourceParseResult:
    main: SelectorList = html.css("main")

    name = parse_name(main)
    pub_date = first(html, "dl#wb-dtmd time::text", "Pub. date")

    entries: List[GlossaryEntry] = []
    dl_lists: list[Any] = html.css("main dl")
    if len(dl_lists) == 0:
        raise ParseException("No DL lists found")

    if isinstance(dl_lists[0], Selector):
        first_dl_list = dl_lists[0]
    else:
        raise ParseException("Expected a <dl>")

    prop: Any
    for prop in first_dl_list.xpath("dt"):
        assert isinstance(prop, Selector)

        # Get the inner text and preserve inner HTML.
        definition: str = (
            prop.xpath("./following-sibling::dd")
            .get()
            .replace("<dd>", "")
            .replace("</dd>", "")
            .replace("  ", " ")
        )
        phrase: str = prop.xpath("normalize-space(descendant::text())").get()

        entries.append(
            GlossaryEntry(
                phrase=NonemptyString(phrase),
                definition=NonemptyString(definition),
            )
        )

    url: str = html.url

    return GlossarySourceParseResult(
        source_url=url,
        name=name,
        author="Department of Justice Canada",
        pub_date=pub_date,
        scrape_date=todays_date(),
        entries=entries,
    )


def parse_name(main: Union[SelectorList, HtmlResponse]) -> str:
    name = first(main, "h1::text", "name")

    if len(main.css("h2")) == 0:  # pyright: reportUnknownArgumentType=false
        return name

    match main.xpath("string(./h2)").get():
        case str(h2):
            return f"{name}, {h2}"
        case _:
            raise ParseException("Could not parse name")


def first(node: Union[SelectorList, HtmlResponse], css: str, expected: str) -> str:
    match node.css(css).get():
        case str(result):
            return normalize_whitespace(result)
        case _:
            raise ParseException(f'Could not parse the {expected} using "{css}"')
