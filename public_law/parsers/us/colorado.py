from scrapy.selector.unified import Selector
from titlecase import titlecase


def parse_title(dom: Selector) -> dict:
    raw_name = dom.xpath("//title_text/text()").get()

    return {"name": titlecase(raw_name)}
