from scrapy.selector.unified import Selector
from titlecase import titlecase

from public_law.items.crs import Division, Title


def parse_title(dom: Selector) -> Title:
    raw_name = dom.xpath("//title_text/text()").get()
    raw_division_names = dom.xpath("//t_div/text()").getall()
    raw_number = dom.xpath("//b/text()").get().split(" ")[1]

    return Title(
        name=titlecase(raw_name),
        number=raw_number,
        divisions=[Division(name=titlecase(n)) for n in raw_division_names],
    )
