from typing import Generator

from scrapy.http.response.html import HtmlResponse

from ...parsers.can.patents_glossary import parse_glossary
from ...models.glossary import GlossaryParseResult
from ..base import BaseGlossarySpider

URL = "https://ised-isde.canada.ca/site/canadian-intellectual-property-office/en/patents/glossary"


class PatentsGlossarySpider(BaseGlossarySpider):
    name = "can_patents_glossary"
    allowed_domains = ["ised-isde.canada.ca"]
    start_urls = [URL]

    def parse_glossary(self, response: HtmlResponse) -> GlossaryParseResult:
        """Parse the glossary page and return the glossary entries."""
        return parse_glossary(response)
