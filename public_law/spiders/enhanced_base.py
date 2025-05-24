import importlib
from abc import ABC
from typing import Any, Generator

from scrapy import Spider
from scrapy.http.response.html import HtmlResponse

from ..models.glossary import GlossaryParseResult


class AutoGlossarySpider(Spider):
    """
    Enhanced base class that automatically resolves parser modules based on naming conventions.

    Subclasses MUST define 'name' and 'start_urls' as class attributes. The parser module is 
    automatically resolved based on the spider name following the convention:

    Spider name: "{country}_{topic}_glossary" 
    Parser module: "public_law.parsers.{country}.{topic}_glossary"

    Example:
        class DVGlossary(AutoGlossarySpider):
            name = "aus_dv_glossary"
            start_urls = ["https://example.com/glossary"]

    This class validates required attributes at class definition time, providing
    immediate feedback for missing or invalid configurations.
    """

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Validate required attributes at class definition time."""
        super().__init_subclass__(**kwargs)

        # Check that name is defined as a class attribute
        if not hasattr(cls, 'name') or not getattr(cls, 'name', None):
            raise TypeError(
                f"{cls.__name__} must define a 'name' class attribute. "
                + "Example: name = 'aus_example_glossary'"
            )

        # Check that start_urls is defined as a class attribute
        if not hasattr(cls, 'start_urls') or not getattr(cls, 'start_urls', None):
            raise TypeError(
                f"{cls.__name__} must define a 'start_urls' class attribute. "
                + "Example: start_urls = ['https://example.com/glossary']"
            )

        # Validate naming convention for early error detection
        spider_name = getattr(cls, 'name', '')
        if spider_name and not cls._is_valid_spider_name(spider_name):
            raise ValueError(
                f"Spider name '{spider_name}' must follow pattern "
                + "'{{country}}_{{topic}}_glossary'. "
                + "Examples: 'aus_dv_glossary', 'usa_uscis_glossary'"
            )

    @classmethod
    def _is_valid_spider_name(cls, name: str) -> bool:
        """Check if spider name follows the expected convention."""
        if not name.endswith('_glossary'):
            return False

        name_without_suffix = name.removesuffix("_glossary")
        parts = name_without_suffix.split("_", 1)
        return len(parts) == 2 and all(part for part in parts)

    def parse(self, response: HtmlResponse, **_: dict[str, Any]) -> Generator[dict[str, Any], None, None]:
        """Parse the response and yield the result in Dublin Core format."""
        result = self.parse_glossary(response)
        yield result.asdict()

    def parse_glossary(self, response: HtmlResponse) -> GlossaryParseResult:
        """
        Parse the glossary page using the automatically resolved parser.

        This method automatically imports and calls the appropriate parser based on
        the spider's name.
        """
        parser_module_path = self._resolve_parser_module()
        parser_module = importlib.import_module(parser_module_path)

        if not hasattr(parser_module, 'parse_glossary'):
            raise AttributeError(
                f"Parser module {parser_module_path} must have a 'parse_glossary' function"
            )

        return parser_module.parse_glossary(response)

    def _resolve_parser_module(self) -> str:
        """
        Resolve the parser module path based on the spider name.

        Converts spider names like "aus_dv_glossary" to parser paths like
        "public_law.parsers.aus.dv_glossary".
        """
        # Remove "_glossary" suffix if present
        name_without_suffix = self.name.removesuffix("_glossary")

        # Split into country and topic
        parts = name_without_suffix.split("_", 1)
        if len(parts) != 2:
            raise ValueError(
                f"Spider name '{self.name}' must follow pattern '{{country}}_{{topic}}_glossary'"
            )

        country, topic = parts
        return f"public_law.parsers.{country}.{topic}_glossary"
