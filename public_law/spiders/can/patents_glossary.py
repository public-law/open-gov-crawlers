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
        # Debug: Print the URL and content length
        print(f"Spider parsing URL: {response.url}")
        print(f"Content length: {len(response.text)}")

        # Debug: Print first 500 chars of content
        print(f"Content preview: {response.text[:500]}")

        result: GlossaryParseResult = parse_glossary(response)

        # Debug: Print number of entries found
        print(f"Found {len(result.entries)} entries")

        yield result
