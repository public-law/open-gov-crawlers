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
        self.data_submitted = False
        # The merged data to return for conversion to a JSON tree
        self.oar = items.OAR(chapters=[])


    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        """Register to receive the idle event"""
        spider = super(SecureSosStateOrUsSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
        return spider


    def spider_idle(self, spider):
        """Schedule a simple request in order to return the collected data"""
        if self.data_submitted: return

        self.crawler.engine.schedule(scrapy.Request('http://neverssl.com/', callback=self.submit_data), spider)
        raise scrapy.exceptions.DontCloseSpider


    def submit_data(self, _):
        """Simply return the collection of all the scraped data.
        To be used as a callback.
        """
        self.data_submitted = True
        return self.oar


    def parse(self, response):
        """The primary Scrapy callback to begin scraping.
        Kick off scraping by parsing the main OAR page.
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
            chapter = items.Chapter(
                kind="Chapter",
                db_id=db_id,
                number=number,
                name=name,
                url=f"https://secure.sos.state.or.us/oard/displayChapterRules.action?selectedChapter={db_id}",
                divisions=[],
            )

            self.oar['chapters'].append(chapter)

            request = scrapy.Request(chapter["url"], callback=self.parse_chapter_page)
            request.meta["chapter"] = chapter
            yield request


    def parse_chapter_page(self, response):
        """A Chapter's page contains a hierarchical list of all its Divisions
        along with their contained Rules.
        """
        chapter = response.meta["chapter"]

        for anchor in response.css("#accordion > h3 > a"):
            db_id = anchor.xpath("@href").get().split("=")[1]
            number, name = map(str.strip, anchor.xpath("text()").get().split("-", 1))
            number = number.split(" ")[1]
            division = items.Division(
                kind="Division",
                db_id=db_id,
                number=number,
                name=name,
                url=f"https://secure.sos.state.or.us/oard/displayDivisionRules.action?selectedDivision={db_id}",
            )

            chapter["divisions"].append(division)

