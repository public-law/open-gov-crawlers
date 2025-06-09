# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright: reportGeneralTypeIssues=false

import os
from pathlib import Path
from typing import Any, cast

from progressbar import ProgressBar
from scrapy import Spider
from scrapy.http.request import Request
from scrapy.http.response.html import HtmlResponse

from public_law.shared.utils import dates
from public_law.legal_texts.parsers.usa.colorado.crs import parse_title
from public_law.legal_texts.parsers.usa.colorado.crs_sections import parse_sections


class ColoradoCRS(Spider):
    """Spider for the Colorado CRS XML files.

    Reads the sources from a local directory instead of the web.
    """
    name = "usa_colorado_crs"


    def start_requests(self):
        """Read the files from a local directory."""
        if hasattr(self, "crsdata_dir") == False:
            raise Exception("No crsdata_dir specified with the -a command line option.")
        
        dir = cast(str, self.crsdata_dir) # pyright: ignore[reportAttributeAccessIssue]

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


    def parse(self, response: HtmlResponse, **_: dict[str, Any]): # type: ignore[override]
        if "README.txt" in response.url:
            yield { "kind": "CRS", "edition": dates.current_year() }
        else:
            yield from self.parse_title_xml(response)


    def parse_title_xml(self, response: HtmlResponse, **_: dict[str, Any]):
        """Framework callback which parses one XML file."""
        self.logger.debug(f"Parsing {response.url}...")

        yield parse_title(response, self.logger) # type: ignore

        for s in parse_sections(response, self.logger): # type: ignore
            yield s
