import importlib
from typing import Any, Generator

from scrapy import Spider
from scrapy.http.response.html import HtmlResponse

from public_law.legal_texts.models.statute import StatuteParseResult
from public_law.shared.models.metadata import Metadata


class BaseStatuteSpider(Spider):
    """Base class for all state statute spiders that enforces output format."""

    def parse(self, response: HtmlResponse, **_: dict[str, Any]) -> Generator[dict[str, Any], None, None]:
        """Parse the response and yield the result in standardized format.

        This method enforces that all spiders use the standardized format
        by ensuring the result is converted using asdict().
        """
        result = self.parse_statutes(response)
        if not isinstance(result, StatuteParseResult):
            raise TypeError("parse_statutes must return a StatuteParseResult")
        yield result.asdict()

    def parse_statutes(self, response: HtmlResponse) -> StatuteParseResult:
        """Parse the statute page and return the result.

        This method must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement parse_statutes")


class EnhancedAutoStatuteSpider(BaseStatuteSpider):
    """Enhanced base for new statute spiders with auto-resolution.
    
    This class separates concerns cleanly:
    - Parsers handle pure data extraction (parse_statute_entries)
    - Spiders handle configuration and orchestration (get_metadata + parse_statutes)
    
    Subclasses MUST define 'name', 'start_urls', and 'get_metadata()' method.
    
    Example:
        class FloridaStatutes(EnhancedAutoStatuteSpider):
            name = "usa_florida_statutes"
            start_urls = ["http://www.leg.state.fl.us/Statutes/"]
            
            def get_metadata(self, response: HtmlResponse) -> Metadata:
                return Metadata(
                    dcterms_title=String("Florida Statutes"),
                    dcterms_coverage="Florida, USA",
                    # ... etc
                )
    """
    
    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Validate required attributes at class definition time."""
        super().__init_subclass__(**kwargs)
        
        # Skip validation for base classes
        if cls.__name__ in ('BaseStatuteSpider', 'EnhancedAutoStatuteSpider'):
            return
            
        # Check that name is defined as a class attribute
        if not hasattr(cls, 'name') or not getattr(cls, 'name', None):
            raise TypeError(
                f"{cls.__name__} must define a 'name' class attribute. "
                + "Example: name = 'usa_florida_statutes'"
            )
            
        # Check that start_urls is defined as a class attribute
        if not hasattr(cls, 'start_urls') or not getattr(cls, 'start_urls', None):
            raise TypeError(
                f"{cls.__name__} must define a 'start_urls' class attribute. "
                + "Example: start_urls = ['http://www.leg.state.fl.us/Statutes/']"
            )
        
        # Validate naming convention for early error detection
        spider_name = getattr(cls, 'name', '')
        if spider_name and not cls._is_valid_spider_name(spider_name):
            raise ValueError(
                f"Spider name '{spider_name}' must follow pattern "
                + "'usa_{{state}}_statutes'. "
                + "Examples: 'usa_florida_statutes', 'usa_texas_statutes'"
            )

    @classmethod
    def _is_valid_spider_name(cls, name: str) -> bool:
        """Check if spider name follows the expected convention."""
        if not name.endswith('_statutes'):
            return False
            
        name_without_suffix = name.removesuffix("_statutes")
        parts = name_without_suffix.split("_", 1)
        return len(parts) == 2 and parts[0] == "usa" and bool(parts[1])
    
    def parse_statutes(self, response: HtmlResponse) -> StatuteParseResult:
        """
        Parse the statute page using the automatically resolved parser and spider metadata.

        This method automatically imports the appropriate parser based on the spider's name,
        calls it to extract entries, gets metadata from the spider, and combines them.
        """
        parser_module_path = self._resolve_parser_module()
        parser_module = importlib.import_module(parser_module_path)

        if not hasattr(parser_module, 'parse_statute_entries'):
            raise AttributeError(
                f"Parser module {parser_module_path} must have a 'parse_statute_entries' function"
            )

        entries = parser_module.parse_statute_entries(response)
        metadata = self.get_metadata(response)
        
        return StatuteParseResult(metadata, entries)
    
    def _resolve_parser_module(self) -> str:
        """
        Resolve the parser module path based on the spider name.

        Converts spider names like "usa_florida_statutes" to parser paths like
        "public_law.legal_texts.parsers.usa.florida_statutes".
        """
        # Remove "_statutes" suffix if present
        name_without_suffix = self.name.removesuffix("_statutes")

        # Split into country and state
        parts = name_without_suffix.split("_", 1)
        if len(parts) != 2 or parts[0] != "usa":
            raise ValueError(
                f"Spider name '{self.name}' must follow pattern 'usa_{{state}}_statutes'"
            )

        country, state = parts
        return f"public_law.legal_texts.parsers.{country}.{state}_statutes"
    
    def get_metadata(self, response: HtmlResponse) -> Metadata:
        """Get metadata for the statutes - must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement get_metadata")