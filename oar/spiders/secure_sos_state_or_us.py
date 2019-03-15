# -*- coding: utf-8 -*-
import scrapy


class SecureSosStateOrUsSpider(scrapy.Spider):
    name = "secure.sos.state.or.us"
    allowed_domains = ["secure.sos.state.or.us"]
    start_urls = ["https://secure.sos.state.or.us/oard/ruleSearch.action"]

    def parse(self, response):
        self.logger.info(f"A response from {response.url} just arrived!")
