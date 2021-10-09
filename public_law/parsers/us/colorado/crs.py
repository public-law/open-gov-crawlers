from scrapy.selector.unified import Selector
from titlecase import titlecase

from public_law.items.crs import Division, Title


def parse_title(dom: Selector) -> Title:
    print(f"{dom=}")
    raw_name = dom.xpath("//title-text/text()").get()
    raw_number = dom.xpath("//title-num/text()").get().split(" ")[1]

    url_number = raw_number.rjust(2, "0")
    source_url = f"https://leg.colorado.gov/sites/default/files/images/olls/crs2021-title-{url_number}.pdf"

    return Title(
        name=titlecase(raw_name),
        number=raw_number,
        divisions=_parse_divisions(dom, source_url),
        source_url=source_url,
    )


def _parse_divisions(dom: Selector, source_url: str) -> list[Division]:
    raw_division_names = dom.xpath("//t-div/text()").getall()

    return [
        Division(name=titlecase(n), source_url=source_url, articles=[])
        for n in raw_division_names
    ]
