# -*- coding: utf-8 -*-

from datetime import datetime, date
import logging
from oar.items import Chapter
import pytz
import scrapy
import scrapy.exceptions
import scrapy.http
import scrapy.signals
from scrapy import Selector
from titlecase import titlecase
from typing import List
from typing_extensions import Protocol


from oar import items
from oar import parsers

DOMAIN = "secure.sos.state.or.us"
URL_PREFIX = f"https://{DOMAIN}/oard/"


def oar_url(relative_fragment: str) -> str:
    return URL_PREFIX + relative_fragment


class ParseException(Exception):
    pass


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

    def parse_chapter_page(self, response: scrapy.http.Response):
        """Parse a mid-level page.

        A Chapter's page contains a hierarchical list of all its Divisions
        along with their contained Rules.
        """
        chapter: Chapter = response.meta["chapter"]
        division_index = {}

        # Collect the Divisions
        anchor: Selector
        for anchor in response.css("#accordion > h3 > a"):
            db_id: str = anchor.xpath("@href").get().split("=")[1]
            raw_number, raw_name = map(
                str.strip, anchor.xpath("text()").get().split("-", 1)
            )
            number = raw_number.split(" ")[1]
            name: str = titlecase(raw_name)
            division = new_division(db_id, number, name)

            chapter["divisions"].append(division)
            division_index[division.number_in_rule_format()] = division

        # Collect empty Rules
        for anchor_paragraph in response.css(".rule_div > p"):
            # TODO: Use the Rule's db_id to generate its URL for scraping.
            #       Possibly add a second url attribute to Rule, e.g.,
            #       scraping_url. Meanwhile, the current one is canonical_url.
            try:
                number = anchor_paragraph.css("strong > a::text").get()
                if number is None:
                    raise ParseException("Couldn't parse number")
                number = number.strip()

                name = anchor_paragraph.xpath("text()").get()
                if name is None:
                    raise ParseException("Couldn't parse name")
                name = name.strip()

                internal_path = anchor_paragraph.xpath(
                    '//a').xpath('@href').get()
                rule = new_rule(number, name, internal_path)

                # Retrieve the Rule details
                request = scrapy.Request(
                    rule['internal_url'], callback=self.parse_rule_page)
                request.meta["rule"] = rule
                yield request

                # Find its Division and add it
                parent_division = division_index[rule.division_number()]
                parent_division["rules"].append(rule)
            except ParseException as e:
                logging.info(
                    f"Error parsing anchor paragraph: {anchor_paragraph.get()}, {e}")

    def parse_rule_page(self, response: scrapy.http.Response):
        """Parse a leaf node (bottom level) page.

        The Rule page contains the actual Rule's full text.
        The Rule object has already been created with the remaining info,
        so here we just retrieve the text and save it.
        """
        raw_paragraphs: List[str] = response.xpath("//p")[1:-1].getall()
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
        """Override to register to receive the idle event"""
        spider: SecureSosStateOrUsSpider = super(SecureSosStateOrUsSpider, cls).from_crawler(
            crawler, *args, **kwargs
        )
        crawler.signals.connect(
            spider.spider_idle, signal=scrapy.signals.spider_idle)
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


def new_rule(number: str, name: str, internal_path: str):
    return items.Rule(
        kind="Rule",
        number=number,
        name=name,
        url=oar_url(f"view.action?ruleNumber={number}"),
        internal_url=oar_url(internal_path)
    )


class SimpleTimezone(Protocol):
    def localize(self, dt: datetime) -> date:
        ...


def todays_date() -> str:
    mountain: SimpleTimezone = pytz.timezone("US/Mountain")
    fmt = "%Y-%m-%d"
    return mountain.localize(datetime.now()).strftime(fmt)
