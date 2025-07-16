from scrapy.http.response.html import HtmlResponse

from public_law.glossaries.spiders._base.enhanced_base import EnhancedAutoGlossarySpider
from public_law.shared.models.metadata import Metadata, Subject
from public_law.shared.utils.text import URL, LoCSubject, WikidataTopic
from public_law.shared.utils.text import NonemptyString as String



class IRLCourtsGlossary(EnhancedAutoGlossarySpider):
    name       = "irl_courts_glossary"
    start_urls = ["https://www.courts.ie/glossary"]


    def get_metadata(self, response: HtmlResponse) -> Metadata:
        """Generate metadata for the IRL Courts Glossary."""
        source_url = URL(response.url)
        subjects = (
            Subject(LoCSubject("sh85033571"), String("Courts")),
            Subject(WikidataTopic("Q41487"),  String("Court")),
        )
        
        return Metadata(
            dcterms_title=String("Glossary of Legal Terms"),
            dcterms_language="en", 
            dcterms_coverage="IRL",
            # Info about original source
            dcterms_source=source_url,
            publiclaw_sourceModified="unknown",
            publiclaw_sourceCreator=String("The Courts Service of Ireland"),
            dcterms_subject=subjects,
        )
