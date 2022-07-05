# pyright: reportUninitializedInstanceVariable=false
# pyright: reportPrivateUsage=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportGeneralTypeIssues=false


from public_law.parsers.us.georgia import parse_ag_opinion
from scrapy import Spider
from scrapy.http.request import Request
from scrapy.http.response import Response
from typing import Any, Dict, cast


class GeorgiaAgOpinions(Spider):
    """Scrape the Georgia Attorney General Opinions

    Retrieve both the official and unofficial opinions,
    producing one JSON object per opinion (page).
    """

    name = "georgia_ag_opinions"
    start_urls = [
        "https://law.georgia.gov/opinions/official",
        "https://law.georgia.gov/opinions/unofficial",
    ]

    def parse(self, response: Response, **kwargs: Dict[str, Any]):
        """Framework callback which begins the parsing."""
        return self.parse_index_page(response)

    def parse_index_page(self, response: Response):
        #
        # 1. Find all the individual opinions on this index page
        # and request a parse for each.
        #
        opinion_paths = cast(
            list[str],
            response.xpath(
                "//td[contains(@class, 'views-field-title')]/a/@href"
            ).getall(),
        )

        for url in [cast(str, response.urljoin(p)) for p in opinion_paths]:
            yield Request(url, callback=self.parse_opinion_page)

        #
        # 2. Go to the next index page, if there is one.
        #
        next_page_path = response.xpath(
            "//a[contains(@title, 'Go to next page')]/@href"
        ).get()

        if next_page_path is not None:
            yield Request(
                response.urljoin(next_page_path), callback=self.parse_index_page
            )

    def parse_opinion_page(self, response: Response):
        yield parse_ag_opinion(response)._asdict()
