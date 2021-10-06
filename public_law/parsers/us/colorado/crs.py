from scrapy.selector.unified import Selector
from titlecase import titlecase


def parse_title(dom: Selector) -> dict:
    raw_name = dom.xpath("//title_text/text()").get()
    raw_divisions = dom.xpath("//t_div/text()").getall()

    return {
        "name": titlecase(raw_name),
        "divisions": [titlecase(d) for d in raw_divisions],
    }
