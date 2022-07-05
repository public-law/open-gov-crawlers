# SOURCE_URL = 'https://www.uscourts.gov/glossary'
# HTML_TITLE = response.xpath('//title/text()').get()

from scrapy.http.response.html import HtmlResponse

from ...models.glossary import GlossaryParseResult


def parse_glossary(html: HtmlResponse) -> GlossaryParseResult:
    raise NotImplementedError()
