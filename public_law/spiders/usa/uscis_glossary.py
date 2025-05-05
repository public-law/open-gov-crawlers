from typing import Any, cast

from scrapy import Spider
from scrapy.http.response import Response
from scrapy.http.response.html import HtmlResponse

from ...parsers.usa.uscis_glossary import parse_glossary

JD_VERBOSE_NAME  = "USA"
PUBLICATION_NAME = "USCIS Glossary"


class USCISGlossary(Spider):
    name = "usa_uscis_glossary"

    start_urls = ["https://www.uscis.gov/tools/glossary"]

    def parse(self, response: Response, **_: dict[str, Any]):
        """Framework callback which begins the parsing.

        @url https://www.uscis.gov/tools/glossary
        @returns items 1 1
        @returns requests 0 0
        @scrapes metadata entries
        """
        yield parse_glossary(cast(HtmlResponse, response)).asdict()
