from scrapy import Spider
from scrapy.http.response.html import HtmlResponse
from typing import Any

from ...parsers.can.parliamentary_glossary import parse_glossary

JD_VERBOSE_NAME  = "Canada"
PUBLICATION_NAME = "Glossary of Parliamentary Terms for Intermediate Students"


class USACourtsGlossary(Spider):
    name       = "can_parliamentary_glossary"
    start_urls = ["https://lop.parl.ca/About/Parliament/Education/glossary-intermediate-students-e.html"]

    def parse(self, response: HtmlResponse, **_: dict[str, Any]):
        """Framework callback which begins the parsing.

        @url https://lop.parl.ca/About/Parliament/Education/glossary-intermediate-students-e.html
        @returns items 1 1
        @returns requests 0 0
        @scrapes metadata entries
        """
        yield parse_glossary(response).asdict()
