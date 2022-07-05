from scrapy import Spider
from scrapy.http.response.html import HtmlResponse
from typing import Any

from public_law.parsers.us.courts_glossary import parse_glossary


class USCourtsGlossary(Spider):
    name = "us_courts_glossary"

    start_urls = ["https://www.uscourts.gov/glossary"]

    def parse(self, response: HtmlResponse, **_: dict[str, Any]):
        """Framework callback which begins the parsing."""

        yield dict(parse_glossary(response))
