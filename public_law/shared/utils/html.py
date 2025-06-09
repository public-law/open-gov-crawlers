from typing import TypeVar, Optional, List, Iterator, Any, Dict, Union
from bs4 import BeautifulSoup, Tag, ResultSet
from scrapy.http.response.html import HtmlResponse
from scrapy.http.response.xml import XmlResponse
from scrapy.selector.unified import Selector, SelectorList
from toolz.functoolz import curry

from .exceptions import ParseException
from .text import make_soup
from .result import Result, Ok, Err

T = TypeVar('T')


def node_name(node: Selector) -> str | None:
    return node.xpath("name()").get()


def just_text(node: Selector | SelectorList | Any) -> str | None:
    return node.xpath("text()").get()


def xpath(selector: str, dom: XmlResponse) -> str:
    """
    Extracts the text content from the XML response using the given XPath selector.
    It does this by appending "/text()" to the selector and returning the first
    match. If no match is found, it raises a ParseException.

    Args:
        selector (str): The XPath selector to match the desired elements.
        dom (XmlResponse): The XML response object.

    Returns:
        str: The extracted text content.

    Raises:
        ParseException: If the specified XPath selector cannot be found in the XML response.
    """
    match dom.xpath(selector + "/text()").get():
        case str(value):
            return value
        case None:
            raise ParseException(f"Could not find {xpath} in {dom.url}")


xpath = curry(xpath)  # type: ignore
