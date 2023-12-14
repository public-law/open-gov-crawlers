# fmt: off

from scrapy import Spider
from scrapy.http.response.html import HtmlResponse
from typing import Any


from ...parsers.nzl.justice_glossary import parse_glossary

JD_VERBOSE_NAME = "New Zealand"
PUBLICATION_NAME = "Glossary"


class NZLJusticeGlossary(Spider):
    name       = "nzl_justice_glossary"
    start_urls = ["https://www.justice.govt.nz/about/glossary/"]

    def parse(self, response: HtmlResponse, **_: dict[str, Any]): # type: ignore[override]
        """Framework callback which begins the parsing.

        @url https://www.justice.govt.nz/about/glossary/
        @returns items 1 1
        @returns requests 0 0
        @scrapes metadata entries
        """
        yield parse_glossary(response).asdict()
