# -*- coding: utf-8 -*-

from datetime import datetime, date
from oar.items import Chapter, Division
import pytz
import scrapy
import scrapy.exceptions
import scrapy.http
import scrapy.signals
from scrapy import Selector
from titlecase import titlecase
from typing_extensions import Protocol


from oar import items
from oar.parsers import DOMAIN, oar_url, parse_division


class SecureSosStateOrUsSpider(scrapy.Spider):
    name = DOMAIN
    allowed_domains = [DOMAIN]
    start_urls = [oar_url("ruleSearch.action")]

    def __init__(self, *args, **kwargs):
        super(SecureSosStateOrUsSpider, self).__init__(*args, **kwargs)

        # A flag, set after post-processing is finished, to avoid an infinite
        # loop.
        self.data_submitted = False

        # The object to return for conversion to a JSON tree. All the parse
        # methods add their results to this structure.
        self.oar = items.OAR(date_accessed=todays_date(), chapters=[])

    def parse(self, response: scrapy.http.Response):
        """The primary Scrapy callback to begin scraping.

        Kick off scraping by parsing the main OAR page.
        """
        return self.parse_search_page(response)

    def parse_search_page(self, response: scrapy.http.Response):
        """Parse the top-level page.

        The search page contains a list of Chapters, with the names,
        numbers, and internal id's.
        """
        option: Selector
        # TODO: Remove the 'first few' debug limitation.
        for option in response.css("#browseForm option")[0:2]:
            db_id: str = option.xpath("@value").get()
            if db_id == "-1":  # Ignore the heading
                continue

            number, name = map(str.strip, option.xpath(
                "text()").get().split("-", 1))
            chapter = new_chapter(db_id, number, name)

            new_chapter_index = len(self.oar['chapters'])
            self.oar["chapters"].append(chapter)

            request = scrapy.Request(
                chapter["url"], callback=self.parse_chapter_page)
            request.meta["chapter"] = chapter
            request.meta['chapter_index'] = new_chapter_index
            yield request

    def parse_chapter_page(self, response: scrapy.http.Response):
        """Parse a mid-level page.

        A Chapter's page contains a hierarchical list of all its Divisions
        along with their contained Rules.
        """
        # chapter: Chapter = response.meta["chapter"]
        chapter: Chapter = self.oar['chapters'][response.meta['chapter_index']]

        # Collect the Divisions
        anchor: Selector
        for anchor in response.css("#accordion > h3 > a"):
            db_id: str = anchor.xpath("@href").get().split(
                "selectedDivision=")[1]
            raw_number, raw_name = map(
                str.strip, anchor.xpath("text()").get().split("-", 1)
            )
            number = raw_number.split(" ")[1]
            name: str = titlecase(raw_name)
            division = new_division(db_id, number, name)

            chapter['divisions'].append(division)

            # Request a scrape of the Division page
            URL: str = division['url']
            request = scrapy.Request(URL, callback=self.parse_division_page)
            request.meta['division'] = division
            yield request

    def parse_division_page(self, response: scrapy.http.Response):
        division: Division = response.meta['division']
        division['rules'].extend(parse_division(response))

    #
    # Output a single object: a JSON tree containing all the scraped data. This
    # code implements that strategy by registering a signal event listener to
    # execute after all scraping has finished and the data is collected.
    #

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        """Override to register to receive the idle event"""
        spider: SecureSosStateOrUsSpider = super(SecureSosStateOrUsSpider, cls).from_crawler(
            crawler, *args, **kwargs
        )
        crawler.signals.connect(
            spider.spider_idle, signal=scrapy.signals.spider_idle)
        return spider

    def spider_idle(self, spider):
        """Schedule a simple request to return the collected data"""
        if self.data_submitted:
            return

        # This is a hack: I don't yet know how to schedule a request to just
        # submit data _without_ also triggering a scrape. So I provide a URL
        # to a simple site that we're going to ignore.
        null_request = scrapy.Request(
            "https://www.public.law/about-us", callback=self.submit_data)
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


def new_chapter(db_id: str, number: str, name: str):
    return items.Chapter(
        kind="Chapter",
        db_id=db_id,
        number=number,
        name=name,
        url=oar_url(f"displayChapterRules.action?selectedChapter={db_id}"),
        divisions=[],
    )


def new_division(db_id: str, number: str, name: str):
    return items.Division(
        kind="Division",
        db_id=db_id,
        number=number,
        name=name,
        url=oar_url(f"displayDivisionRules.action?selectedDivision={db_id}"),
        rules=[],
    )


class SimpleTimezone(Protocol):
    def localize(self, dt: datetime) -> date:
        ...


def todays_date() -> str:
    mountain: SimpleTimezone = pytz.timezone("US/Mountain")
    fmt = "%Y-%m-%d"
    return mountain.localize(datetime.now()).strftime(fmt)
