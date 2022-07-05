# SOURCE_URL = 'https://www.uscourts.gov/glossary'
# HTML_TITLE = response.xpath('//title/text()').get()

from typing import cast
from scrapy.http.response.html import HtmlResponse

from ...dates import today
from ...text import NonemptyString as NS
from ...models.glossary import GlossaryParseResult
from ...metadata import Metadata


def parse_glossary(html: HtmlResponse) -> GlossaryParseResult:

    # pyright: reportUnknownMemberType=false
    title = cast(str, html.xpath("//title/text()").get())

    return GlossaryParseResult(
        metadata=Metadata(
            dcterms_title=NS(title),
            dcterms_source=NS("https://www.uscourts.gov/glossary"),
            dcterms_creator="https://public.law",
            publiclaw_sourceModified=today(),
            dcterms_coverage=NS("TBD"),
            dcterms_language="en",
            publiclaw_sourceCreator=NS("https://www.uscourts.gov"),
        ),
        entries=[],
    )
