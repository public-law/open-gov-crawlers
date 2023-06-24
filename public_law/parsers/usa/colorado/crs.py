# pyright: reportUnknownMemberType=false
# pyright: reportOptionalMemberAccess=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownLambdaType=false
# pyright: reportGeneralTypeIssues=false


from scrapy.selector.unified import Selector
from scrapy.http.response import Response

from titlecase import titlecase
from itertools import takewhile, dropwhile
from typing import Any

from public_law.selector_util import node_name, just_text
from public_law.text import remove_trailing_period, normalize_whitespace
from public_law.items.crs import Article, Division, Title, Section

from bs4 import BeautifulSoup




def parse_sections(dom: Response, logger: Any = None) -> list[Section]:
    section_nodes = dom.xpath("//SECTION-TEXT")

    sections = []
    for node in section_nodes:
        if _is_repealed(node):
            continue

        number = _parse_section_number(node)
        if number is None:
            if logger is not None:
                logger.warn(f"Could not parse section number for {normalize_whitespace(node.get())} in {dom.url}")
            continue

        name = _parse_section_name(node)
        if name is None:
            if logger is not None:
                logger.warn(f"Could not parse section name for {normalize_whitespace(node.get())} in {dom.url}")
            continue

        text   = _parse_section_text(node)

        sections.append(Section(
            name           = name,
            number         = number,
            text           = text,
            article_number = number.split('-')[1],
            title_number   = number.split('-')[0]
        ))

    return sections


def _is_repealed(section_text: Selector) -> bool:
    match section_text.xpath('CATCH-LINE').get():
        case str(st):
            return "(Repealed)" in st
        case None:
            return False


def _parse_section_number(section_node: Selector) -> str | None:
    return just_text(section_node.xpath('CATCH-LINE/RHFTO'))


def _parse_section_name(section_node: Selector) -> str | None:
    soup = BeautifulSoup(section_node.xpath('CATCH-LINE').get(), 'xml')
    raw_name = normalize_whitespace(soup.get_text())
    name = remove_trailing_period(raw_name).split('.')[-1]

    return normalize_whitespace(name)


def _parse_section_text(section_node: Selector) -> str:
    raw_text     = section_node.get()
    text_strings = list(BeautifulSoup(raw_text, 'xml').stripped_strings)[3:]
    paragraphs   = ["<p>" + normalize_whitespace(s) + "</p>" for s in text_strings]
    
    return "\n".join(paragraphs)


def parse_title_bang(dom: Response, logger: Any = None) -> Title:
    result = parse_title(dom, logger)
    if result is None:
        raise Exception("Could not parse title")
    else:
        return result


def parse_title(dom: Response, logger: Any = None) -> Title | None:
    raw_name = dom.xpath("//TITLE-TEXT/text()").get()
    
    if raw_name is None:
        if logger is not None:
            logger.warn(f"Could not parse title name in {dom.url}")
            return None

    number     = dom.xpath("//TITLE-NUM/text()").get().split(" ")[1]
    url_number = number.rjust(2, "0")
    source_url = f"https://leg.colorado.gov/sites/default/files/images/olls/crs2022-title-{url_number}.pdf"

    return Title(
        name       = titlecase(raw_name),
        number     = number,
        children   = _parse_divisions(number, dom, source_url),
        source_url = source_url,
    )


def _parse_divisions(title_number: str, dom: Selector, source_url: str) -> list[Division]:
    raw_division_names = dom.xpath("//T-DIV/text()")

    return [
        Division(
            name         = titlecase(div_node.get()),
            articles     = _parse_articles(title_number, dom, div_node, titlecase(div_node.get()), source_url),
            title_number = title_number
        )
        for div_node in raw_division_names
    ]


def _parse_articles(title_number: str, dom: Selector, div_node: Selector, name: str, source_url: str) -> list[Article]:
    """Return the articles within the given Division."""

    #
    # Algorithm:
    #
    # 1. Get all the child elements of TITLE-ANAL.
    divs_and_articles = dom.xpath("//TITLE-ANAL/T-DIV | //TITLE-ANAL/TA-LIST")

    # 2. Find the T-DIV with the Division name.
    partial_list = list(dropwhile(
        lambda n: titlecase(just_text(n)) != name, 
        divs_and_articles
        ))

    if len(partial_list) == 0:
        return []

    # 3. `takewhile` all the following TA-LIST elements
    #    and stop at the end of the Articles.
    _head = partial_list[0]
    tail  = partial_list[1:]
    article_nodes = takewhile(is_article_node, tail)

    # 4. Convert the TA-LIST elements into Article objects.    
    articles = [
        Article(
            name = parse_article_name(n), 
            number = parse_article_number(n),
            title_number = title_number
            ) 
        for n in article_nodes
        ]

    return articles


def is_article_node(node: Selector):
    return node_name(node) == "TA-LIST"


def parse_article_name(node: Selector):
    """Return just the name of the Article.
    The raw text looks like this:
        "General, Provisions, 16-1-101 to 16-1-110"
    
    We want to return just the first part:
        "General, Provisions"
    """
    raw_text     = node.xpath("I/text()").get()
    cleaned_text = ", ".join(raw_text.split(",")[:-1])

    return cleaned_text


def parse_article_number(node: Selector):
    """Return just the number of the Article.
    The raw text looks like this:
        "1.1."
    
    We want to return just this:
        "1.1"
    """
    raw_text     = node.xpath("DT/text()").get()
    cleaned_text = remove_trailing_period(raw_text)

    return cleaned_text
