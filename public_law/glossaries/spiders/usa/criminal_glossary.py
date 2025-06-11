from scrapy.http.response.html import HtmlResponse

from public_law.shared.spiders.enhanced_base import EnhancedAutoGlossarySpider
from public_law.shared.models.metadata import Metadata, Subject
from public_law.shared.utils.text import URL, LoCSubject, WikidataTopic
from public_law.shared.utils.text import NonemptyString as String

class CriminalGlossarySpider(EnhancedAutoGlossarySpider):
    """
    Spider for the USA Criminal Glossary from San Diego Superior Court.
    """
    name       = "usa_criminal_glossary"
    start_urls = ["https://www.sdcourt.ca.gov/sdcourt/criminal2/criminalglossary"]

    def get_metadata(self, response: HtmlResponse) -> Metadata:
        source_url = URL(response.url)
        subjects = (
            Subject(LoCSubject("sh85034086"), String("Criminal Procedure")),
            Subject(WikidataTopic("Q146071"), String("Criminal Procedure")),
        )

        return Metadata(
            dcterms_title=String("Criminal Glossary"),
            dcterms_language="en",
            dcterms_coverage="USA",
            dcterms_source=source_url,
            publiclaw_sourceModified="unknown",
            publiclaw_sourceCreator=String(
                "Superior Court of California, County of San Diego"),
            dcterms_subject=subjects,
        ) 
