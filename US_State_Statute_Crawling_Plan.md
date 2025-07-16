# Comprehensive Plan: US State Statute Crawling Spiders

## Executive Summary

This plan outlines the development of Scrapy spiders to crawl statutes for 45 US states (excluding California, Colorado, Oregon, New York, and Nevada), following the established architecture patterns in the `open-gov-crawlers` repository.

**Legal Significance**: This project builds on the landmark Supreme Court victory in Georgia v. Public.Resource.Org (2020), where Carl Malamud and Public.Resource.Org successfully defended the public's right to access official legal materials without copyright restrictions. Georgia is prioritized as our first implementation target to honor this victory and demonstrate the principles of open government data access.

## 1. State List and URLs

### 45 Target States

Based on research, here are the 45 states with their official statute website URLs:

| State | Official Statute Website | Code Name |
|-------|-------------------------|-----------|
| Alabama | http://alisondb.legislature.state.al.us/alison/CoA.aspx | Code of Alabama |
| Alaska | http://www.legis.state.ak.us/basis/folio.asp | Alaska Statutes |
| Arizona | http://www.azleg.state.az.us/ArizonaRevisedStatutes.asp | Arizona Revised Statutes |
| Arkansas | https://www.arkleg.state.ar.us/home/FTPDocuments/SessionMeetings/2023/2023R/Public/All.aspx | Arkansas Code |
| Connecticut | https://www.cga.ct.gov/current/pub/titles.htm | Connecticut General Statutes |
| Delaware | https://delcode.delaware.gov/ | Delaware Code |
| Florida | http://www.leg.state.fl.us/Statutes/ | Florida Statutes |
| **Georgia** | https://www.lexisnexis.com/hottopics/gacode/ | **Official Code of Georgia Annotated** ⭐ |
| Hawaii | http://www.capitol.hawaii.gov/hrscurrent/ | Hawaii Revised Statutes |
| Idaho | https://legislature.idaho.gov/statutesrules/idstat/ | Idaho Statutes |
| Illinois | http://www.ilga.gov/legislation/ilcs/ilcs.asp | Illinois Compiled Statutes |
| Indiana | http://iga.in.gov/legislative/laws/current/ic/ | Indiana Code |
| Iowa | https://www.legis.iowa.gov/law/iowaCode | Code of Iowa |
| Kansas | http://www.kslegislature.org/li/b2021_22/statute/ | Kansas Statutes |
| Kentucky | https://apps.legislature.ky.gov/law/statutes/ | Kentucky Revised Statutes |
| Louisiana | https://legis.la.gov/Legis/Laws_Toc.aspx | Louisiana Revised Statutes |
| Maine | http://legislature.maine.gov/statutes/ | Maine Revised Statutes |
| Maryland | http://mgaleg.maryland.gov/mgawebsite/Laws/StatuteText | Maryland Code |
| Massachusetts | https://malegislature.gov/Laws/GeneralLaws | General Laws of Massachusetts |
| Michigan | http://www.legislature.mi.gov/mileg.aspx?page=chapterindex | Michigan Compiled Laws |
| Minnesota | https://www.revisor.mn.gov/statutes/ | Minnesota Statutes |
| Mississippi | https://law.justia.com/codes/mississippi/ | Mississippi Code |
| Missouri | https://revisor.mo.gov/main/Home.aspx | Missouri Revised Statutes |
| Montana | https://leg.mt.gov/bills/mca/ | Montana Code Annotated |
| Nebraska | https://nebraskalegislature.gov/laws/browse-statutes.php | Nebraska Revised Statutes |
| New Hampshire | http://www.gencourt.state.nh.us/rsa/ | New Hampshire Revised Statutes |
| New Jersey | https://lis.njleg.state.nj.us/nxt/gateway.dll | New Jersey Statutes |
| New Mexico | https://nmonesource.com/nmos/nmsa/en/nav.do | New Mexico Statutes Annotated |
| North Carolina | https://www.ncleg.gov/Laws/GeneralStatutes | North Carolina General Statutes |
| North Dakota | https://www.legis.nd.gov/general-information/north-dakota-century-code | North Dakota Century Code |
| Ohio | https://codes.ohio.gov/ohio-revised-code | Ohio Revised Code |
| Oklahoma | http://www.oklegislature.gov/osStatuesTitle.aspx | Oklahoma Statutes |
| Pennsylvania | https://www.legis.state.pa.us/cfdocs/legis/LI/consCheck.cfm | Pennsylvania Consolidated Statutes |
| Rhode Island | http://webserver.rilin.state.ri.us/Statutes/ | Rhode Island General Laws |
| South Carolina | https://www.scstatehouse.gov/code/statmast.php | South Carolina Code of Laws |
| South Dakota | http://sdlegislature.gov/Statutes/ | South Dakota Codified Laws |
| Tennessee | https://www.tn.gov/sos/acts/ | Tennessee Code Annotated |
| Texas | https://statutes.capitol.texas.gov/ | Texas Statutes |
| Utah | https://le.utah.gov/xcode/code.html | Utah Code |
| Vermont | https://legislature.vermont.gov/statutes/ | Vermont Statutes Annotated |
| Virginia | https://law.lis.virginia.gov/vacode/ | Code of Virginia |
| Washington | https://app.leg.wa.gov/RCW/ | Revised Code of Washington |
| West Virginia | http://www.wvlegislature.gov/wvcode/ | West Virginia Code |
| Wisconsin | https://docs.legis.wisconsin.gov/statutes | Wisconsin Statutes |
| Wyoming | https://wyoleg.gov/statutes/ | Wyoming Statutes |

