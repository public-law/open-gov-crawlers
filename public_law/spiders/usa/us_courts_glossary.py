from typing import Any

from scrapy import Spider
from scrapy.http.response.html import HtmlResponse

from ...parsers.usa.us_courts_glossary import parse_glossary

JD_VERBOSE_NAME = "USA"
PUBLICATION_NAME = "US Courts Glossary"


class USACourtsGlossary(Spider):
    name = "usa_courts_glossary"

    start_urls = ["https://www.uscourts.gov/glossary"]

    def parse(self, response: HtmlResponse, **_: dict[str, Any]):
        """Framework callback which begins the parsing.

        @url https://www.uscourts.gov/glossary
        @returns items 1 1
        @returns requests 0 0
        @scrapes metadata entries
        """
        yield parse_glossary(response).asdict()
