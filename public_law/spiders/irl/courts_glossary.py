# fmt: off

from typing import Any

from scrapy.http.response.html import HtmlResponse

from ...parsers.irl.courts_glossary import parse_glossary
from ...models.glossary import GlossaryParseResult
from ..base import BaseGlossarySpider

JD_VERBOSE_NAME = "Ireland"
PUBLICATION_NAME = "Glossary of Legal Terms"


class IRLCourtsGlossary(BaseGlossarySpider):
    name = "irl_courts_glossary"
    start_urls = ["https://www.courts.ie/glossary"]

    def parse_glossary(self, response: HtmlResponse) -> GlossaryParseResult:
        """Framework callback which begins the parsing."""
        return parse_glossary(response)
