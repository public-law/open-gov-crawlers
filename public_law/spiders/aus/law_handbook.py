from typing import Any

from scrapy.http.response.html import HtmlResponse

from ...parsers.aus.law_handbook import parse_glossary
from public_law.models.glossary import GlossaryParseResult
from public_law.spiders.base import BaseGlossarySpider

JD_VERBOSE_NAME = "Australia"
PUBLICATION_NAME = "Law Handbook Glossary"


class LawHandbookGlossary(BaseGlossarySpider):
    name = "aus_handbook_glossary"

    start_urls = ["https://lawhandbook.sa.gov.au/go01.php"]

    def parse_glossary(self, response: HtmlResponse) -> GlossaryParseResult:
        """Framework callback which begins the parsing.

        @url https://lawhandbook.sa.gov.au/go01.php
        @returns items 1 1
        @returns requests 0 0
        @scrapes metadata entries
        """
        return parse_glossary(response)
