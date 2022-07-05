# SOURCE_URL = 'https://www.uscourts.gov/glossary'
# HTML_TITLE = response.xpath('//title/text()').get()

from typing import cast
from scrapy.http.response.html import HtmlResponse

from ...text import NonemptyString as NS
from ...models.glossary import GlossaryParseResult
from ...metadata import Metadata


def parse_glossary(html: HtmlResponse) -> GlossaryParseResult:

    # pyright: reportUnknownMemberType=false
    return GlossaryParseResult(
        metadata=Metadata(
            dcterms_title=NS("Glossary of Legal Terms"),
            dcterms_language="en",
            dcterms_coverage=NS("USA"),
            # Info about original source
            dcterms_source=NS("https://www.uscourts.gov/glossary"),
            publiclaw_sourceModified="unknown",
            publiclaw_sourceCreator=NS("United States Courts"),
        ),
        entries=[],
    )
