from scrapy import Spider
from scrapy.http.response.html import HtmlResponse
from typing import Any

from ...parsers.aus.ip_glossary import parse_glossary

JD_VERBOSE_NAME = "Australia"
PUBLICATION_NAME = "IP Glossary"


class USACourtsGlossary(Spider):
    name = "aus_ip_glossary"

    start_urls = [
        "https://raw.githubusercontent.com/public-law/datasets/master/Australia/ip-glossary.html"
    ]

    def parse(self, response: HtmlResponse, **_: dict[str, Any]):
        """Framework callback which begins the parsing.

        @url https://raw.githubusercontent.com/public-law/datasets/master/Australia/ip-glossary.html
        @returns items 1 1
        @returns requests 0 0
        @scrapes metadata entries
        """
        yield parse_glossary(response).asdict()
