from scrapy.http.response.html import HtmlResponse

from ...parsers.aus.ip_glossary import parse_glossary
from ...models.glossary import GlossaryParseResult
from ..base import BaseGlossarySpider

JD_VERBOSE_NAME = "Australia"
PUBLICATION_NAME = "IP Glossary"


class IPGlossary(BaseGlossarySpider):
    name = "aus_ip_glossary"

    start_urls = [
        "https://raw.githubusercontent.com/public-law/datasets/master/Australia/ip-glossary.html"
    ]

    def parse_glossary(self, response: HtmlResponse) -> GlossaryParseResult:
        """Framework callback which begins the parsing."""
        return parse_glossary(response)
