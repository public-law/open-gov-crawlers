from scrapy.http.response.html import HtmlResponse
from ...models.glossary import GlossaryEntry, GlossaryParseResult, reading_ease


def parse_glossary(html: HtmlResponse) -> GlossaryParseResult:
    pass
