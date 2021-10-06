from scrapy.selector.unified import Selector
from titlecase import titlecase

from public_law.items.crs import Division, Title


def parse_title(dom: Selector) -> Title:
    raw_name = dom.xpath("//title_text/text()").get()
    raw_number = dom.xpath("//b/text()").get().split(" ")[1]

    url_number = raw_number.rjust(2, "0")
    source_url = f"https://leg.colorado.gov/sites/default/files/images/olls/crs2021-title-{url_number}.pdf"

    return Title(
        name=titlecase(raw_name),
        number=raw_number,
        divisions=_parse_divisions(dom),
        source_url=source_url,
    )


def _parse_divisions(dom: Selector) -> list[Division]:
    raw_division_names = dom.xpath("//t_div/text()").getall()
    return [Division(name=titlecase(n)) for n in raw_division_names]
