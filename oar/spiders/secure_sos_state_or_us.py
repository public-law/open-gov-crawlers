# -*- coding: utf-8 -*-

from datetime import datetime
import logging
import pytz
import scrapy
from scrapy import signals
from titlecase import titlecase

from oar import items
from oar import parsers

DOMAIN = "secure.sos.state.or.us"
URL_PREFIX = f"https://{DOMAIN}/oard/"


def oar_url(relative_fragment: str) -> str:
    return URL_PREFIX + relative_fragment


class SecureSosStateOrUsSpider(scrapy.Spider):
    name = DOMAIN
    allowed_domains = [DOMAIN]
    start_urls = [oar_url("ruleSearch.action")]

    def __init__(self):
        super().__init__()

        # A flag, set after post-processing is finished, to avoid an infinite
        # loop.
        self.data_submitted = False

        # The object to return for conversion to a JSON tree. All the parse
        # methods add their results to this structure.
        self.oar = items.OAR(date_accessed=todays_date(), chapters=[])

    def parse(self, response):
        """The primary Scrapy callback to begin scraping.

        Kick off scraping by parsing the main OAR page.
        """
        return self.parse_search_page(response)

    def parse_search_page(self, response):
        """Parse the top-level page.

        The search page contains a list of Chapters, with the names,
        numbers, and internal id's.
        """
        for option in response.css("#browseForm option"):
            db_id = option.xpath("@value").get()
            if db_id == "-1":  # Ignore the heading
                continue

            number, name = map(str.strip, option.xpath(
                "text()").get().split("-", 1))
            chapter = new_chapter(db_id, number, name)
            self.oar["chapters"].append(chapter)

            request = scrapy.Request(
                chapter["url"], callback=self.parse_chapter_page)
            request.meta["chapter"] = chapter
            yield request

    def parse_chapter_page(self, response):
        """Parse a mid-level page.

        A Chapter's page contains a hierarchical list of all its Divisions
        along with their contained Rules.
        """
        chapter = response.meta["chapter"]
        division_index = {}

        # Collect the Divisions
        for anchor in response.css("#accordion > h3 > a"):
            db_id = anchor.xpath("@href").get().split("=")[1]
            raw_number, raw_name = map(
                str.strip, anchor.xpath("text()").get().split("-", 1)
            )
            number = raw_number.split(" ")[1]
            name = titlecase(raw_name)
            division = new_division(db_id, number, name)

            chapter["divisions"].append(division)
            division_index[division.number_in_rule_format()] = division

        # Collect empty Rules
        for anchor in response.css(".rule_div > p"):
            # TODO: Use the Rule's db_id to generate its URL for scraping.
            #       Possibly add a second url attribute to Rule, e.g.,
            #       scraping_url. Meanwhile, the current one is canonical_url.
            try:
                number = anchor.css("strong > a::text").get().strip()
                name = anchor.xpath("text()").get().strip()
                rule = new_rule(number, name)

                # Retrieve the Rule details
                request = scrapy.Request(
                    rule["url"], callback=self.parse_rule_page)
                request.meta["rule"] = rule
                yield request

                # Find its Division and add it
                parent_division = division_index[rule.division_number()]
                parent_division["rules"].append(rule)
            except:
                logging.info(f"Error parsing anchor: {anchor.get()}")

    def parse_rule_page(self, response):
        """Parse a leaf node (bottom level) page.

        The Rule page contains the actual Rule's full text.
        The Rule object has already been created with the remaining info,
        so here we just retrieve the text and save it.
        """
        raw_paragraphs = response.xpath("//p")[1:-1].getall()
        cleaned_up_paragraphs = [
            p.strip().replace("  ", "").replace("\n", "") for p in raw_paragraphs
        ]
        non_empty_paragraphs = list(filter(None, cleaned_up_paragraphs))
        content_paragaphs = non_empty_paragraphs[0:-1]

        meta_paragraph = non_empty_paragraphs[-1]
        metadata = parsers.meta_sections(meta_paragraph)

        rule = response.meta["rule"]
        rule["text"] = "\n".join(content_paragaphs)
        rule["authority"] = metadata["authority"]
        rule["implements"] = metadata["implements"]
        rule["history"] = metadata["history"]

    #
    # Output a single object: a JSON tree containing all the scraped data. This
    # code implements that strategy by registering a signal (event) listener to
    # execute after all scraping has finished, and the data is collected.
    #

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        """Register to receive the idle event"""
        spider: SecureSosStateOrUsSpider = super(SecureSosStateOrUsSpider, cls).from_crawler(
            crawler, *args, **kwargs
        )
        crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
        return spider

    def spider_idle(self, spider):
        """Schedule a simple request in order to return the collected data"""
        if self.data_submitted:
            return

        # This is a hack: I don't yet know how to schedule a request to just
        # submit data _without_ also triggering a scrape. So I provide a URL
        # to a simple site that we're going to ignore.
        null_request = scrapy.Request(
            "http://neverssl.com/", callback=self.submit_data)
        self.crawler.engine.schedule(null_request, spider)
        raise scrapy.exceptions.DontCloseSpider

    def submit_data(self, _):
        """Simply return the collection of all the scraped data.

        Ignore the actual scraped content. I haven't figured out another
        way to submit the merged results. To be used as a callback when
        the spider is idle (i.e., has finished scraping.)
        """
        self.data_submitted = True
        return self.oar


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


def new_rule(number: str, name: str):
    return items.Rule(
        kind="Rule",
        number=number,
        name=name,
        url=oar_url(f"view.action?ruleNumber={number}"),
    )


def todays_date() -> str:
    pacific = pytz.timezone("US/Pacific")
    fmt = "%Y-%m-%d"
    return pacific.localize(datetime.now()).strftime(fmt)
