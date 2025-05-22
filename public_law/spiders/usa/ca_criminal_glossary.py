from typing import Any

from scrapy import Spider
from scrapy.http.response.html import HtmlResponse

from public_law.models.glossary import GlossaryParseResult
from public_law.spiders.base import BaseGlossarySpider

from ...parsers.usa.criminal_glossary import parse_glossary

JD_VERBOSE_NAME = "USA"
PUBLICATION_NAME = "Criminal Glossary"


class CaCriminalGlossary(BaseGlossarySpider):
    name = "usa_criminal_glossary"

    start_urls = [
        "https://www.sdcourt.ca.gov/sdcourt/criminal2/criminalglossary"]

    def parse_glossary(self, response: HtmlResponse) -> GlossaryParseResult:
        """Framework callback which begins the parsing.

        @url https://www.sdcourt.ca.gov/sdcourt/criminal2/criminalglossary
        @returns items 1 1
        @returns requests 0 0
        @scrapes metadata entries
        """
        return parse_glossary(response)
