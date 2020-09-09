import scrapy


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

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_index_page)

    def parse_index_page(self, response):
        yield {"Index URL": response.url}

        opinion_paths = response.xpath(
            "//td[contains(@class, 'views-field-title')]/a/@href"
        ).getall()

        for url in [response.urljoin(p) for p in opinion_paths]:
            yield scrapy.Request(url, callback=self.parse_opinion_page)

        next_page_path = response.xpath(
            "//a[contains(@title, 'Go to next page')]/@href"
        ).get()

        yield scrapy.Request(
            response.urljoin(next_page_path), callback=self.parse_index_page
        )

    def parse_opinion_page(self, response):
        yield {"Opinion URL": response.url}
