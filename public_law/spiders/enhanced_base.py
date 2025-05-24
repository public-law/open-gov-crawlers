import importlib
from typing import Any, Generator

from scrapy import Spider
from scrapy.http.response.html import HtmlResponse

from ..models.glossary import GlossaryParseResult


class AutoGlossarySpider(Spider):
    """
    Enhanced base class that automatically resolves parser modules based on naming conventions.

    Subclasses only need to define 'name' and 'start_urls'. The parser module is automatically
    resolved based on the spider name following the convention:

    Spider name: "{country}_{topic}_glossary" 
    Parser module: "public_law.parsers.{country}.{topic}_glossary"

    Example:
        Spider name: "aus_dv_glossary"
        Parser module: "public_law.parsers.aus.dv_glossary"
    """

    def parse(self, response: HtmlResponse, **_: dict[str, Any]) -> Generator[dict[str, Any], None, None]:
        """Parse the response and yield the result in Dublin Core format."""
        result = self.parse_glossary(response)
        if not isinstance(result, GlossaryParseResult):
            raise TypeError("parse_glossary must return a GlossaryParseResult")
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
        if not self.name:
            raise ValueError("Spider must have a 'name' attribute")

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
