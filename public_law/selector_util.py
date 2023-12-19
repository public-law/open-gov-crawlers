# pyright: reportUnknownMemberType=false

from typing import Any

from scrapy.selector.unified import Selector, SelectorList
from scrapy.http.response.xml import XmlResponse

from .exceptions import ParseException

def node_name(node: Selector) -> str | None:
    return node.xpath("name()").get()


def just_text(node: Selector | SelectorList | Any) -> str | None:
    return node.xpath("text()").get()


def xpath_get(dom: XmlResponse, xpath: str) -> str:
    match dom.xpath(xpath).get():
        case str(value):
            return value
        case None:
            raise ParseException(f"Could not find {xpath} in {dom.url}")
