from typing import Any, Optional, Protocol, cast

from scrapy.http.response.xml import XmlResponse
from scrapy.selector.unified import Selector
from toolz import functoolz

from public_law import html, text
from public_law.exceptions import ParseException
from public_law.items.crs import Article, Division, Title
from public_law.parsers.usa.colorado.crs_articles import parse_articles
from public_law.parsers.usa.colorado.crs_divisions import parse_divisions


def second(x: list[Any]) -> Any:
    return x[1]


class Logger(Protocol):
    """Define a simple shape-based logger interface."""
    def warn(self, message: str) -> None: ...



def parse_title_bang(dom: XmlResponse, logger: Logger) -> Title:
    match parse_title(dom, logger):
        case None:
            raise Exception("Could not parse title")
        case title:
            return title


def parse_title(dom: XmlResponse, logger: Logger) -> Optional[Title]:
    try:
        name = pipe(
            "//TITLE-TEXT/text()"
            , html.xpath(dom)  # type: ignore
            , text.titleize
        )
        number = pipe(
            "//TITLE-NUM/text()"
            , html.xpath(dom)  # type: ignore
            , text.split(" ")
            , second
        )
        children = _parse_divisions_or_articles(number, dom, logger)
        url      = source_url(number)

        return Title(name, number, children, url)

    except ParseException as e:
        logger.warn(f"Could not parse the title: {e}")
        return None


def pipe(*args: Any) -> text.NonemptyString:
    """
    A wrapper around pipe() that casts the result.
    """
    args_with_string: Any = args + (text.NonemptyString,)

    return cast(text.NonemptyString, functoolz.pipe(*args_with_string))  # type: ignore


def _parse_divisions_or_articles(title_number: text.NonemptyString, dom: Selector | XmlResponse, logger: Logger) -> list[Division] | list[Article]:
    division_nodes = dom.xpath("//T-DIV")
    article_nodes  = dom.xpath("//TA-LIST")

    if len(division_nodes) > 0:
        parse_fun = parse_divisions
    elif len(article_nodes) > 0:
        parse_fun = parse_articles
    else:
        msg = f"Neither T-DIV nor TA-LIST nodes were found in Title {title_number}."
        raise ParseException(msg)

    return parse_fun(title_number, dom, logger)


def source_url(title_number: text.NonemptyString) -> text.URL:
    url_number = title_number.rjust(2, "0")
    return text.URL(f"https://leg.colorado.gov/sites/default/files/images/olls/crs2022-title-{url_number}.pdf")
