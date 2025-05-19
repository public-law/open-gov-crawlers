from typing import Any

from scrapy import Spider
from scrapy.http.response.html import HtmlResponse

from ...parsers.usa.criminal_glossary import parse_glossary

JD_VERBOSE_NAME = "USA"
PUBLICATION_NAME = "Criminal Glossary"


class CriminalGlossary(Spider):
    name = "usa_ca_criminal_glossary"

    start_urls = [
        "https://www.sdcourt.ca.gov/sdcourt/criminal2/criminalglossary"]

    def parse(self, response: HtmlResponse, **_: dict[str, Any]):
        """Framework callback which begins the parsing.

        @url https://www.sdcourt.ca.gov/sdcourt/criminal2/criminalglossary
        @returns items 1 1
        @returns requests 0 0
        @scrapes metadata entries
        """
        yield parse_glossary(response).asdict()
