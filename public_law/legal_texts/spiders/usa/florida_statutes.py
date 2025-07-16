import scrapy
from scrapy.http.response.html import HtmlResponse

from public_law.legal_texts.spiders._base.statute_base import EnhancedAutoStatuteSpider
from public_law.shared.models.metadata import Metadata, Subject
from public_law.shared.utils.text import URL, NonemptyString as String


class FloridaStatutes(EnhancedAutoStatuteSpider):
    """Spider for Florida Statutes.
    
    Crawls the Florida Legislature's statute database to extract
    all statutory provisions organized by title and chapter.
    """
    name = "usa_florida_statutes"
    start_urls = ["http://www.leg.state.fl.us/Statutes/index.cfm?Tab=statutes&submenu=1"]
    
    # Scrapy settings specific to this spider
    custom_settings = {
        'DOWNLOAD_DELAY': 1.0,  # Be respectful to state servers
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
    }
    
    def get_metadata(self, response: HtmlResponse) -> Metadata:
        """Get metadata for Florida statutes."""
        source_url = URL(response.url)
        subjects = (
            Subject(
                uri=URL("https://www.wikidata.org/wiki/Q812"),
                rdfs_label=String("Florida"),
            ),
            Subject(
                uri=URL("https://id.loc.gov/authorities/subjects/sh85123392"),
                rdfs_label=String("Statutes"),
            ),
            Subject(
                uri=URL("https://id.loc.gov/authorities/subjects/sh85075851"),
                rdfs_label=String("Law--Florida"),
            ),
        )
        
        return Metadata(
            dcterms_title=String("Florida Statutes"),
            dcterms_language="en",
            dcterms_coverage="Florida, USA",
            dcterms_source=source_url,
            publiclaw_sourceModified="unknown",
            publiclaw_sourceCreator=String("Florida Legislature"),
            dcterms_subject=subjects,
        )
    
    def start_requests(self):
        """Generate initial requests with proper error handling."""
        for url in self.start_urls:
            yield scrapy.Request(
                url, 
                callback=self.parse_title_index,
                errback=self.handle_error,
                meta={'dont_cache': True}
            )
    
    def parse_title_index(self, response: HtmlResponse):
        """Parse the main statute index page to find all titles."""
        # Extract links to individual titles
        # Florida organizes statutes by Title (e.g., Title I, Title II, etc.)
        title_links = response.css('a[href*="Title"]::attr(href)').getall()
        
        for link in title_links:
            yield response.follow(
                link,
                callback=self.parse_title_page,
                errback=self.handle_error,
                meta={'title_link': link}
            )
    
    def parse_title_page(self, response: HtmlResponse):
        """Parse a title page to find all chapters within that title."""
        # Extract chapter links from the title page
        chapter_links = response.css('a[href*="Chapter"]::attr(href)').getall()
        
        for link in chapter_links:
            yield response.follow(
                link,
                callback=self.parse_chapter_page,
                errback=self.handle_error,
                meta={
                    'title_link': response.meta.get('title_link'),
                    'chapter_link': link
                }
            )
    
    def parse_chapter_page(self, response: HtmlResponse):
        """Parse a chapter page to find all sections within that chapter."""
        # Extract section links from the chapter page
        section_links = response.css('a[href*="Section"]::attr(href)').getall()
        
        for link in section_links:
            yield response.follow(
                link,
                callback=self.parse_section_page,
                errback=self.handle_error,
                meta={
                    'title_link': response.meta.get('title_link'),
                    'chapter_link': response.meta.get('chapter_link'),
                    'section_link': link
                }
            )
    
    def parse_section_page(self, response: HtmlResponse):
        """Parse individual statute sections - this calls the parser."""
        # This method will automatically call the parser and return structured data
        return self.parse_statutes(response)
    
    def handle_error(self, failure):
        """Handle spider errors gracefully."""
        self.logger.error(f"Request failed: {failure.request.url}")
        self.logger.error(f"Error: {failure.value}")
        
        # Log the failure but don't stop the spider
        if hasattr(failure, 'request'):
            self.logger.info(f"Failed URL: {failure.request.url}")