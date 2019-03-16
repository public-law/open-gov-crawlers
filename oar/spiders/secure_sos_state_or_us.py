# -*- coding: utf-8 -*-

import scrapy
from scrapy import signals

from oar import items


class SecureSosStateOrUsSpider(scrapy.Spider):
    name = "secure.sos.state.or.us"
    allowed_domains = ["secure.sos.state.or.us"]
    start_urls = ["https://secure.sos.state.or.us/oard/ruleSearch.action"]


    def __init__(self):
        super()

        # A flag, set after post-processing is finished, to avoid an infinite
        # loop.
        self.data_submitted = False

        # The object to return for conversion to a JSON tree. All the parse
        # methods add their results to this structure.
        self.oar = items.OAR(chapters=[])


    def parse(self, response):
        """The primary Scrapy callback to begin scraping. Kick off scraping by parsing
        the main OAR page.
        """
        return self.parse_search_page(response)


    def parse_search_page(self, response):
        """The search page contains a list of Chapters, with the names,
        numbers, and internal id's."""
        for option in response.css("#browseForm option"):
            db_id = option.xpath("@value").get()
            if db_id == "-1":  # Ignore the heading
                continue

            number, name = map(str.strip, option.xpath("text()").get().split("-", 1))
            chapter = new_chapter(db_id, number, name)
            self.oar['chapters'].append(chapter)

            request = scrapy.Request(chapter["url"], callback=self.parse_chapter_page)
            request.meta["chapter"] = chapter
            yield request


    def parse_chapter_page(self, response):
        """A Chapter's page contains a hierarchical list of all its Divisions
        along with their contained Rules.
        """
        chapter = response.meta["chapter"]
        division_index = {}

        for anchor in response.css("#accordion > h3 > a"):
            db_id = anchor.xpath("@href").get().split("=")[1]
            number, name = map(str.strip, anchor.xpath("text()").get().split("-", 1))
            number = number.split(" ")[1]
            division = new_division(db_id, number, name)

            chapter["divisions"].append(division)
            division_index[number] = division



    #
    # Output a single object: a JSON tree containing all the scraped data. This
    # code implements that strategy by registering a signal (event) listener to
    # execute after all scraping has finished, and the data is collected.
    #

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        """Register to receive the idle event"""
        spider = super(SecureSosStateOrUsSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
        return spider


    def spider_idle(self, spider):
        """Schedule a simple request in order to return the collected data"""
        if self.data_submitted: return

        null_request = scrapy.Request('http://neverssl.com/', callback=self.submit_data)
        self.crawler.engine.schedule(null_request, spider)
        raise scrapy.exceptions.DontCloseSpider


    def submit_data(self, _):
        """Simply return the collection of all the scraped data. Ignore the actual
        scraped content. I haven't figured out another way to submit the merged
        results.

        To be used as a callback when the spider is idle (i.e., has finished scraping.)
        """
        self.data_submitted = True
        return self.oar


def new_chapter(db_id, number, name):
    return items.Chapter(
        kind="Chapter",
        db_id=db_id,
        number=number,
        name=name,
        url=f"https://secure.sos.state.or.us/oard/displayChapterRules.action?selectedChapter={db_id}",
        divisions=[],
    )


def new_division(db_id, number, name):
    return items.Division(
        kind="Division",
        db_id=db_id,
        number=number,
        name=name,
        url=f"https://secure.sos.state.or.us/oard/displayDivisionRules.action?selectedDivision={db_id}",
    )
