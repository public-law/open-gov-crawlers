from typing import Any

from scrapy import Spider
from scrapy.http.response.html import HtmlResponse

from ...parsers.gbr.fpr_glossary import parse_glossary


class FPRGlossarySpider(Spider):
    """
    Spider for the UK Family Procedure Rules glossary.
    """
    name = "gbr_fpr_glossary"
    start_urls = [
        "https://www.justice.gov.uk/courts/procedure-rules/family/backmatter/fpr_glossary"
    ]

    def parse(self, response: HtmlResponse, **_: dict[str, Any]):
        """
        Parse the glossary page and yield the parsed entries.
        """
        yield parse_glossary(response).asdict()
