# pyright: reportUnknownMemberType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportGeneralTypeIssues=false
# pyright: reportUnusedCallResult=false

import os
import re

from pathlib import Path

from progressbar import ProgressBar
from scrapy import Spider
from scrapy.http.request import Request
from scrapy.http.response.html import HtmlResponse
from typing import Any

from public_law.parsers.usa.colorado.crs import parse_title, parse_sections


class ColoradoCRS(Spider):
    """Spider for the Colorado CRS XML files.

    Reads the sources from a local directory instead of the web.
    """
    name     = "usa_colorado_crs"
    DIR      = f"{os.getcwd()}/tmp/sources/CRSDATA20220915"
    XML_DIR  = f"{DIR}/TITLES"


    def start_requests(self):
        """Read the files from a local directory."""
        xml_files = sorted(Path(self.XML_DIR).glob("*.xml"))
        bar = ProgressBar(max_value=len(xml_files)+1).start()

        yield Request(url=f"file://{self.DIR}/README.txt", callback=self.parse_readme)
        bar.update(1)

        for path in xml_files:
            yield Request(url=f"file://{path}", callback=self.parse_title_xml)
            bar.increment()

        bar.finish()


    def parse_readme(self, response: HtmlResponse, **_: dict[str, Any]):
        result = re.findall(r'COLORADO REVISED STATUTES (\d\d\d\d) DATASET', str(response.body))
        if len(result) != 1:
            raise Exception(f"Could not parse year from README: {response.body}")
        
        year: str = result[0]

        yield { "kind": "CRS", "edition": year }


    def parse_title_xml(self, response: HtmlResponse, **_: dict[str, Any]):
        """Framework callback which parses one XML file."""
        self.logger.debug(f"Parsing {response.url}...")

        yield parse_title(response, self.logger)

        for s in parse_sections(response, self.logger):
            yield s
