# pyright: reportUnknownMemberType=false
# pyright: reportOptionalMemberAccess=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownLambdaType=false


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
        case result:
            return result


def parse_title(dom: XmlResponse, logger: Any) -> Title | None:
    raw_name = dom.xpath("//TITLE-TEXT/text()").get()
    
    if raw_name is None:
        logger.warn(f"Could not parse title name in {dom.url}")
        return None

    name       = NonemptyString(titleize(raw_name))
    number     = NonemptyString(dom.xpath("//TITLE-NUM/text()").get().split(" ")[1])
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
        return parse_divisions(title_number, dom, logger)
    elif len(article_nodes) > 0:
        return parse_articles(title_number, dom, logger)
    else:
        raise Exception(f"Could not parse divisions or articles in Title {title_number}")