## 2. Repository Architecture Analysis

### Current Patterns Used

1. **Domain Organization**: Legal texts are separated from glossaries under `public_law/legal_texts/`
2. **Spider Base Classes**: Three main patterns:
   - `BaseGlossarySpider` (older pattern)
   - `AutoGlossarySpider` (auto-resolver pattern)
   - `EnhancedAutoGlossarySpider` (recommended new pattern)

3. **Data Models**: 
   - Legal texts use specific models (`CRS`, `OAR`, etc.)
   - Different from glossary models (`GlossaryEntry`, `GlossaryParseResult`)

4. **Parser/Spider Separation**:
   - Parsers: Pure data extraction functions
   - Spiders: Configuration and orchestration

## 3. Data Model Design

### Proposed StatuteEntry Model

```python
# public_law/legal_texts/models/statute.py
from dataclasses import dataclass
from typing import Optional
from public_law.shared.utils.text import NonemptyString, URI

@dataclass(frozen=True)
class StatuteEntry:
    """Represents a single statute section or provision."""
    
    # Core fields
    title: NonemptyString            # e.g., "Title 16" 
    chapter: Optional[NonemptyString]  # e.g., "Chapter 3"
    section: NonemptyString          # e.g., "Section 16-3-101"
    text: NonemptyString             # Full text of the statute
    citation: NonemptyString         # Official citation
    
    # Metadata
    url: URI                         # Source URL
    effective_date: Optional[str]    # When the statute became effective
    last_updated: Optional[str]      # Last modification date
    
    # Hierarchical structure
    part: Optional[NonemptyString]   # Some states use parts
    article: Optional[NonemptyString] # Some states use articles
    subsection: Optional[NonemptyString] # Subsection identifier
    
    kind: str = "StatuteEntry"

@dataclass(frozen=True)
class StatuteParseResult:
    """Collection of all statute entries from a state."""
    
    metadata: Metadata
    entries: tuple[StatuteEntry, ...]
    
    def asdict(self):
        return {
            "metadata": self.metadata.asdict(),
            "entries": [entry.asdict() for entry in self.entries],
        }
```

### Base Spider Class for Statutes

