from typing import TypeVar, Optional, List, Iterator, Any
from bs4 import BeautifulSoup, Tag, ResultSet
from scrapy.http.response.html import HtmlResponse
from scrapy.http.response.xml import XmlResponse
from scrapy.selector.unified import Selector, SelectorList
from toolz.functoolz import curry

from .exceptions import ParseException
from .text import make_soup
from .result import Result, Ok, Err

T = TypeVar('T')


class TypedSoup:
    """A type-safe wrapper around BeautifulSoup results."""

    def __init__(self, element: Tag | BeautifulSoup) -> None:  # type: ignore
        self._element = element

    def find(self, name: str) -> 'TypedSoup | None':
        """Find a single element, returning None if not found or not a Tag."""
        result = self._element.find(name)
        if not result or not isinstance(result, Tag):
            return None
        return TypedSoup(result)

    def find_all(self, name: str) -> List['TypedSoup']:
        """Find all elements, filtering out non-Tag results."""
        return [
            TypedSoup(tag) for tag in self._element.find_all(name)
            if isinstance(tag, Tag)
        ]

    def get_text(self, strip: bool = True) -> str:
        """Get text content, guaranteed to be a string."""
        return self._element.get_text(strip=strip)

    def __bool__(self) -> bool:
        """Allow using the wrapper in boolean contexts."""
        return bool(self._element)

    def children(self) -> list['TypedSoup']:
        return [TypedSoup(child) for child in self._element.children if isinstance(child, Tag)]

    def tag_name(self) -> str | None:
        return self._element.name

    def parent(self) -> 'TypedSoup | None':
        parent = self._element.parent
        if isinstance(parent, Tag):
            return TypedSoup(parent)
        return None

    def next_sibling(self) -> 'TypedSoup | None':
        sibling = self._element.next_sibling
        if isinstance(sibling, Tag):
            return TypedSoup(sibling)
        return None


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


def parse_html(html: HtmlResponse) -> TypedSoup:
    """Create a type-safe BeautifulSoup wrapper from an HTML response."""
    return TypedSoup(make_soup(html))
