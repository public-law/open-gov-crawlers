# SOURCE_URL = 'https://www.uscourts.gov/glossary'
# HTML_TITLE = response.xpath('//title/text()').get()

from scrapy.http.response.html import HtmlResponse

from ...dates import today
from ...models.glossary import GlossaryParseResult
from ...metadata import Metadata


def parse_glossary(html: HtmlResponse) -> GlossaryParseResult:

    return GlossaryParseResult(
        metadata=Metadata(
            dcterms_title=html.xpath("//title/text()").get(),
            dcterms_source="TBD",
            dcterms_creator="TBD",
            publiclaw_sourceModified=today(),
            dcterms_coverage="TBD",
            dcterms_language="en",
            publiclaw_sourceCreator="https://www.uscourts.gov",
        ),
        entries=[],
    )
