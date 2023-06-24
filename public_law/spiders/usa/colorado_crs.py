# pyright: reportUnknownMemberType=false

import os
from pathlib import Path

from scrapy import Spider
from scrapy.http.request import Request
from scrapy.http.response.html import HtmlResponse
from typing import Any

from public_law.parsers.usa.colorado.crs import parse_title, parse_sections


class ColoradoCRS(Spider):
    """Spider for the Colorado CRS XML files.

    Reads the sources from a local directory instead of the web.
    """
    name = "usa_colorado_crs"
    XML_DIR  = f"{os.getcwd()}/tmp/sources/CRSDATA20220915/TITLES"


    def start_requests(self):
        for path in sorted(Path(self.XML_DIR).glob("*.xml")):
            yield Request(url=f"file://{path}", callback=self.parse)


    def parse(self, response: HtmlResponse, **_: dict[str, Any]):
        """Framework callback which begins the parsing."""
        self.logger.debug(f"Parsing {response.url}...")

        yield parse_title(response, self.logger)

        for s in parse_sections(response, self.logger):
            yield s
