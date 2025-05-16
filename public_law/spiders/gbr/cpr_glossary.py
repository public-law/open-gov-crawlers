from typing import Any

from scrapy import Spider
from scrapy.http.response.html import HtmlResponse

from ...parsers.gbr.cpr_glossary import parse_glossary


class CPRGlossarySpider(Spider):
    """
    Spider for the UK Criminal Procedure Rules glossary.
    """
    name = "gbr_cpr_glossary"
    start_urls = [
        "https://www.legislation.gov.uk/uksi/2020/759/part/Glossary?view=plain"
    ]

    def parse(self, response: HtmlResponse, **_: dict[str, Any]):
        """
        Parse the glossary page and yield the parsed entries.
        """
        yield parse_glossary(response).asdict()
