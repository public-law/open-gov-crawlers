from typing import Any

from scrapy import Spider
from scrapy.http.response.html import HtmlResponse

import public_law.parsers.can.doj_glossaries as parser

JD_VERBOSE_NAME = "Canada"
PUBLICATION_NAME = "Dept. of Justice Legal Glossaries"


class DojGlossaries(Spider):
    name = "can_doj_glossaries"
    start_urls = parser.configured_urls()

    def parse(self, response: HtmlResponse, **_: dict[str, Any]):
        """Framework callback which begins the parsing.

        @url https://www.justice.gc.ca/eng/fl-df/parent/mp-fdp/p11.html
        @returns items 1 1
        @returns requests 0 0
        @scrapes metadata entries
        """
        yield parser.parse_glossary(response).asdict()
