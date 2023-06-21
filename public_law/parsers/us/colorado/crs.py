from scrapy.selector.unified import Selector
from titlecase import titlecase

from public_law.items.crs import Article, Division, Title


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
    raw_division_names: list[str] = dom.xpath("//t-div/text()").getall() # type: ignore

    return [
        Division(
            name=titlecase(name),
            source_url=source_url,
            articles=_parse_articles(name, dom, source_url),
        )
        for name in raw_division_names
    ]


def _parse_articles(
    division_name: str, dom: Selector, source_url: str
) -> list[Article]:
    """Return the articles within the given Division."""

    # Algorithm:
    #
    # 1. Get all the child elements of TITLE-ANAL.
    # 2. Find the T-DIV with the Division name.
    # 3. `takewhile` all the following TA-LIST elements
    #    and stop if another T-DIV is reached.

    return []
