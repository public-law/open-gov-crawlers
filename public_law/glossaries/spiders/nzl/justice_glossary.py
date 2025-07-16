from scrapy.http.response.html import HtmlResponse

from public_law.glossaries.spiders._base.enhanced_base import EnhancedAutoGlossarySpider
from public_law.shared.models.metadata import Metadata, Subject
from public_law.shared.utils.text import URL, LoCSubject
from public_law.shared.utils.text import NonemptyString as String

class JusticeGlossarySpider(EnhancedAutoGlossarySpider):
    """
    Spider for the New Zealand Ministry of Justice glossary.
    """
    name       = "nzl_justice_glossary"
    start_urls = ["https://www.justice.govt.nz/about/glossary/"]

    def get_metadata(self, response: HtmlResponse) -> Metadata:
        source_url = URL(response.url)
        subjects = (
            Subject(
                uri=LoCSubject("sh85071120"),
                rdfs_label=String("Justice, Administration of"),
            ),
            Subject(
                uri=URL("https://www.wikidata.org/wiki/Q16514399"),
                rdfs_label=String("Administration of justice"),
            ),
        )

        return Metadata(
            dcterms_title=String("Glossary"),
            dcterms_language="en",
            dcterms_coverage="NZL",
            dcterms_source=source_url,
            publiclaw_sourceModified="unknown",
            publiclaw_sourceCreator=String("New Zealand Ministry of Justice"),
            dcterms_subject=subjects,
        )
