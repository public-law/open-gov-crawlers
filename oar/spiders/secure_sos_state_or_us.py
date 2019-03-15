# -*- coding: utf-8 -*-
import scrapy
from oar import items


class SecureSosStateOrUsSpider(scrapy.Spider):
    name = "secure.sos.state.or.us"
    allowed_domains = ["secure.sos.state.or.us"]
    start_urls = ["https://secure.sos.state.or.us/oard/ruleSearch.action"]

    def parse(self, response):
        for option in response.css("#browseForm option"):
            db_id = option.xpath("@value").get()
            if db_id == "-1":  # Ignore the heading
                continue
            number, name = map(str.strip, option.xpath("text()").get().split("-", 1))
            yield items.Chapter(db_id=db_id, name=name, number=number)