```python
# public_law/legal_texts/spiders/_base/statute_base.py
from typing import Any, Generator
from scrapy import Spider
from scrapy.http.response.html import HtmlResponse
from public_law.legal_texts.models.statute import StatuteParseResult

class BaseStatuteSpider(Spider):
    """Base class for all state statute spiders."""
    
    def parse(self, response: HtmlResponse, **_: dict[str, Any]) -> Generator[dict[str, Any], None, None]:
        """Parse the response and yield the result."""
        result = self.parse_statutes(response)
        if not isinstance(result, StatuteParseResult):
            raise TypeError("parse_statutes must return a StatuteParseResult")
        yield result.asdict()
    
    def parse_statutes(self, response: HtmlResponse) -> StatuteParseResult:
        """Parse the statute page and return the result.
        
        This method must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement parse_statutes")

class EnhancedAutoStatuteSpider(BaseStatuteSpider):
    """Enhanced base for new statute spiders with auto-resolution."""
    
    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Validate required attributes at class definition time."""
        super().__init_subclass__(**kwargs)
        
        if cls.__name__ in ('BaseStatuteSpider', 'EnhancedAutoStatuteSpider'):
            return
            
        if not hasattr(cls, 'name') or not getattr(cls, 'name', None):
            raise TypeError(f"{cls.__name__} must define a 'name' class attribute")
            
        if not hasattr(cls, 'start_urls') or not getattr(cls, 'start_urls', None):
            raise TypeError(f"{cls.__name__} must define a 'start_urls' class attribute")
    
    def parse_statutes(self, response: HtmlResponse) -> StatuteParseResult:
        """Auto-resolve parser and combine with metadata."""
        parser_module_path = self._resolve_parser_module()
        parser_module = importlib.import_module(parser_module_path)
        
        if not hasattr(parser_module, 'parse_statute_entries'):
            raise AttributeError(
                f"Parser module {parser_module_path} must have a 'parse_statute_entries' function"
            )
        
        entries = parser_module.parse_statute_entries(response)
        metadata = self.get_metadata(response)
        
        return StatuteParseResult(metadata, entries)
    
    def _resolve_parser_module(self) -> str:
        """Resolve parser module path from spider name."""
        # Convert "usa_alabama_statutes" to "public_law.legal_texts.parsers.usa.alabama_statutes"
        name_parts = self.name.split("_")
        if len(name_parts) < 3:
            raise ValueError(f"Spider name '{self.name}' must follow pattern 'usa_{{state}}_statutes'")
        
        country = name_parts[0]  # usa
        state = name_parts[1]    # alabama
        return f"public_law.legal_texts.parsers.{country}.{state}_statutes"
    
    def get_metadata(self, response: HtmlResponse) -> Metadata:
        """Get metadata for the statutes - must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement get_metadata")
```

## 4. Spider Implementation Strategy

### 4.1 Template Spider Structure

```python
# public_law/legal_texts/spiders/usa/alabama_statutes.py
from scrapy.http.response.html import HtmlResponse
from public_law.legal_texts.spiders._base.statute_base import EnhancedAutoStatuteSpider
from public_law.shared.models.metadata import Metadata, Subject
from public_law.shared.utils.text import URL, NonemptyString as String

class AlabamaStatutes(EnhancedAutoStatuteSpider):
    name = "usa_alabama_statutes"
    start_urls = ["http://alisondb.legislature.state.al.us/alison/CoA.aspx"]
    
    # Scrapy settings specific to this spider
    custom_settings = {
        'DOWNLOAD_DELAY': 1.0,  # Be respectful to state servers
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
    }
    
    def get_metadata(self, response: HtmlResponse) -> Metadata:
        """Get metadata for Alabama statutes."""
        source_url = URL(response.url)
        subjects = (
            Subject(
                uri=URL("https://www.wikidata.org/wiki/Q173919"),
                rdfs_label=String("Alabama"),
            ),
            Subject(
                uri=URL("https://id.loc.gov/authorities/subjects/sh85123392"),
                rdfs_label=String("Statutes"),
            ),
        )
        
        return Metadata(
            dcterms_title=String("Code of Alabama"),
            dcterms_language="en",
            dcterms_coverage="Alabama, USA",
            dcterms_source=source_url,
            publiclaw_sourceModified="unknown",
            publiclaw_sourceCreator=String("Alabama Legislature"),
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
        """Parse the main index page to find all titles."""
        # Extract links to individual titles
        title_links = response.css('a[href*="Title"]::attr(href)').getall()
        
        for link in title_links:
            yield response.follow(
                link,
                callback=self.parse_title_page,
                errback=self.handle_error
            )
    
    def parse_title_page(self, response: HtmlResponse):
        """Parse a title page to find chapters/sections."""
        # This would be implemented based on the specific structure
        # of Alabama's statute website
        pass
    
    def handle_error(self, failure):
        """Handle spider errors gracefully."""
        self.logger.error(f"Request failed: {failure.request.url}")
        self.logger.error(f"Error: {failure.value}")
```

### 4.2 Parser Implementation

