# pyright: reportUnknownMemberType=false

from scrapy.selector.unified import Selector
from scrapy.http.response.xml import XmlResponse

from typing import Any

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


def parse_title(dom: XmlResponse, logger: Any) -> Title | None:
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

    url_number = number.rjust(2, "0")
    source_url = URL(f"https://leg.colorado.gov/sites/default/files/images/olls/crs2022-title-{url_number}.pdf")

    return Title(
        name       = name,
        number     = number,
        source_url = URL(source_url),
        children   = _parse_divisions_or_articles(number, dom, logger)
    )


def _parse_divisions_or_articles(title_number: NonemptyString, dom: Selector | XmlResponse, logger: Any) -> list[Division] | list[Article]:
    division_nodes = dom.xpath("//T-DIV")
    article_nodes  = dom.xpath("//TA-LIST")

    if len(division_nodes) > 0:
        func = parse_divisions
    elif len(article_nodes) > 0:
        func = parse_articles
    else:
        raise Exception(f"Could not parse divisions or articles in Title {title_number}. Neither T-DIV nor TA-LIST nodes were found.")

    return func(title_number, dom, logger)
