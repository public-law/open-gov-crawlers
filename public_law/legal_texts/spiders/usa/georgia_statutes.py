import scrapy
from scrapy.http.response.html import HtmlResponse

from public_law.legal_texts.spiders._base.statute_base import EnhancedAutoStatuteSpider
from public_law.shared.models.metadata import Metadata, Subject
from public_law.shared.utils.text import URL, NonemptyString as String


class GeorgiaStatutes(EnhancedAutoStatuteSpider):
    """Spider for Georgia Code - Official Code of Georgia Annotated.
    
    HIGH PRIORITY: This spider honors the landmark Supreme Court victory in 
    Georgia v. Public.Resource.Org (2020), where Carl Malamud and Public.Resource.Org
    successfully defended the public's right to access official legal materials 
    without copyright restrictions.
    
    Following this victory, Georgia's official legal code is now freely accessible,
    making this a high-priority target for open government data collection.
    """
    name = "usa_georgia_statutes"
    start_urls = ["https://www.lexisnexis.com/hottopics/gacode/"]
    
    # Scrapy settings specific to this spider - more conservative for LexisNexis
    custom_settings = {
        'DOWNLOAD_DELAY': 2.0,  # Slower for vendor-hosted site
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,  # Very conservative
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'COOKIES_ENABLED': True,  # May be needed for LexisNexis
        'USER_AGENT': 'Mozilla/5.0 (compatible; PublicLawBot/1.0; +https://public.law; Georgia-v-PRO-compliance)',
    }
    
    def get_metadata(self, response: HtmlResponse) -> Metadata:
        """Get metadata for Georgia statutes with historical context."""
        source_url = URL(response.url)
        subjects = (
            Subject(
                uri=URL("https://www.wikidata.org/wiki/Q1428"),
                rdfs_label=String("Georgia (U.S. state)"),
            ),
            Subject(
                uri=URL("https://id.loc.gov/authorities/subjects/sh85123392"),
                rdfs_label=String("Statutes"),
            ),
            Subject(
                uri=URL("https://id.loc.gov/authorities/subjects/sh85076240"),
                rdfs_label=String("Law--Georgia"),
            ),
            Subject(
                uri=URL("https://www.wikidata.org/wiki/Q7231"),
                rdfs_label=String("Public domain"),
            ),
        )
        
        return Metadata(
            dcterms_title=String("Official Code of Georgia Annotated"),
            dcterms_language="en",
            dcterms_coverage="Georgia, USA",
            dcterms_source=source_url,
            publiclaw_sourceModified="unknown",
            publiclaw_sourceCreator=String("Georgia General Assembly"),
            dcterms_subject=subjects,
            # Note: Following Georgia v. Public.Resource.Org (2020) Supreme Court decision
            dcterms_rights=String("Public Domain - Georgia v. Public.Resource.Org, 590 U.S. ___ (2020)"),
        )
    
    def start_requests(self):
        """Generate initial requests with enhanced error handling for LexisNexis."""
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'https://www.lexisnexis.com/',
        }
        
        for url in self.start_urls:
            yield scrapy.Request(
                url, 
                callback=self.parse_title_index,
                errback=self.handle_error,
                headers=headers,
                meta={
                    'dont_cache': True,
                    'priority': 10,  # High priority for Georgia
                }
            )
    
    def parse_title_index(self, response: HtmlResponse):
        """Parse the main Georgia Code index page to find all titles.
        
        LexisNexis structure may be different from direct state sites,
        so we need to be flexible in our parsing approach.
        """
        # Look for title links in LexisNexis format
        title_selectors = [
            'a[href*="Title"]',
            'a[href*="title"]',
            'a[href*="T"]',  # Some sites use T1, T2, etc.
            '.title-link',
            '[data-title]',
        ]
        
        title_links = []
        for selector in title_selectors:
            links = response.css(f'{selector}::attr(href)').getall()
            title_links.extend(links)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_title_links = []
        for link in title_links:
            if link not in seen:
                seen.add(link)
                unique_title_links.append(link)
        
        if not unique_title_links:
            self.logger.warning(f"No title links found on {response.url}")
            # Fallback: look for any links that might lead to statutes
            all_links = response.css('a::attr(href)').getall()
            potential_links = [link for link in all_links 
                             if any(term in link.lower() for term in ['code', 'statute', 'law', 'title', 'chapter'])]
            unique_title_links = potential_links[:20]  # Limit to avoid too many requests
        
        for link in unique_title_links:
            yield response.follow(
                link,
                callback=self.parse_title_page,
                errback=self.handle_error,
                meta={'title_link': link}
            )
    
    def parse_title_page(self, response: HtmlResponse):
        """Parse a title page to find all chapters within that title."""
        # Similar flexible approach for chapter links
        chapter_selectors = [
            'a[href*="Chapter"]',
            'a[href*="chapter"]',
            'a[href*="Ch"]',
            '.chapter-link',
            '[data-chapter]',
        ]
        
        chapter_links = []
        for selector in chapter_selectors:
            links = response.css(f'{selector}::attr(href)').getall()
            chapter_links.extend(links)
        
        # Remove duplicates
        unique_chapter_links = list(dict.fromkeys(chapter_links))
        
        for link in unique_chapter_links:
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
        # Flexible approach for section links
        section_selectors = [
            'a[href*="Section"]',
            'a[href*="section"]',
            'a[href*="Sec"]',
            'a[href*="-"]',  # Georgia sections often use format like "16-1-1"
            '.section-link',
            '[data-section]',
        ]
        
        section_links = []
        for selector in section_selectors:
            links = response.css(f'{selector}::attr(href)').getall()
            section_links.extend(links)
        
        # Filter to likely section links (containing numbers and hyphens)
        import re
        likely_sections = []
        for link in section_links:
            if re.search(r'\d+[-\d]+', link):  # Contains number patterns like "16-1-1"
                likely_sections.append(link)
        
        # Remove duplicates
        unique_section_links = list(dict.fromkeys(likely_sections))
        
        for link in unique_section_links[:50]:  # Limit to avoid overwhelming the server
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
        """Parse individual statute sections.
        
        This calls the auto-resolved parser to extract StatuteEntry objects.
        """
        # Log the victory for Carl Malamud when we successfully crawl Georgia statutes
        self.logger.info(f"Crawling Georgia statute {response.url} - "
                        f"honoring Georgia v. Public.Resource.Org victory for open legal data")
        
        return self.parse_statutes(response)
    
    def handle_error(self, failure):
        """Enhanced error handling for LexisNexis crawling."""
        self.logger.error(f"Request failed: {failure.request.url}")
        self.logger.error(f"Error: {failure.value}")
        
        # Special handling for LexisNexis-specific errors
        if hasattr(failure, 'response') and failure.response:
            if failure.response.status == 403:
                self.logger.warning("403 Forbidden - may need to adjust headers or add delay")
            elif failure.response.status == 429:
                self.logger.warning("429 Rate Limited - will retry with longer delay")
            elif "lexisnexis" in failure.request.url and failure.response.status >= 400:
                self.logger.warning(f"LexisNexis-specific error {failure.response.status} - "
                                  f"may need to adjust crawling strategy")
        
        # Log the failure but don't stop the spider
        if hasattr(failure, 'request'):
            self.logger.info(f"Failed URL: {failure.request.url}")