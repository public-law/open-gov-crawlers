from typing import Any, cast

from scrapy.http.response import Response
from scrapy.http.response.html import HtmlResponse

from ...parsers.usa.uscis_glossary import parse_glossary
from ...models.glossary import GlossaryParseResult
from ..base import BaseGlossarySpider

JD_VERBOSE_NAME = "USA"
PUBLICATION_NAME = "USCIS Glossary"


class USCISGlossary(BaseGlossarySpider):
    name = "usa_uscis_glossary"

    start_urls = ["https://www.uscis.gov/tools/glossary"]

    def parse_glossary(self, response: Response) -> GlossaryParseResult:
        """Framework callback which begins the parsing."""
        return parse_glossary(cast(HtmlResponse, response))
