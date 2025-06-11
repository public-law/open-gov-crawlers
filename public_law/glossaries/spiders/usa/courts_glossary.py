from scrapy.http.response.html import HtmlResponse

from public_law.shared.spiders.enhanced_base import EnhancedAutoGlossarySpider
from public_law.shared.models.metadata import Metadata, Subject
from public_law.shared.utils.text import URL, LoCSubject, NonemptyString as String


class CourtsGlossary(EnhancedAutoGlossarySpider):
    name       = "usa_courts_glossary"
    start_urls = ["https://www.uscourts.gov/glossary"]
    
    def get_metadata(self, response: HtmlResponse) -> Metadata:
        """Get metadata for the US Courts glossary."""
        source_url = URL(response.url)
        subjects = (
            Subject(
                uri=LoCSubject("sh85033575"),
                rdfs_label=String("Courts--United States"),
            ),
            Subject(
                uri=URL("https://www.wikidata.org/wiki/Q194907"),
                rdfs_label=String("United States federal courts"),
            ),
        )
        
        return Metadata(
            dcterms_title=String("Glossary of Legal Terms"),
            dcterms_language="en",
            dcterms_coverage="USA",
            dcterms_source=source_url,
            publiclaw_sourceModified="unknown",
            publiclaw_sourceCreator=String("United States Courts"),
            dcterms_subject=subjects,
        )
