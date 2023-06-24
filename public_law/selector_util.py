from scrapy.selector.unified import Selector


def node_name(node: Selector):
    return node.xpath("name()").get()

def just_text(node: Selector) -> str | None:
    return node.xpath("text()").get()
