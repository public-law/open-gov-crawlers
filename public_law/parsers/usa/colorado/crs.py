# pyright: reportUnknownMemberType=false
# pyright: reportOptionalMemberAccess=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownLambdaType=false


from scrapy.selector.unified import Selector
from scrapy.http.response import Response

from typing import Any

from public_law.selector_util import just_text
from public_law.text import remove_trailing_period, normalize_whitespace, NonemptyString, URL, titleize
from public_law.items.crs import Article, Division, Title, Section
from public_law.parsers.usa.colorado.crs_articles import div_name_text, parse_articles, parse_articles_from_division

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
            part_number    = None,
            title_number   = NonemptyString(number.split('-')[0])
        ))

    return sections


def _has_subdivisions(dom: Selector | Response) -> bool:
    raw_div_names = [just_text(e) for e in dom.xpath("//TITLE-ANAL/T-DIV")]
    
    return not all([Division.is_valid_raw_name(n) for n in raw_div_names])



def _is_repealed(section_text: Selector) -> bool:
    match section_text.xpath('CATCH-LINE').get():
        case str(text):
            return ("(Repealed" in text) or ("(Deleted" in text) or ("(Reserved" in text)
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

    name       = NonemptyString(titleize(raw_name))
    number     = NonemptyString(dom.xpath("//TITLE-NUM/text()").get().split(" ")[1])
    url_number = number.rjust(2, "0")
    source_url = URL(f"https://leg.colorado.gov/sites/default/files/images/olls/crs2022-title-{url_number}.pdf")

    # print(f"\nTitle: {number}, {name}")

    return Title(
        name       = name,
        number     = number,
        source_url = URL(source_url),
        children   = _parse_divisions_or_articles(number, dom, logger)
    )


def _parse_divisions_or_articles(title_number: NonemptyString, dom: Selector | Response, logger: Any) -> list[Division] | list[Article]:
    division_nodes = dom.xpath("//T-DIV")
    article_nodes  = dom.xpath("//TA-LIST")

    if len(division_nodes) > 0:
        return _parse_divisions(title_number, dom, logger)
    elif len(article_nodes) > 0:
        return parse_articles(title_number, dom, logger)
    else:
        raise Exception(f"Could not parse divisions or articles in Title {title_number}")


def _parse_divisions(title_number: NonemptyString, dom: Selector | Response, logger: Any) -> list[Division]:
    division_nodes = dom.xpath("//T-DIV")

    divs = []
    for div_node in division_nodes:
        name = div_name_text(div_node)
        if name is None:
            logger.warn(f"Could not parse division name in {div_node.get()}, Title {title_number}")
            continue

        try:
            if _has_subdivisions(dom):
                pass
                # divs.append(
                #     Division(
                #         raw_name     = name,
                #         children     = _parse_subdivisions_from_division(title_number, dom, name),
                #         title_number = title_number
                #         )
                #     )
            else:
                divs.append(
                    Division(
                        raw_name     = name,
                        children     = parse_articles_from_division(title_number, dom, name),
                        title_number = title_number
                        )
                    )
        except ValueError:
            logger.warn(f"Could not parse division name in {name}, Title {title_number}")

    return divs
