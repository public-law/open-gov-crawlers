import re

from scrapy import Selector
from typing import Any, Dict, List

from oar.items import Rule
from oar.text import delete_all

SEPARATOR = re.compile(r"(?<=\d),|&amp;")


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


def parse_division(html: Selector) -> List[Any]:
    return [parse_rule(rule_div) for rule_div in html.xpath('//div[@class="rule_div"]')]


def parse_rule(rule_div: Selector) -> Rule:
    return Rule(
        kind="Rule",
        # number=number,
        # name=name,
        # url=oar_url(f"view.action?ruleNumber={number}"),
        # internal_url=f"https://secure.sos.state.or.us{internal_path}"
    )
