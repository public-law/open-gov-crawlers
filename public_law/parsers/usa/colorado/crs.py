# pyright: reportUnknownMemberType=false

from scrapy.selector.unified import Selector
from scrapy.http.response.xml import XmlResponse

from typing import Any, Optional

from public_law.text import NonemptyString, URL, titleize
from public_law.items.crs import Article, Division, Title
from public_law.parsers.usa.colorado.crs_articles  import parse_articles
from public_law.parsers.usa.colorado.crs_divisions import parse_divisions


def parse_title_bang(dom: XmlResponse, logger: Any) -> Title:
    match parse_title(dom, logger):
        case None:
            raise Exception("Could not parse title")
        case title:
            return title


def parse_title(dom: XmlResponse, logger: Any) -> Optional[Title]:
    match(dom.xpath("//TITLE-TEXT/text()").get()):
        case str(raw_name):
            name = NonemptyString(titleize(raw_name))
        case None:
            logger.warn(f"Could not the parse title name in {dom.url}")
            return None

    match(dom.xpath("//TITLE-NUM/text()").get()):
        case str(raw_number):
            number = NonemptyString(raw_number.split(" ")[1])
        case None:
            logger.warn(f"Could not the parse title number in {dom.url}")
            return None
    
    match _parse_divisions_or_articles(number, dom, logger):
        case list(children):
            return Title(
                name       = name,
                number     = number,
                source_url = title_source_url(number),
                children   = children
            )
        case None:
            return None


def _parse_divisions_or_articles(title_number: NonemptyString, dom: Selector | XmlResponse, logger: Any) -> Optional[list[Division] | list[Article]]:
    division_nodes = dom.xpath("//T-DIV")
    article_nodes  = dom.xpath("//TA-LIST")

    if len(division_nodes) > 0:
        parse_fun = parse_divisions
    elif len(article_nodes) > 0:
        parse_fun = parse_articles
    else:
        msg = f"Could not parse divisions or articles in Title {title_number}. Neither T-DIV nor TA-LIST nodes were found."
        logger.warn(msg)
        return None

    return parse_fun(title_number, dom, logger)


def title_source_url(title_number: NonemptyString) -> URL:
    url_number = title_number.rjust(2, "0")
    return URL(f"https://leg.colorado.gov/sites/default/files/images/olls/crs2022-title-{url_number}.pdf")
