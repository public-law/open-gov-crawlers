"""
Declarative spider definition macros that generate proper class definitions
for Scrapy auto-discovery while maintaining minimal boilerplate.
"""

import importlib
from typing import Type, Any, Callable

from scrapy.http.response.html import HtmlResponse
from .base import BaseGlossarySpider
from ..models.glossary import GlossaryParseResult


def glossary_spider(
    name: str,
    start_urls: list[str],
    parser_module: str,
    class_name: str | None = None
) -> Type[BaseGlossarySpider]:
    """
    Declarative macro to create a glossary spider class.

    This generates an actual class definition that Scrapy can discover,
    while keeping the syntax minimal and declarative.

    Usage:
        MySpider = glossary_spider(
            name="aus_example_glossary",
            start_urls=["https://example.com/glossary"],
            parser_module="public_law.parsers.aus.example_glossary"
        )
    """
    if class_name is None:
        class_name = f"{name.title().replace('_', '')}Spider"

    # Import the parser function
    parser_mod = importlib.import_module(parser_module)
    parse_glossary_func: Callable[[HtmlResponse],
                                  GlossaryParseResult] = parser_mod.parse_glossary

    # Create the class dynamically but with proper structure for discovery
    class_dict: dict[str, Any] = {
        'name': name,
        'start_urls': start_urls,
        'parse_glossary': lambda self, response: parse_glossary_func(response),
        '__module__': __name__,  # This helps with discovery
    }

    # Create the class using type() for proper class creation
    spider_class: Type[BaseGlossarySpider] = type(
        class_name, (BaseGlossarySpider,), class_dict)

    # Set proper metadata for introspection
    spider_class.__name__ = class_name
    spider_class.__qualname__ = class_name

    return spider_class


# Alternative: Even more minimal syntax using a decorator pattern
def spider_config(name: str, start_urls: list[str], parser_module: str) -> Callable[[Type[BaseGlossarySpider]], Type[BaseGlossarySpider]]:
    """
    Decorator that transforms a minimal class into a full spider.

    Usage:
        @spider_config(
            name="aus_example_glossary",
            start_urls=["https://example.com/glossary"],
            parser_module="public_law.parsers.aus.example_glossary"
        )
        class ExampleSpider(BaseGlossarySpider):
            pass
    """
    def decorator(cls: Type[BaseGlossarySpider]) -> Type[BaseGlossarySpider]:
        # Import the parser function
        parser_mod = importlib.import_module(parser_module)
        parse_glossary_func: Callable[[HtmlResponse],
                                      GlossaryParseResult] = parser_mod.parse_glossary

        # Set class attributes
        cls.name = name
        cls.start_urls = start_urls

        # Override parse_glossary method
        def parse_glossary(self: BaseGlossarySpider, response: HtmlResponse) -> GlossaryParseResult:
            return parse_glossary_func(response)

        cls.parse_glossary = parse_glossary
        return cls

    return decorator
