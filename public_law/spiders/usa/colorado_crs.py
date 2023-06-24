from scrapy import Spider
from scrapy.http.response.html import HtmlResponse
from typing import Any

# from ...parsers.usa.uscis_glossary import parse_glossary


class ColoradoCRS(Spider):
    name = "usa_colorado_crs"

    start_urls = ["File://tmp/sources/CRSDATA20220915/TITLES"]

    def parse(self, response: HtmlResponse, **_: dict[str, Any]):
        """Framework callback which begins the parsing.
        """

        yield response.body
