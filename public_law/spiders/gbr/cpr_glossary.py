from scrapy.http.response.html import HtmlResponse

from ...parsers.gbr.cpr_glossary import parse_glossary
from ...models.glossary import GlossaryParseResult
from ..base import BaseGlossarySpider


class CPRGlossarySpider(BaseGlossarySpider):
    """
    Spider for the UK Criminal Procedure Rules glossary.
    """
    name = "gbr_cpr_glossary"
    start_urls = [
        "https://www.legislation.gov.uk/uksi/2020/759/part/Glossary?view=plain"
    ]

    def parse_glossary(self, response: HtmlResponse) -> GlossaryParseResult:
        """
        Parse the glossary page and return the parsed entries.
        """
        return parse_glossary(response)
