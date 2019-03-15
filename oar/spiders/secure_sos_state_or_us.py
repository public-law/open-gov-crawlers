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
            # Or... do the final yield in a spider_idle signal handler:
            # https://docs.scrapy.org/en/latest/topics/signals.html

        yield chapter
