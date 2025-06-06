from scrapy.http.response.html import HtmlResponse

from public_law.models.glossary import GlossaryParseResult
from public_law.spiders.base import BaseGlossarySpider

import public_law.parsers.can.doj_glossaries as parser


class DojGlossaries(BaseGlossarySpider):
    name       = "can_doj_glossaries"
    start_urls = parser.configured_urls()


    def parse_glossary(self, response: HtmlResponse) -> GlossaryParseResult:
        """Framework callback which begins the parsing.

        @url https://www.justice.gc.ca/eng/fl-df/parent/mp-fdp/p11.html
        @returns items 1 1
        @returns requests 0 0
        @scrapes metadata entries
        """
        return parser.parse_glossary(response)
