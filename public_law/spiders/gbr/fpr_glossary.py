from typing import Any

from scrapy.http.response.html import HtmlResponse

from ...parsers.gbr.fpr_glossary import parse_glossary
from ...models.glossary import GlossaryParseResult
from ..base import BaseGlossarySpider


class FPRGlossarySpider(BaseGlossarySpider):
    """
    Spider for the UK Family Procedure Rules glossary.
    """
    name = "gbr_fpr_glossary"
    start_urls = [
        "https://www.justice.gov.uk/courts/procedure-rules/family/backmatter/fpr_glossary"
    ]

    def parse_glossary(self, response: HtmlResponse) -> GlossaryParseResult:
        """
        Parse the glossary page and return the parsed entries.
        """
        return parse_glossary(response)
