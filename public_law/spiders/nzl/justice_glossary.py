from scrapy.http.response.html import HtmlResponse

from ...parsers.nzl.justice_glossary import parse_glossary
from ...models.glossary import GlossaryParseResult
from ..base import BaseGlossarySpider

JD_VERBOSE_NAME = "New Zealand"
PUBLICATION_NAME = "Glossary"


class NZLJusticeGlossary(BaseGlossarySpider):
    name = "nzl_justice_glossary"
    start_urls = ["https://www.justice.govt.nz/about/glossary/"]

    def parse_glossary(self, response: HtmlResponse) -> GlossaryParseResult:
        """Framework callback which begins the parsing."""
        return parse_glossary(response)
