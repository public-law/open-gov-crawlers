# pyright: reportUnknownVariableType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownMemberType=false
# pyright: reportUninitializedInstanceVariable=false
# pyright: reportPrivateUsage=false
# pyright: reportUnknownVariableType=false
# pyright: reportGeneralTypeIssues=false

from typing import Any, Dict, List

from scrapy import Spider
from scrapy.selector.unified import Selector
from scrapy.crawler import Crawler
import scrapy.exceptions
from scrapy.http.response import Response
from scrapy.http.request import Request
import scrapy.signals
from titlecase import titlecase

from public_law import items
from public_law.items import Chapter, Division
from public_law.parsers.usa.oregon import DOMAIN, oar_url, parse_division
from public_law.dates import todays_date


JD_VERBOSE_NAME = "USA / Oregon"
PUBLICATION_NAME = "Oregon Administrative Rules"


class OregonRegs(Spider):
    name = "usa_or_regs"
    allowed_domains = [DOMAIN]
    start_urls = [oar_url("ruleSearch.action")]

    def __init__(self, *args: List[str], **kwargs: Dict[str, Any]):
        super().__init__(*args, **kwargs)

        # A flag, set after post-processing is finished, to avoid an infinite
        # loop.
        self.data_submitted = False

        # The object to return for conversion to a JSON tree. All the parse
        # methods add their results to this structure.
        self.oar = items.OAR(date_accessed=todays_date(), chapters=[])

    def parse(self, response: Response, **_kwargs: Dict[str, Any]):
        """The primary Scrapy callback to begin scraping.

        Kick off scraping by parsing the main OAR page.
        """
        return self.parse_search_page(response)

    def parse_search_page(self, response: Response):
        """Parse the top-level page.

        The search page contains a list of Chapters, with the names,
        numbers, and internal id's.
        """
        for option in response.css("#browseForm option"):
            db_id: Any = option.xpath("@value").get()
            if db_id == "-1":  # Ignore the heading
                continue

            number, name = map(str.strip, option.xpath("text()").get().split("-", 1))
            chapter = new_chapter(db_id, number, name)

            new_chapter_index = len(self.oar["chapters"])
            self.oar["chapters"].append(chapter)

            request = Request(chapter["url"], callback=self.parse_chapter_page)
            request.meta["chapter_index"] = new_chapter_index
            yield request

    def parse_chapter_page(self, response: Response):
        """Parse a mid-level page.

        A Chapter's page contains a hierarchical list of all its Divisions
        along with their contained Rules.
        """
        chapter: Chapter = self.oar["chapters"][response.meta["chapter_index"]]

        # Collect the Divisions
        anchor: Selector
        for anchor in response.css("#accordion > h3 > a"):
            db_id: str = anchor.xpath("@href").get().split("selectedDivision=")[1]
            raw_number, raw_name = map(
                str.strip, anchor.xpath("text()").get().split("-", 1)
            )
            number = raw_number.split(" ")[1]
            name: str = titlecase(raw_name)
            division = new_division(db_id, number, name)

            chapter["divisions"].append(division)

            # Request a scrape of the Division page
            request = Request(division["url"], callback=self.parse_division_page)
            request.meta["division_index"] = len(chapter["divisions"]) - 1
            request.meta["chapter_index"] = response.meta["chapter_index"]
            yield request

    def parse_division_page(self, response: Response):
        chapter: Chapter = self.oar["chapters"][response.meta["chapter_index"]]
        division: Division = chapter["divisions"][response.meta["division_index"]]

        division["rules"].extend(parse_division(response))

    #
    # Output a single object: a JSON tree containing all the scraped data. This
    # code implements that strategy by registering a signal event listener to
    # execute after all scraping has finished and the data is collected.
    #

    @classmethod
    def from_crawler(cls, crawler: Crawler, *args: List[str], **kwargs: Dict[str, Any]):
        """Override to register to receive the idle event"""
        spider: OregonRegs = super(OregonRegs, cls).from_crawler(
            crawler, *args, **kwargs
        )
        crawler.signals.connect(spider.spider_idle, signal=scrapy.signals.spider_idle)
        return spider

    def spider_idle(self, spider: Spider):
        """Schedule a simple request to return the collected data"""
        if self.data_submitted:
            return

        # This is a hack: I don't yet know how to schedule a request to just
        # submit data _without_ also triggering a scrape. So I provide a URL
        # to a simple site that we're going to ignore.
        null_request = Request(
            "https://www.public.law/about-us", callback=self.submit_data
        )
        self.crawler.engine.schedule(null_request, spider)
        raise scrapy.exceptions.DontCloseSpider

    def submit_data(self, _):
        """Simply return the collection of all the scraped data.

        Ignore the actual scraped content. I haven't figured out another
        way to submit the merged results. To be used as a callback when
        the spider is idle (i.e., has finished scraping.)
        """
        self.data_submitted = True
        yield self.oar


def new_chapter(db_id: str, number: str, name: str) -> Chapter:
    return items.Chapter(
        kind="Chapter",
        db_id=db_id,
        number=number,
        name=name,
        url=oar_url(f"displayChapterRules.action?selectedChapter={db_id}"),
        divisions=[],
    )


def new_division(db_id: str, number: str, name: str) -> Division:
    return items.Division(
        kind="Division",
        db_id=db_id,
        number=number,
        name=name,
        url=oar_url(f"displayDivisionRules.action?selectedDivision={db_id}"),
        rules=[],
    )
