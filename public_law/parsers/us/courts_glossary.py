# SOURCE_URL = 'https://www.uscourts.gov/glossary'
# HTML_TITLE = response.xpath('//title/text()').get()

from dataclasses import dataclass

from scrapy.http.response.html import HtmlResponse

from public_law.metadata import Metadata


@dataclass(frozen=True)
class GlossaryEntry:
    ...


@dataclass(frozen=True)
class GlossarySourceParseResult:
    metadata: Metadata
    entries: list[GlossaryEntry]


def parse_glossary(html: HtmlResponse) -> GlossarySourceParseResult:
    raise NotImplementedError()
