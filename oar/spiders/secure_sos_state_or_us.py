# -*- coding: utf-8 -*-
import json
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
        self.oar = {'chapters': []}


    # Register to receive the signal
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(SecureSosStateOrUsSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
        return spider

    def spider_idle(self, spider):
        if self.data_submitted: return

        # Schedule a null request
        self.crawler.engine.schedule(scrapy.Request('http://neverssl.com/', callback=self.submit_data), spider)
        raise scrapy.exceptions.DontCloseSpider

    def submit_data(self, _):
        self.data_submitted = True
        return self.oar


    def parse(self, response):
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
        chapter = response.meta["chapter"]

        for a in response.css("#accordion > h3 > a"):
            db_id = a.xpath("@href").get().split("=")[1]
            number, name = map(str.strip, a.xpath("text()").get().split("-", 1))
            number = number.split(" ")[1]
            division = items.Division(
                kind="Division",
                db_id=db_id,
                number=number,
                name=name,
                url=f"https://secure.sos.state.or.us/oard/displayDivisionRules.action?selectedDivision={db_id}",
            )

            chapter["divisions"].append(division)

            # 1. Find the rules w/in the new division.
            # 2. Add empty rules to the division.
            # 3. Create a Pipeline to output the to-be-scraped Rule URLs to a plaintext file.
            # 4. Create a RuleTextSpider to retrieve just the text of the rules.
            # 5. This RuleTextSpider can create a second JSON file with a simple JSON lines format.
            # 6. A script can use both JSON files as input and create a good single file.
            #
            # Or... do the final yield in a spider_idle or spider_closed signal handler:
            # https://docs.scrapy.org/en/latest/topics/signals.html
            #
            # Or... just scrape the Rule Contents and yield them as simple key/value pairs to
            # be included in the "JSON" output. And then post-process into proper JSON.
