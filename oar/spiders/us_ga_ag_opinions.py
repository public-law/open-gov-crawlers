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
        yield {"Index URL": response.url}

        opinion_paths = response.xpath(
            "//td[contains(@class, 'views-field-title')]/a/@href"
        ).getall()

        for url in [response.urljoin(p) for p in opinion_paths]:
            yield scrapy.Request(url, callback=self.parse_opinion_page)

        next_page_path = response.xpath(
            "//a[contains(@title, 'Go to next page')]/@href"
        ).get()

        yield scrapy.Request(response.urljoin(next_page_path), callback=self.parse)

    def parse_opinion_page(self, response):
        yield {"Opinion URL": response.url}