```python
# public_law/legal_texts/parsers/usa/alabama_statutes.py
from typing import tuple
from scrapy.http.response.html import HtmlResponse
from bs4 import BeautifulSoup
from public_law.legal_texts.models.statute import StatuteEntry
from public_law.shared.utils.html import from_response
from public_law.shared.utils.text import NonemptyString, normalize_whitespace

def parse_statute_entries(response: HtmlResponse) -> tuple[StatuteEntry, ...]:
    """Parse statute entries from Alabama statutes page."""
    soup = from_response(response)
    entries = []
    
    # Implementation would depend on the specific HTML structure
    # of Alabama's statute pages
    for section_element in soup.find_all('div', class_='statute-section'):
        try:
            entry = _parse_single_section(section_element, response.url)
            if entry:
                entries.append(entry)
        except Exception as e:
            # Log but continue processing other sections
            logger.warning(f"Failed to parse section: {e}")
            continue
    
    return tuple(entries)

def _parse_single_section(element, base_url: str) -> StatuteEntry | None:
    """Parse a single statute section element."""
    # Extract section number
    section_num = element.find('span', class_='section-number')
    if not section_num:
        return None
    
    # Extract section text
    section_text = element.find('div', class_='section-text')
    if not section_text:
        return None
    
    # Extract other metadata...
    
    return StatuteEntry(
        title=NonemptyString("Title X"),  # Would be extracted
        chapter=None,  # Would be extracted if present
        section=NonemptyString(normalize_whitespace(section_num.get_text())),
        text=NonemptyString(normalize_whitespace(section_text.get_text())),
        citation=NonemptyString(f"Ala. Code § {section_num.get_text()}"),
        url=base_url,
        effective_date=None,
        last_updated=None,
        part=None,
        article=None,
        subsection=None,
    )
```

## 5. State Categorization by Difficulty

### Tier 1: High Priority (Easy + Legally Significant)
**Priority: Implement first**
- **Georgia Code (HIGH PRIORITY)** - Following Georgia v. Public.Resource.Org Supreme Court victory (2020), Georgia's official legal code is now freely accessible without copyright restrictions. This represents a landmark win for public access to legal materials, and crawling Georgia's statutes supports the open government data movement that Carl Malamud championed.
- Florida Statutes (clean HTML structure)
- Utah Code (modern website)
- Virginia Code (well-structured)
- Washington RCW (clean format)
- Wisconsin Statutes (organized HTML)

### Tier 2: Moderate (some JavaScript, but crawlable)
- Illinois Compiled Statutes
- Ohio Revised Code
- Michigan Compiled Laws
- North Carolina General Statutes
- Texas Statutes

### Tier 3: Complex (JavaScript-heavy, CAPTCHAs, complex navigation)
- Maryland Code
- New Jersey Statutes
- Pennsylvania Consolidated Statutes
- Some states with vendor-hosted solutions

## 6. Scrapy Configuration

### 6.1 Settings Integration

Update `public_law/settings.py`:

```python
SPIDER_MODULES = [
    "public_law.glossaries.spiders",
    "public_law.legal_texts.spiders" 
]

# State-specific settings
STATE_SPIDER_SETTINGS = {
    'DOWNLOAD_DELAY': 1.0,  # Default for state sites
    'CONCURRENT_REQUESTS_PER_DOMAIN': 2,  # Be respectful
    'RANDOMIZE_DOWNLOAD_DELAY': True,
    'ROBOTSTXT_OBEY': True,
}

# Override for specific states if needed
CUSTOM_SPIDER_SETTINGS = {
    'usa_georgia_statutes': {
        'DOWNLOAD_DELAY': 2.0,  # LexisNexis might need slower crawling
    },
    'usa_pennsylvania_statutes': {
        'DOWNLOAD_DELAY': 1.5,
    }
}
```

### 6.2 Middleware for State Crawling

```python
# public_law/middlewares.py (addition)
class StateStatuteMiddleware:
    """Custom middleware for state statute crawling."""
    
    def process_request(self, request, spider):
        """Add User-Agent and headers for state sites."""
        if hasattr(spider, 'name') and 'statutes' in spider.name:
            request.headers.setdefault('User-Agent', 
                'Mozilla/5.0 (compatible; PublicLawBot/1.0; +https://public.law)')
            request.headers.setdefault('Accept', 
                'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    
    def process_response(self, request, response, spider):
        """Handle common response issues."""
        if response.status == 429:  # Rate limited
            spider.logger.warning(f"Rate limited on {request.url}")
            # Could implement retry logic
        return response
```

## 7. Error Handling and Robustness

### 7.1 Common Issues and Solutions

