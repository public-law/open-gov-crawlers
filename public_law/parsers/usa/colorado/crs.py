# pyright: reportUnknownMemberType=false
# pyright: reportOptionalMemberAccess=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownLambdaType=false


from scrapy.selector.unified import Selector
from titlecase import titlecase
import itertools
from typing import cast

from public_law.items.crs import Article, Division, Title


def parse_title(dom: Selector) -> Title:
    print(f"{dom=}")
    raw_name   = cast(str, dom.xpath("//title-text/text()").get())
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
    raw_division_names = dom.xpath("//t-div/text()")

    return [
        Division(
            name=titlecase(div_node.get()),
            source_url=source_url,
            articles=_parse_articles(dom, div_node, source_url),
        )
        for div_node in raw_division_names
    ]


def _parse_articles(dom: Selector, div_node: Selector, source_url: str) -> list[Article]:
    """Return the articles within the given Division."""

    # Algorithm:
    #
    # 1. Get all the child elements of TITLE-ANAL.
    # 2. Find the T-DIV with the Division name.
    # 3. `takewhile` all the following TA-LIST elements
    #    and stop if another T-DIV is reached.

    divs_and_articles = dom.xpath("//t-div | //ta-list")

    _head = divs_and_articles[0]
    tail = divs_and_articles[1:]

    article_nodes = itertools.takewhile(
        lambda node: node.xpath("name()").get() == "ta-list", 
        tail
        )
    
    articles = [Article(name=n.get(), number="999", source_url=source_url) for n in article_nodes]

    return articles
