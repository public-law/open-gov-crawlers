from typing import Any

from scrapy.http.response.html import HtmlResponse

from ...parsers.usa.us_courts_glossary import parse_glossary
from ...models.glossary import GlossaryParseResult
from ..base import BaseGlossarySpider

JD_VERBOSE_NAME = "USA"
PUBLICATION_NAME = "US Courts Glossary"


class USACourtsGlossary(BaseGlossarySpider):
    name = "usa_courts_glossary"

    start_urls = ["https://www.uscourts.gov/glossary"]

    def parse_glossary(self, response: HtmlResponse) -> GlossaryParseResult:
        """Framework callback which begins the parsing."""
        return parse_glossary(response)
