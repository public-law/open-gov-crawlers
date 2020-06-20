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
    # Somewhat tricky: The history section uses embedded <br>
    # tags, so we want to leave those in place. Therefore, we want
    # to use just the first two <br>'s to split the meta section
    # into three parts.
    authority_meta: List[str]
    implements_meta: List[str]
    history_meta: str

    if ("Statutory/Other Authority" not in text) and ("Statutes/Other Implemented" not in text):
        authority_meta = []
        implements_meta = []
        history_meta = _string_meta(text)

    elif "Statutory/Other Authority" not in text:
        authority_meta = []
        implements, history = text.split("<br>", maxsplit=1)
        implements_meta = _list_meta(implements)
        history_meta = _string_meta(history)

    elif "Statutes/Other Implemented" not in text:
        authority, history = text.split("<br>", maxsplit=1)
        authority_meta  = _list_meta(authority)
        implements_meta = []
        history_meta = _string_meta(history)

    else:
        authority, implements, history = text.split("<br>", maxsplit=2)
        authority_meta  = _list_meta(authority)
        implements_meta = _list_meta(implements)
        history_meta = _string_meta(history)

    return {
        "authority": authority_meta,
        "implements": implements_meta,
        "history": history_meta,
    }


def _list_meta(section: str) -> List[str]:
    return statute_meta(section.split("</b>")[1].strip())

def _string_meta(section: str) -> str:
    return delete_all(section, ["<p>", "<b>History:</b><br>", "<br> </p>"]).strip()


def statute_meta(text: str) -> List[str]:
    """Parse a statute meta line of text.

    For example:
      input:  'ORS 181A.235 & ORS 192'
      output: ['ORS 181A.235', 'ORS 192']
    """
    return [s.strip() for s in SEPARATOR.split(text)]


def parse_division(html: Selector) -> List[Rule]:
    rules = [parse_rule(rule_div) for rule_div in html.xpath('//div[@class="rule_div"]')]
    if len(rules) == 0:
        raise ParseException("Found no Rules in the Division")

    return rules


def parse_rule(rule_div: Selector) -> Rule:
    number = rule_div.css("strong > a::text").get().strip()
    name   = rule_div.css('strong::text').get().strip()

    return _parse_rule_content(rule_div, number, name)


def _parse_rule_content(rule_div: Selector, number: str, name: str) -> Rule:
    raw_paragraphs: List[str] = rule_div.xpath("p")[1:].getall()
    cleaned_up_paragraphs = [
        p.strip().replace("\n", "") for p in raw_paragraphs
    ]
    cleaned_up_paragraphs = [
        re.sub(r' +', ' ', p) for p in cleaned_up_paragraphs
    ]
    non_empty_paragraphs = list(filter(None, cleaned_up_paragraphs))
    content_paragaphs = non_empty_paragraphs[1:-1]

    meta_paragraph = non_empty_paragraphs[-1]
    metadata = meta_sections(meta_paragraph)

    return Rule(
        kind="Rule",
        number=number,
        name=name,
        url=oar_url(f"view.action?ruleNumber={number}"),
        text="\n".join(content_paragaphs),
        authority=metadata["authority"],
        implements=metadata["implements"],
        history=metadata["history"]
    )


URL_PREFIX = f"https://{DOMAIN}/oard/"


def oar_url(relative_fragment: str) -> str:
    return URL_PREFIX + relative_fragment
