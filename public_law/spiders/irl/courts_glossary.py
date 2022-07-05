# fmt: off

from scrapy import Spider
from scrapy.http.response.html import HtmlResponse
from typing import Any

from ...parsers.irl.courts_glossary import parse_glossary


class IRLCourtsGlossary(Spider):
    name       = "irl_courts_glossary"
    start_urls = ["https://www.courts.ie/glossary"]

    def parse(self, response: HtmlResponse, **_: dict[str, Any]):
        """Framework callback which begins the parsing.

        @url https://www.courts.ie/glossary
        @returns items 1 1
        @returns requests 0 0
        @scrapes metadata entries
        """
        yield dict(parse_glossary(response))
