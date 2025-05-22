from typing import Any, Generator

from scrapy import Spider
from scrapy.http.response.html import HtmlResponse

from ..models.glossary import GlossaryParseResult


class BaseGlossarySpider(Spider):
    """Base class for all glossary spiders that enforces Dublin Core output format."""

    def parse(self, response: HtmlResponse, **_: dict[str, Any]) -> Generator[dict[str, Any], None, None]:
        """Parse the response and yield the result in Dublin Core format.

        This method enforces that all spiders use the Dublin Core naming format
        by ensuring the result is converted using asdict().
        """
        result = self.parse_glossary(response)
        if not isinstance(result, GlossaryParseResult):  # type: ignore
            raise TypeError("parse_glossary must return a GlossaryParseResult")
        yield result.asdict()

    def parse_glossary(self, response: HtmlResponse) -> GlossaryParseResult:
        """Parse the glossary page and return the result.

        This method must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement parse_glossary")
