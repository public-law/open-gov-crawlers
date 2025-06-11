from scrapy.http.response.html import HtmlResponse

from public_law.shared.spiders.enhanced_base import EnhancedAutoGlossarySpider
from public_law.shared.models.metadata import Metadata, Subject
from public_law.shared.utils import text
from public_law.shared.utils.text import NonemptyString as String


class USCISGlossary(EnhancedAutoGlossarySpider):
    name       = "usa_uscis_glossary"
    start_urls = ["https://www.uscis.gov/tools/glossary"]

    def get_metadata(self, response: HtmlResponse) -> Metadata:
        """
        Return metadata for the USCIS Glossary.
        """
        source_url = text.URL(response.url)

        subjects = (
                    Subject(text.LoCSubject("sh85042790"), String("Emigration and immigration law")),
                    Subject(text.WikidataTopic("Q231147"),  String("immigration law")), 
                )
        
        return Metadata(
                dcterms_title=String("USCIS Glossary"),
                dcterms_language="en",
                dcterms_coverage="USA",
                # Info about original source
                dcterms_source=source_url,
                publiclaw_sourceModified="unknown",
                publiclaw_sourceCreator=String("U.S. Citizenship and Immigration Services"),
                dcterms_subject=subjects,
            )
