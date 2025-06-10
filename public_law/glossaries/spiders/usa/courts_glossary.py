from scrapy.http.response.html import HtmlResponse

from public_law.shared.spiders.enhanced_base import EnhancedAutoGlossarySpider
from public_law.shared.models.metadata import Metadata
from public_law.glossaries.utils.metadata import us_courts_glossary_metadata


class CourtsGlossary(EnhancedAutoGlossarySpider):
    name       = "usa_courts_glossary"
    start_urls = ["https://www.uscourts.gov/glossary"]
    
    def get_metadata(self, response: HtmlResponse) -> Metadata:
        """Get metadata for the US Courts glossary."""
        return us_courts_glossary_metadata()
