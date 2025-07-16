# pyright: reportCallIssue=false

from typing import Optional, Protocol

from scrapy.http.response.xml import XmlResponse

from public_law.shared.utils import html, seq, text
from public_law.shared.exceptions import ParseException
from public_law.legal_texts.models.crs import Article, Division, Title
from public_law.legal_texts.parsers.usa.colorado.crs_articles import parse_articles
from public_law.legal_texts.parsers.usa.colorado.crs_divisions import parse_divisions


class Logger(Protocol):
    """Defines a simple shape-based logger interface."""
    def warn(self, message: str) -> None: ...



def parse_title_bang(dom: XmlResponse, logger: Logger) -> Title:
    match parse_title(dom, logger):
        case None:
            raise ParseException("Could not parse title")
        case title:
            return title


def parse_title(dom: XmlResponse, logger: Logger) -> Optional[Title]:
    try:
        name = text.pipe(
            dom
            , html.xpath("//TITLE-TEXT")
            , text.titleize
        )
        number = text.pipe(
            dom
            , html.xpath("//TITLE-NUM")                                        
            , text.split(" ")
            , seq.get(1)
        )
        children = _parse_divisions_or_articles(number, dom, logger)
        url      = _source_url(number)

        return Title(name, number, children, url)

    except ParseException as e:
        logger.warn(f"Could not parse the title: {e}")
        return None


def _parse_divisions_or_articles(title_number: text.NonemptyString, dom: XmlResponse, logger: Logger) -> list[Division] | list[Article]:
    division_nodes = dom.xpath("//T-DIV")
    article_nodes  = dom.xpath("//TA-LIST")

    if len(division_nodes) == 0 and len(article_nodes) == 0:
        msg = f"Neither T-DIV nor TA-LIST nodes were found in {dom.url}"
        logger.warn(msg)
        return []

    if len(division_nodes) > 0:
        parse_fun = parse_divisions
    else:
        parse_fun = parse_articles

    return parse_fun(title_number, dom, logger)

def _source_url(title_number: text.NonemptyString) -> text.URL:
    url_number = title_number.rjust(2, "0")
    return text.URL(f"https://leg.colorado.gov/sites/default/files/images/olls/crs2022-title-{url_number}.pdf")
