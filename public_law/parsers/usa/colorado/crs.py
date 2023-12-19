# pyright: reportUnknownMemberType=false

from scrapy.selector.unified import Selector
from scrapy.http.response.xml import XmlResponse

from typing import Any, Optional
from toolz.functoolz import curry, flip, pipe # type: ignore

from public_law.exceptions import ParseException
from public_law.selector_util import xpath_get
from public_law.text import NonemptyString, URL, titleize
from public_law.items.crs import Article, Division, Title
from public_law.parsers.usa.colorado.crs_articles  import parse_articles
from public_law.parsers.usa.colorado.crs_divisions import parse_divisions

split       = curry(flip(str.split))
second: str = lambda x: x[1] # type: ignore
xpath_get   = curry(xpath_get)

def parse_title_bang(dom: XmlResponse, logger: Any) -> Title:
    match parse_title(dom, logger):
        case None:
            raise Exception("Could not parse title")
        case title:
            return title


def parse_title(dom: XmlResponse, logger: Any) -> Optional[Title]:
    try:
        name: NonemptyString = pipe(                                       # type: ignore
            "//TITLE-TEXT/text()",
            xpath_get(dom),
            titleize,
            NonemptyString
        )
        number: NonemptyString = pipe(                                     # type: ignore
            "//TITLE-NUM/text()",
            xpath_get(dom),
            split(" "),
            second,
            NonemptyString
        )
        children = _parse_divisions_or_articles(number, dom, logger)

        return Title(
            name       = name,
            number     = number,
            source_url = source_url(number),
            children   = children
        )

    except ParseException as e:
        logger.warn(f"Could not parse the title: {e}")
        return None
        

def _parse_divisions_or_articles(title_number: NonemptyString, dom: Selector | XmlResponse, logger: Any) -> list[Division] | list[Article]:
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


def source_url(title_number: NonemptyString) -> URL:
    url_number = title_number.rjust(2, "0")
    return URL(f"https://leg.colorado.gov/sites/default/files/images/olls/crs2022-title-{url_number}.pdf")
