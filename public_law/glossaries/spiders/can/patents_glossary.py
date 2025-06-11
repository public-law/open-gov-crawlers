from scrapy.http.response.html import HtmlResponse

from public_law.shared.spiders.enhanced_base import EnhancedAutoGlossarySpider
from public_law.shared.models.metadata import Metadata, Subject
from public_law.shared.utils.text import URL, LoCSubject, WikidataTopic
from public_law.shared.utils.text import NonemptyString as String


class PatentsGlossarySpider(EnhancedAutoGlossarySpider):
    name       = "can_patents_glossary"
    start_urls = ["https://ised-isde.canada.ca/site/canadian-intellectual-property-office/en/patents/glossary"]

    def get_metadata(self, response: HtmlResponse) -> Metadata:
        """Get metadata for the Canada Patents Glossary."""
        source_url = URL(response.url)
        subjects = (
            Subject(LoCSubject("sh85098655"), String("Patents")),
            Subject(WikidataTopic("Q3039731"), String("Patent Law")),
        )

        return Metadata(
            dcterms_title=String("Canadian Patent Glossary"),
            dcterms_language="en",
            dcterms_coverage="CAN",
            # Info about original source
            dcterms_source=source_url,
            publiclaw_sourceModified="unknown",
            publiclaw_sourceCreator=String(
                "Canadian Intellectual Property Office"),
            dcterms_subject=subjects,
        )
