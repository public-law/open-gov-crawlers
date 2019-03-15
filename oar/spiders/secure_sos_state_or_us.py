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
                kind="Chapter",
                db_id=db_id,
                number=number,
                name=name,
                url=f"https://secure.sos.state.or.us/oard/displayChapterRules.action?selectedChapter={db_id}",
                divisions=[],
            )

            request = scrapy.Request(chapter["url"], callback=self.parse_chapter_page)
            request.meta["chapter"] = chapter

            yield request

    def parse_chapter_page(self, response):
        chapter = response.meta["chapter"]

        for a in response.css("#accordion > h3 > a"):
            db_id = a.xpath("@href").get().split("=")[1]
            number, name = map(str.strip, a.xpath("text()").get().split("-", 1))
            number = number.split(" ")[1]

            chapter["divisions"].append(
                items.Division(
                    kind="Division",
                    db_id=db_id,
                    number=number,
                    name=name,
                    url=f"https://secure.sos.state.or.us/oard/displayDivisionRules.action?selectedDivision={db_id}",
                )
            )

        yield chapter
