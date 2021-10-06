from scrapy.selector.unified import Selector
from titlecase import titlecase

from public_law.items import CrsTitle


def parse_title(dom: Selector) -> CrsTitle:
    raw_name = dom.xpath("//title_text/text()").get()
    raw_divisions = dom.xpath("//t_div/text()").getall()
    raw_number = dom.xpath("//b/text()").get().split(" ")[1]

    return CrsTitle(
        name=titlecase(raw_name),
        number=raw_number,
        divisions=[titlecase(d) for d in raw_divisions],
    )
