from scrapy.selector.unified import Selector
from scrapy.http.response.xml import XmlResponse

from typing import Any, Optional, Protocol
from toolz.functoolz import curry, flip

from ....exceptions    import ParseException
from ....flow          import pipe_to_string
from ....selector_util import xpath_get
from ....text          import NonemptyString, URL

import public_law.html  as html
import public_law.lists as lists
import public_law.text  as text

from public_law.items.crs import Article, Division, Title
from .crs_articles  import parse_articles
from .crs_divisions import parse_divisions

split     = curry(flip(str.split))

class Logger(Protocol):
    def warn(self, message: str) -> None: ...



def parse_title_bang(dom: XmlResponse, logger: Logger) -> Title:
    match parse_title(dom, logger):
        case None:
            raise Exception("Could not parse title")
        case title:
            return title


def parse_title(dom: XmlResponse, logger: Logger) -> Optional[Title]:
    try:
        return parse_title_or_raise(dom)
    except ParseException as e:
        logger.warn(f"Could not parse the title: {e}")
        return None


def parse_title_or_raise(dom: XmlResponse) -> Title:
    name = pipe_to_string(
        "//TITLE-TEXT/text()"
        , html.xpath_get(dom)
        , text.titleize
    )
    number = pipe_to_string(
        "//TITLE-NUM/text()"
        , html.xpath_get(dom)
        , text.split_on_space
        , lists.second
    )
    children = _parse_divisions_or_articles(number, dom)
    url      = source_url(number)

    return Title(name, number, children, url)


def _parse_divisions_or_articles(title_number: NonemptyString, dom: Selector | XmlResponse) -> list[Division] | list[Article]:
    division_nodes = dom.xpath("//T-DIV")
    article_nodes  = dom.xpath("//TA-LIST")

    if len(division_nodes) > 0:
        parse_fun = parse_divisions
    elif len(article_nodes) > 0:
        parse_fun = parse_articles
    else:
        msg = f"Neither T-DIV nor TA-LIST nodes were found in Title {title_number}."
        raise ParseException(msg)

    return parse_fun(title_number, dom)


def source_url(title_number: NonemptyString) -> URL:
    url_number = title_number.rjust(2, "0")
    return URL(f"https://leg.colorado.gov/sites/default/files/images/olls/crs2022-title-{url_number}.pdf")
