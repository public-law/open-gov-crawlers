from typing import Any

from scrapy.http.response.html import HtmlResponse

from ...parsers.aus.dv_glossary import parse_glossary
from ...models.glossary import GlossaryParseResult
from ..base import BaseGlossarySpider

JD_VERBOSE_NAME = "Australia"
PUBLICATION_NAME = "Family, domestic and sexual violence glossary"


class DVGlossary(BaseGlossarySpider):
    name = "aus_dv_glossary"

    start_urls = [
        "https://www.aihw.gov.au/reports-data/behaviours-risk-factors/domestic-violence/glossary"
    ]

    def parse_glossary(self, response: HtmlResponse) -> GlossaryParseResult:
        """Framework callback which begins the parsing."""
        return parse_glossary(response)
