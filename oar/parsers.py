import re

from scrapy import Selector
from typing import Any, Dict, List

from oar.items import Rule
from oar.text import delete_all

SEPARATOR = re.compile(r"(?<=\d),|&amp;")
DOMAIN = "secure.sos.state.or.us"


class ParseException(Exception):
    pass


def meta_sections(text: str) -> Dict[str, Any]:
    authority, implements, history = text.split("<br>", maxsplit=2)

    return {
        "authority": statute_meta(authority.split("</b>")[1].strip()),
        "implements": statute_meta(implements.split("</b>")[1].strip()),
        "history": delete_all(history, ["<b>History:</b><br>", "<br></p>"]),
    }


def statute_meta(text: str) -> List[str]:
    """Parse a statute meta line of text.

    For example:
      input:  'ORS 181A.235 & ORS 192'
      output: ['ORS 181A.235', 'ORS 192']
    """
    return [s.strip() for s in SEPARATOR.split(text)]


def parse_division(html: Selector) -> List[Rule]:
    return [parse_rule(rule_div) for rule_div in html.xpath('//div[@class="rule_div"]')]


def parse_rule(rule_div: Selector) -> Rule:
    number = rule_div.css("strong > a::text").get()
    number = number.strip()

    name = rule_div.css('strong::text').get()
    name = name.strip()

    return parse_rule_content(rule_div, number, name)


def parse_rule_content(rule_div: Selector, number: str, name: str) -> Rule:
    raw_paragraphs: List[str] = rule_div.xpath("p")[1:-1].getall()
    cleaned_up_paragraphs = [
        p.strip().replace("\n", "") for p in raw_paragraphs
    ]
    cleaned_up_paragraphs = [
        re.sub(r' +', ' ', p) for p in cleaned_up_paragraphs
    ]
    non_empty_paragraphs = list(filter(None, cleaned_up_paragraphs))
    content_paragaphs = non_empty_paragraphs[1:]

    # meta_paragraph = non_empty_paragraphs[-1]
    # metadata = meta_sections(meta_paragraph)

    return Rule(
        kind="Rule",
        number=number,
        name=name,
        url=oar_url(f"view.action?ruleNumber={number}"),
        text="\n".join(content_paragaphs),
        # authority=metadata["authority"],
        # implements=metadata["implements"],
        # history=metadata["history"]
    )


URL_PREFIX = f"https://{DOMAIN}/oard/"


def oar_url(relative_fragment: str) -> str:
    return URL_PREFIX + relative_fragment
