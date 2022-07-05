# fmt: off

from scrapy import Spider
from scrapy.http.response.html import HtmlResponse
from typing import Any

from ...parsers.nzl.justice_glossary import parse_glossary


class NZJusticeGlossary(Spider):
    name       = "nz_justice_glossary"
    start_urls = ["https://www.justice.govt.nz/about/glossary/"]

    def parse(self, response: HtmlResponse, **_: dict[str, Any]):
        """Framework callback which begins the parsing.

        @url https://www.justice.govt.nz/about/glossary/
        @returns items 1 1
        @returns requests 0 0
        @scrapes metadata entries
        """
        yield dict(parse_glossary(response))
