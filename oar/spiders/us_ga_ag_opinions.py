import scrapy


# Nothing at all
class UsAgGaOpinions(scrapy.Spider):
    """Scrape the Georgia Attorney General Opinions

    Scrape both the official and unofficial opinions,
    producing one JSON record per opinion.
    """

    name = "us_ag_ga_opinions"
    start_urls = [
        "https://law.georgia.gov/opinions/official",
        "https://law.georgia.gov/opinions/unofficial",
    ]

    def parse(self, response):
        opinion_paths = response.xpath(
            "//td[contains(@class, 'views-field-title')]/a/@href"
        ).getall()

        for url in [response.urljoin(p) for p in opinion_paths]:
            yield scrapy.Request(url, callback=self.parse_opinion)

    def parse_opinion(self, response):
        yield {"Opinion URL": response.url}
