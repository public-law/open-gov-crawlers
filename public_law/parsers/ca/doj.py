from datetime import date, datetime
from typing import List, NamedTuple, Protocol, Union

import pytz
from scrapy import Selector
from scrapy.http import HtmlResponse
from scrapy.selector.unified import SelectorList

from public_law.text import NonemptyString, normalize_whitespace


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

    name: str
    source_url: str
    author: str
    pub_date: str
    scrape_date: str
    entries: List[GlossaryEntry]


def parse_glossary(html: HtmlResponse) -> GlossarySourceParseResult:
    main: SelectorList = html.css("main")

    name = first(main, "h1::text", "name") + "; " + first(main, "h2::text", "name")
    pub_date = first(html, "dl#wb-dtmd time::text", "Pub. date")

    entries: List[GlossaryEntry] = []
    dl_lists = html.css("main dl")
    if len(dl_lists) == 0:
        raise ParseException("No DL lists found")

    if isinstance(dl_lists[0], Selector):
        first_dl_list = dl_lists[0]
    else:
        raise ParseException("Expected a <dl>")

    for prop in first_dl_list.xpath("dt"):
        assert isinstance(prop, Selector)

        entries.append(
            GlossaryEntry(
                phrase=NonemptyString(
                    prop.xpath("normalize-space(descendant::text())").get()
                ),
                definition=NonemptyString(
                    prop.xpath("normalize-space(./following-sibling::dd/text())").get()
                ),
            )
        )

    return GlossarySourceParseResult(
        name=name,
        source_url=html.url,
        author="Department of Justice Canada",
        pub_date=pub_date,
        scrape_date=todays_date(),
        entries=entries,
    )


def first(node: Union[SelectorList, HtmlResponse], css: str, expected: str) -> str:
    result = node.css(css).get()
    if result is None:
        raise ParseException(f"Could not parse the {expected}")
    return normalize_whitespace(result)


class SimpleTimezone(Protocol):
    def localize(self, dt: datetime) -> date:
        ...


def todays_date() -> str:
    mountain: SimpleTimezone = pytz.timezone("US/Mountain")
    fmt = "%Y-%m-%d"
    return mountain.localize(datetime.now()).strftime(fmt)
