from typing import Any

from bs4 import BeautifulSoup
from scrapy.http.response.xml import XmlResponse
from scrapy.selector.unified import Selector

from public_law.shared.utils.html import just_text
from public_law.legal_texts.models.crs import Section
from public_law.shared.utils.text import (NonemptyString, normalize_whitespace,
                             remove_trailing_period)


def parse_sections(dom: XmlResponse, logger: Any) -> list[Section]:
    # Filter out empty section nodes first
    section_nodes = [
        node for node in dom.selector.xpath("//SECTION-TEXT")
        if node.get().strip() != "<SECTION-TEXT/>"
    ]

    sections: list[Section] = []
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
