from scrapy import Spider
from scrapy.http.response.html import HtmlResponse
from typing import Any

from ...parsers.aus.dv_glossary import parse_glossary

JD_VERBOSE_NAME = "Australia"
PUBLICATION_NAME = "Family, domestic and sexual violence glossary"


class DVGlossary(Spider):
    name = "aus_dv_glossary"

    start_urls = [
        "https://www.aihw.gov.au/reports-data/behaviours-risk-factors/domestic-violence/glossary"
    ]

    def parse(self, response: HtmlResponse, **_: dict[str, Any]):
        """Framework callback which begins the parsing.

        @url https://www.aihw.gov.au/reports-data/behaviours-risk-factors/domestic-violence/glossary
        @returns items 1 1
        @returns requests 0 0
        @scrapes metadata entries
        """
        yield parse_glossary(response).asdict()
