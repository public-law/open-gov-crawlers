from typing import Any

from scrapy.selector.unified import Selector, SelectorList


def node_name(node: Selector) -> str | None:
    return node.xpath("name()").get()

def just_text(node: Selector | SelectorList | Any) -> str | None:
    return node.xpath("text()").get()
