from typing import Any

from scrapy import Spider
from scrapy.http.response.html import HtmlResponse

from ...parsers.aus.law_handbook import parse_glossary

JD_VERBOSE_NAME = "Australia"
PUBLICATION_NAME = "Law Handbook Glossary"


class LawHandbookGlossary(Spider):
    name = "aus_law_handbook"

    start_urls = ["https://lawhandbook.sa.gov.au/go01.php"]

    def parse(self, response: HtmlResponse, **_: dict[str, Any]):
        """Framework callback which begins the parsing.

        @url https://lawhandbook.sa.gov.au/go01.php
        @returns items 1 1
        @returns requests 0 0
        @scrapes metadata entries
        """
        yield parse_glossary(response).asdict()
