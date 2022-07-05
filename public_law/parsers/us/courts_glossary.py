# SOURCE_URL = 'https://www.uscourts.gov/glossary'
# HTML_TITLE = response.xpath('//title/text()').get()

from scrapy.http.response.html import HtmlResponse

from ...dates import today
from ...text import NonemptyString as NS
from ...models.glossary import GlossaryParseResult
from ...metadata import Metadata


def parse_glossary(html: HtmlResponse) -> GlossaryParseResult:

    return GlossaryParseResult(
        metadata=Metadata(
            dcterms_title=NS(html.xpath("//title/text()").get()),
            dcterms_source=NS("https://www.uscourts.gov/glossary"),
            dcterms_creator="TBD",
            publiclaw_sourceModified=today(),
            dcterms_coverage=NS("TBD"),
            dcterms_language="en",
            publiclaw_sourceCreator=NS("https://www.uscourts.gov"),
        ),
        entries=[],
    )
