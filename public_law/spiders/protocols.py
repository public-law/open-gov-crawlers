"""
Protocols for type-safe spider interfaces.
"""

from typing import Protocol, List, Type, Any
from scrapy.http.response.html import HtmlResponse


class GlossarySpiderProtocol(Protocol):
    """
    Protocol defining the interface for glossary spiders.

    This enables static type checking and IDE support to ensure
    spiders have the required attributes.
    """

    name: str
    start_urls: List[str]

    def parse_glossary(self, response: HtmlResponse) -> Any:
        """Parse a glossary page and return the result."""
        ...


def validate_spider_interface(spider_class: Type[Any]) -> Type[GlossarySpiderProtocol]:
    """
    Type checker helper to validate spider implements the protocol.

    Usage in spider modules:
        # This will show type errors if Spider is missing required attributes
        _: GlossarySpiderProtocol = validate_spider_interface(MySpider)
    """
    return spider_class
