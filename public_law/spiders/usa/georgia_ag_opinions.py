# pyright: reportUninitializedInstanceVariable=false
# pyright: reportPrivateUsage=false
# pyright: reportUnknownVariableType=false

# pyright: reportUnknownArgumentType=false
# pyright: reportGeneralTypeIssues=false


from typing import Any, Dict

from scrapy import Spider
from scrapy.http.request import Request
from scrapy.http.response import Response
from scrapy.http.response.html import HtmlResponse

from ...parsers.usa.georgia_ag_opinions import parse_ag_opinion

JD_VERBOSE_NAME = "USA / Georgia"
PUBLICATION_NAME = "Attorney General Opinions"


class GeorgiaAgOpinions(Spider):
    """Scrape the Georgia Attorney General Opinions

    Retrieve both the official and unofficial opinions,
    producing one JSON object per opinion (page).
    """

    name = "usa_ga_attorney_general_opinions"
    start_urls = [
        "https://law.georgia.gov/opinions/official",
        "https://law.georgia.gov/opinions/unofficial",
    ]


    def parse(self, response: Response, **kwargs: Dict[str, Any]):
        """Framework callback which begins the parsing."""

        match(response):
            case HtmlResponse():
                return self.parse_index_page(response)

            case _:
                raise Exception(f"Unexpected response type: {type(response)}")


    def parse_index_page(self, response: HtmlResponse):
        #
        # 1. Find all the individual opinions on this index page
        # and request a parse for each.
        #
        opinion_paths = response.xpath(
                "//td[contains(@class, 'views-field-title')]/a/@href"
            ).getall()

        for url in [response.urljoin(p) for p in opinion_paths]:
            yield Request(url, callback=self.parse_opinion_page) # type: ignore

        #
        # 2. Go to the next index page, if there is one.
        #
        next_page_path = response.xpath(
            "//a[contains(@title, 'Go to next page')]/@href"
        ).get()

        if next_page_path is not None:
            yield Request(
                response.urljoin(next_page_path), callback=self.parse_index_page # type: ignore
            )


    def parse_opinion_page(self, response: HtmlResponse):
        yield parse_ag_opinion(response)._asdict()
