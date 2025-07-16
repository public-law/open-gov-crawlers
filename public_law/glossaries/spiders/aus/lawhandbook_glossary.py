from scrapy.http.response.html import HtmlResponse

from public_law.glossaries.spiders._base.enhanced_base import EnhancedAutoGlossarySpider
from public_law.shared.models.metadata import Metadata, Subject
from public_law.shared.utils.text import URL, LoCSubject
from public_law.shared.utils.text import NonemptyString as String



class LawHandbookGlossary(EnhancedAutoGlossarySpider):
    name       = "aus_lawhandbook_glossary"
    start_urls = ["https://lawhandbook.sa.gov.au/go01.php"]


    def get_metadata(self, response: HtmlResponse) -> Metadata:
        """
        Generate metadata for the Australia Law Handbook Glossary.
        
        This Glossary defies the planned subject tagging scheme
        because it has terms from a wide variety of areas of law.
        """
        source_url = URL(response.url)
        subjects = (
            Subject(
                uri=LoCSubject("sh85075720"),
                rdfs_label=String("Legal aid"),
            ),
            Subject(
                uri=URL("https://www.wikidata.org/wiki/Q707748"),
                rdfs_label=String("Legal aid"),
            ),
        )

        return Metadata(
            dcterms_title=String("Law Handbook Glossary"),
            dcterms_language="en",
            dcterms_coverage="AUS",
            # Info about original source
            dcterms_source=source_url,
            publiclaw_sourceModified="unknown",
            publiclaw_sourceCreator=String("Legal Services Commission of South Australia"),
            dcterms_subject=subjects,
        )
