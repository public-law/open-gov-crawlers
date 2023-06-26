# pyright: reportUnknownMemberType=false
# pyright: reportOptionalMemberAccess=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownLambdaType=false


from scrapy.selector.unified import Selector
from scrapy.http.response import Response

from titlecase import titlecase
from itertools import takewhile, dropwhile
from typing import Any

from public_law.selector_util import node_name, just_text
from public_law.text import remove_trailing_period, normalize_whitespace, NonemptyString, URL
from public_law.items.crs import Article, Division, Title, Section

from bs4 import BeautifulSoup




def parse_sections(dom: Response, logger: Any) -> list[Section]:
    section_nodes = dom.xpath("//SECTION-TEXT")

    sections = []
    for node in section_nodes:
        if _is_repealed(node):
            continue

        number = _parse_section_number(node)
        if number is None:
            logger.warn(f"Could not parse section number for {normalize_whitespace(node.get())} in {dom.url}")
            continue

        name = _parse_section_name(node)
        if name is None:
            logger.warn(f"Could not parse section name for {normalize_whitespace(node.get())} in {dom.url}")
            continue

        text = _parse_section_text(node)
        if text == '':
            logger.warn(f"Could not parse section text for {normalize_whitespace(node.get())} in {dom.url}")
            continue


        sections.append(Section(
            name           = NonemptyString(name),
            number         = NonemptyString(number),
            text           = NonemptyString(text),
            article_number = NonemptyString(number.split('-')[1]),
            title_number   = NonemptyString(number.split('-')[0])
        ))

    return sections


def _is_repealed(section_text: Selector) -> bool:
    match section_text.xpath('CATCH-LINE').get():
        case str(text):
            return ("(Repealed" in text) or ("(Deleted" in text)
        case None:
            return False


def _parse_section_number(section_node: Selector) -> str | None:
    return just_text(section_node.xpath('CATCH-LINE/RHFTO'))


def _parse_section_name(section_node: Selector) -> str | None:
    match section_node.xpath('CATCH-LINE').get():
        case None:
            return None
        case str(s):
            soup     = BeautifulSoup(s, 'xml')
            raw_name = normalize_whitespace(soup.get_text())
            name     = remove_trailing_period(raw_name).split('.')[-1]

            return normalize_whitespace(name)


def _parse_section_text(section_node: Selector) -> str:
    raw_text     = section_node.get()
    text_strings = list(BeautifulSoup(raw_text, 'xml').stripped_strings)[3:]
    paragraphs   = ["<p>" + normalize_whitespace(s) + "</p>" for s in text_strings]
    
    return "\n".join(paragraphs)


def parse_title_bang(dom: Response, logger: Any) -> Title:
    match parse_title(dom, logger):
        case None:
            raise Exception("Could not parse title")
        case result:
            return result


def parse_title(dom: Response, logger: Any) -> Title | None:
    raw_name = dom.xpath("//TITLE-TEXT/text()").get()
    
    if raw_name is None:
        logger.warn(f"Could not parse title name in {dom.url}")
        return None

    number     = NonemptyString(dom.xpath("//TITLE-NUM/text()").get().split(" ")[1])
    url_number = number.rjust(2, "0")
    source_url = URL(f"https://leg.colorado.gov/sites/default/files/images/olls/crs2022-title-{url_number}.pdf")

    return Title(
        name       = NonemptyString(titlecase(raw_name)),
        number     = number,
        children   = _parse_divisions(number, dom, source_url),
        source_url = URL(source_url)
    )


def _parse_divisions(title_number: NonemptyString, dom: Selector | Response, source_url: URL) -> list[Division]:
    division_nodes = dom.xpath("//T-DIV")

    divs = []
    for div_node in division_nodes:
        name = _div_name_text(div_node)

        divs.append(
            Division(
                name         = NonemptyString(name),
                articles     = _parse_articles(title_number, dom, name, source_url),
                title_number = NonemptyString(title_number))
        )
    return divs


def _div_name_text(div_node: Selector) -> NonemptyString:
    soup = BeautifulSoup(div_node.get(), 'xml')

    return NonemptyString(titlecase(normalize_whitespace(soup.get_text())))


def _parse_articles(title_number: NonemptyString, dom: Selector | Response, div_name: NonemptyString, source_url: URL) -> list[Article]:
    """Return the articles within the given Division."""

    #
    # Algorithm:
    #
    # 1. Get all the child elements of TITLE-ANAL.
    divs_and_articles = dom.xpath("//TITLE-ANAL/T-DIV | //TITLE-ANAL/TA-LIST")

    # 2. Find the T-DIV with the Division name.
    partial_list = list(dropwhile(
        lambda n: _div_name_text(n) != div_name, 
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
    return [
        Article(
            name = parse_article_name(n), 
            number = parse_article_number(n),
            title_number = title_number
            ) 
        for n in article_nodes
        ]


def is_article_node(node: Selector) -> bool:
    return node_name(node) == "TA-LIST"


def parse_article_name(node: Selector) -> NonemptyString:
    """Return just the name of the Article.
    The raw text looks like this:
        "General, Provisions, 16-1-101 to 16-1-110"
    
    We want to return just the first part:
        "General, Provisions"
    """
    match node.xpath("I/text()").get():
        case str(text):
            raw_text     = normalize_whitespace(text)
            cleaned_text = ", ".join(raw_text.split(",")[:-1])
            if cleaned_text == "":
                cleaned_text = raw_text
            return NonemptyString(cleaned_text)
        case None:
            raise Exception("Could not parse article name in {node}")


def parse_article_number(node: Selector) -> NonemptyString:
    """Return just the number of the Article.
    The raw text looks like this:
        "1.1."
    
    We want to return just this:
        "1.1"
    """
    match node.xpath("DT/text()").get():
        case str(raw_text):
            return NonemptyString(remove_trailing_period(raw_text))
        case None:
            raise Exception("Could not parse article number in {node}")