```python
# public_law/legal_texts/spiders/_base/error_handling.py
import scrapy
from scrapy.downloadermiddlewares.retry import RetryMiddleware

class StatuteSpiderErrorHandling:
    """Mixin for common error handling patterns."""
    
    def handle_error(self, failure):
        """Standard error handling for statute spiders."""
        request = failure.request
        
        if failure.check(scrapy.exceptions.HttpError):
            response = failure.value.response
            self.logger.error(f'HTTP {response.status} on {request.url}')
            
        elif failure.check(scrapy.exceptions.DNSLookupError):
            self.logger.error(f'DNS lookup failed for {request.url}')
            
        elif failure.check(scrapy.exceptions.TimeoutError):
            self.logger.error(f'Timeout on {request.url}')
            
        else:
            self.logger.error(f'Unexpected error on {request.url}: {failure.value}')
    
    def is_valid_statute_page(self, response: HtmlResponse) -> bool:
        """Check if response contains valid statute content."""
        # Common checks across states
        if response.status != 200:
            return False
            
        if "404" in response.text or "not found" in response.text.lower():
            return False
            
        # Must contain some statutory text indicators
        statute_indicators = ['section', 'chapter', 'title', 'code', 'statute']
        text_lower = response.text.lower()
        
        return any(indicator in text_lower for indicator in statute_indicators)
```

## 8. Testing Framework

### 8.1 Test Structure

```python
# tests/legal_texts/spiders/usa/alabama_statutes_test.py
import pytest
from scrapy.http.response.html import HtmlResponse
from public_law.legal_texts.spiders.usa.alabama_statutes import AlabamaStatutes

@pytest.fixture
def response():
    """Mock response with Alabama statute HTML."""
    with open("tests/fixtures/usa/alabama-statutes.html", "rb") as f:
        html_content = f.read()
    
    return HtmlResponse(
        url="http://alisondb.legislature.state.al.us/alison/CoA.aspx",
        body=html_content,
        encoding="utf-8",
    )

@pytest.fixture
def spider():
    """Create Alabama statutes spider instance."""
    return AlabamaStatutes()

class TestAlabamaStatutes:
    def test_spider_name(self, spider):
        assert spider.name == "usa_alabama_statutes"
    
    def test_start_urls(self, spider):
        assert len(spider.start_urls) > 0
        assert all(url.startswith('http') for url in spider.start_urls)
    
    def test_metadata_generation(self, spider, response):
        metadata = spider.get_metadata(response)
        assert metadata.dcterms_title == "Code of Alabama"
        assert metadata.dcterms_language == "en"
        assert metadata.dcterms_coverage == "Alabama, USA"
    
    def test_parse_statutes(self, spider, response):
        result = spider.parse_statutes(response)
        assert len(result.entries) > 0
        
        # Test first entry structure
        entry = result.entries[0]
        assert entry.title
        assert entry.section
        assert entry.text
        assert entry.citation
```

### 8.2 Integration Testing

```python
# tests/legal_texts/integration/test_state_spiders.py
import pytest
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class TestStatuteSpiderIntegration:
    """Integration tests for state statute spiders."""
    
    @pytest.mark.slow
    def test_alabama_spider_runs(self):
        """Test that Alabama spider can run without errors."""
        settings = get_project_settings()
        process = CrawlerProcess(settings)
        
        # Run spider with limited pages for testing
        process.crawl('usa_alabama_statutes', limit_pages=5)
        process.start()
```

## 9. Deployment and Monitoring

### 9.1 Spider Running Scripts

```bash
# script/run-state-statute-spiders
#!/usr/bin/env bash

set -e

OUTPUT_DIR="../statute-datasets"
SPIDERS=$(poetry run scrapy list | grep "usa_.*_statutes")

for spider in $SPIDERS; do
    OUTPUT_FILE="${OUTPUT_DIR}/${spider}.json"
    
    if [ -f ${OUTPUT_FILE} ]; then
        echo "Skipping ${spider} because output already exists."
        continue
    fi
    
    echo "Running ${spider}..."
    poetry run scrapy crawl --output ${OUTPUT_FILE} $spider
    
    # Add delay between spiders to be respectful
    sleep 30
done
```

### 9.2 Monitoring and Alerting

```python
# public_law/monitors.py (addition)
from spidermon import Monitor, MonitorSuite, monitors

@monitors.name('State Statute Spider Monitor')
class StateStatuteSpiderMonitor(Monitor):
    
    @monitors.name('Minimum entries extracted')
    def test_minimum_entries(self):
        """Ensure minimum number of statute entries were extracted."""
        expected_minimums = {
            'usa_alabama_statutes': 1000,
            'usa_florida_statutes': 2000,
            # ... other states
        }
        
        spider_name = self.data.stats.get('spider_name')
        if spider_name in expected_minimums:
            entries_count = self.data.stats.get('item_scraped_count', 0)
            minimum = expected_minimums[spider_name]
            
            self.assertGreaterEqual(
                entries_count, 
                minimum,
                f'{spider_name} extracted {entries_count} entries, expected at least {minimum}'
            )
```

