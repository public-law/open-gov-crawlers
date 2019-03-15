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
            chapter = items.Chapter(
                db_id=db_id,
                number=number,
                name=name,
                url=f"https://secure.sos.state.or.us/oard/displayChapterRules.action?selectedChapter={db_id}",
            )
            yield chapter

            request = scrapy.Request(chapter["url"], callback=self.parse_chapter_page)
            request.meta["chapter"] = chapter
            yield request

    def parse_chapter_page(self, response) -> None:
        chapter = response.meta["chapter"]
        pass
