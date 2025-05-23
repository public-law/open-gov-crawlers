from typing import Any

from scrapy.http.response.html import HtmlResponse

from ...parsers.aus.designip_glossary import parse_glossary
from ...models.glossary import GlossaryParseResult
from ..base import BaseGlossarySpider

JD_VERBOSE_NAME = "Australia"
PUBLICATION_NAME = "Design Examiners Manual Glossary"


class DesignIPGlossary(BaseGlossarySpider):
    name = "aus_designip_glossary"

    start_urls = [
        "http://manuals.ipaustralia.gov.au/design/glossary"
    ]

    def parse_glossary(self, response: HtmlResponse) -> GlossaryParseResult:
        """Framework callback which begins the parsing.

        @url http://manuals.ipaustralia.gov.au/design/glossary
        @returns items 1 1
        @returns requests 0 0
        @scrapes metadata entries
        """
        return parse_glossary(response)
