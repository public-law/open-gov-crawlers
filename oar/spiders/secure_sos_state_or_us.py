# -*- coding: utf-8 -*-
import scrapy


class SecureSosStateOrUsSpider(scrapy.Spider):
    name = "secure.sos.state.or.us"
    allowed_domains = ["secure.sos.state.or.us"]
    start_urls = ["https://secure.sos.state.or.us/oard/ruleSearch.action"]

    def parse(self, response):
        for option in response.css("#browseForm option"):
            db_id = option.xpath("@value").get()
            if db_id == "-1":
                continue
            number, name = map(str.strip, option.xpath("text()").get().split("-", 1))
            yield {"db_id": db_id, "number": number, "name": name}
