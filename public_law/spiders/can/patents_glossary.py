from typing import Generator

from scrapy import Spider
from scrapy.http.response.html import HtmlResponse

from ...parsers.can.patents_glossary import parse_glossary
from ...models.glossary import GlossaryParseResult

URL = "https://ised-isde.canada.ca/site/canadian-intellectual-property-office/en/patents/glossary"


class PatentsGlossarySpider(Spider):
    name = "can_patents_glossary"
    allowed_domains = ["ised-isde.canada.ca"]
    start_urls = [URL]

    def parse(self, response: HtmlResponse) -> Generator[GlossaryParseResult, None, None]:
        """Parse the glossary page and yield the glossary entries."""
        result: GlossaryParseResult = parse_glossary(response)
        yield result