## 10. Workflow for Adding New State Spiders

### Step-by-Step Process:

1. **Research Phase**:
   ```bash
   # Create research document
   mkdir -p docs/state_research
   touch docs/state_research/alabama_analysis.md
   ```

2. **Spider Creation**:
   ```bash
   # Create spider file
   touch public_law/legal_texts/spiders/usa/alabama_statutes.py
   
   # Create parser file
   touch public_law/legal_texts/parsers/usa/alabama_statutes.py
   
   # Create test files
   touch tests/legal_texts/spiders/usa/alabama_statutes_test.py
   touch tests/legal_texts/parsers/usa/alabama_statutes_test.py
   ```

3. **Fixture Collection**:
   ```bash
   # Download sample HTML for testing
   curl "http://example-alabama-statute-url" > tests/fixtures/usa/alabama-statutes.html
   ```

4. **Testing**:
   ```bash
   # Run parser tests first
   poetry run pytest tests/legal_texts/parsers/usa/alabama_statutes_test.py
   
   # Run spider tests
   poetry run pytest tests/legal_texts/spiders/usa/alabama_statutes_test.py
   
   # Integration test
   poetry run scrapy crawl usa_alabama_statutes -s CLOSESPIDER_PAGECOUNT=10
   ```

5. **Documentation**:
   - Update README.md with new spider
   - Add to state tracking spreadsheet
   - Document any special considerations

## 11. Example Implementation: Florida Statutes

### 11.1 Spider Implementation

```python
# public_law/legal_texts/spiders/usa/florida_statutes.py
from scrapy.http.response.html import HtmlResponse
from public_law.legal_texts.spiders._base.statute_base import EnhancedAutoStatuteSpider
from public_law.shared.models.metadata import Metadata, Subject
from public_law.shared.utils.text import URL, NonemptyString as String

class FloridaStatutes(EnhancedAutoStatuteSpider):
    name = "usa_florida_statutes"
    start_urls = ["http://www.leg.state.fl.us/Statutes/index.cfm?Tab=statutes&submenu=1"]
    
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
```

## 12. Priority Implementation Schedule

### Phase 1 (Months 1-2): Foundation and Tier 1 States
1. Implement base classes and data models
2. Create testing framework
3. Implement 6 Tier 1 states with **Georgia as top priority** (Georgia, Florida, Utah, Virginia, Washington, Wisconsin)

### Phase 2 (Months 3-4): Tier 2 States  
1. Implement 10 Tier 2 states
2. Refine error handling and monitoring
3. Optimize performance and reliability

### Phase 3 (Months 5-6): Tier 3 States and Polish
1. Implement remaining complex states
2. Handle JavaScript-heavy sites (potentially with Splash/Selenium)
3. Final testing and documentation

### Phase 4 (Month 7): Integration and Deployment
1. Full integration testing
2. Production deployment
3. Monitoring setup
4. Documentation completion

## 13. Success Metrics

- **Coverage**: Successfully crawl all 45 states
- **Data Quality**: Minimum 90% of statutes captured per state
- **Reliability**: 95% uptime for spider runs
- **Performance**: Complete full crawl of all states within 48 hours
- **Maintainability**: Clear documentation and test coverage > 80%

## 14. Risk Mitigation

1. **Website Changes**: Implement monitoring for structure changes
2. **Rate Limiting**: Respectful crawling with proper delays (especially important for Georgia given the legal precedent)
3. **Legal Compliance**: Follow robots.txt and terms of service. **Georgia Note**: The Georgia v. Public.Resource.Org Supreme Court decision establishes legal precedent for public access to official legal materials, but we maintain respectful crawling practices.
4. **Data Validation**: Comprehensive testing and validation
5. **Backup Plans**: Manual fallbacks for critical states
6. **Legal Precedent**: Document compliance with Georgia v. Public.Resource.Org decision for transparency and legal defensibility

This comprehensive plan provides a roadmap for systematically implementing statute crawling spiders for all 45 target states while maintaining code quality and following the established repository patterns. 

**Acknowledgment**: This work builds upon the pioneering efforts of Carl Malamud and Public.Resource.Org in defending public access to legal materials. The Georgia v. Public.Resource.Org Supreme Court victory represents a landmark achievement for open government data, and this project aims to honor that legacy by making state statutes freely accessible to all.
