# pyright: reportUnknownMemberType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownParameterType=false
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


    def start_requests(self):
        """Read the files from a local directory."""
        try:
            dir = self.crsdata_dir
        except:
            raise Exception("No crsdata_dir specified.")

        DIR      = f"{os.getcwd()}/{dir}"
        XML_DIR  = f"{DIR}/TITLES"

        xml_files = sorted(Path(XML_DIR).glob("*.xml"))
        xml_urls  = [f"file://{path}" for path in xml_files]
        readme_url = f"file://{DIR}/README.txt"

        with ProgressBar(max_value = len(xml_files) + 1) as bar:
            yield Request(readme_url)
            bar.update(1)

            for url in xml_urls:
                yield Request(url)
                bar.increment()


    def parse(self, response: HtmlResponse, **_: dict[str, Any]):
        if "README.txt" in response.url:
            yield from self.parse_readme(response)
        else:
            yield from self.parse_title_xml(response)


    def parse_readme(self, response: HtmlResponse, **_: dict[str, Any]):
        result = re.findall(r'COLORADO REVISED STATUTES (\d\d\d\d) DATASET', str(response.body))
        if len(result) != 1:
            raise Exception(f"Could not parse year from README: {response.body}")
        
        year: str = result[0]

        yield { "kind": "CRS", "edition": int(year) }


    def parse_title_xml(self, response: HtmlResponse, **_: dict[str, Any]):
        """Framework callback which parses one XML file."""
        self.logger.debug(f"Parsing {response.url}...")

        yield parse_title(response, self.logger)

        for s in parse_sections(response, self.logger):
            yield s
