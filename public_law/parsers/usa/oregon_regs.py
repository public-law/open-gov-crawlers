import re

from scrapy.http.response import Response
from scrapy.selector.unified import Selector

from ...exceptions import ParseException
from ...items.oar import Rule
from ...text import delete_all

SEPARATOR = re.compile(r"(?<=\d),|&amp;")
DOMAIN = "secure.sos.state.or.us"
URL_PREFIX = f"https://{DOMAIN}/oard/"


def oar_url(relative_fragment: str) -> str:
    return URL_PREFIX + relative_fragment


def parse_division(html: Response) -> list[Rule]:
    """A 'Division' has an HTML page which lists many Rules."""

    # rules = [
    #     _parse_rule(rule_div) for rule_div in html.xpath('//div[@class="rule_div"]')
    # ]

    # if len(rules) == 0:
    #     raise ParseException("Found no Rules in the Division")

    # return rules

    match [
        _parse_rule(rule_div) for rule_div in html.xpath('//div[@class="rule_div"]')  # type: ignore
    ]:
        case []:
            raise ParseException("Found no Rules in the Division")
        case rules:
            return rules


def _parse_rule(rule_div: Selector) -> Rule:
    """A Rule has a number, name, text, and metadata."""

    number = _parse_number(rule_div)
    name = _parse_name(rule_div)
    text, metadata = _parse_content(rule_div)

    source_url = _rule_url(number)

    return Rule(
        number=number,
        name=name,
        text=text,
        authority=metadata["authority"],
        implements=metadata["implements"],
        history=metadata["history"],
        url=source_url,
        kind="Rule",
    )


def _parse_number(rule_div: Selector) -> str:
    return rule_div.css("strong > a::text").get(" ").strip() # type: ignore


def _parse_name(rule_div: Selector) -> str:
    return rule_div.css("strong::text").get(" ").strip() # type: ignore


def _parse_content(rule_div: Selector) -> tuple[str, dict[str, list[str] | str]]:
    """Parse the given HTML div for the text string and metadata dict."""

    # Parse the body text
    raw_paragraphs: list[str] = rule_div.xpath("p")[1:].getall()
    cleaned_up_paragraphs = [p.strip().replace("\n", "") for p in raw_paragraphs]
    cleaned_up_paragraphs = [re.sub(r" +", " ", p) for p in cleaned_up_paragraphs]
    non_empty_paragraphs = list(filter(None, cleaned_up_paragraphs))
    content_paragraphs = non_empty_paragraphs[1:-1]
    body_text = "\n".join(content_paragraphs)

    # Parse the metadata
    meta_paragraph = non_empty_paragraphs[-1]
    metadata = _meta_sections(meta_paragraph)

    return (body_text, metadata)


def _rule_url(number: str) -> str:
    return URL_PREFIX + f"view.action?ruleNumber={number}"


def _meta_sections(text: str) -> dict[str, list[str] | str]:
    """
    A Rule always has some meta-info. It's three distinct optional sections,
    Authority, Implements, and History. Parse the given text into these three
    sections.
    """

    # Somewhat tricky: The history section uses embedded <br>
    # tags, so we want to leave those in place. Therefore, we want
    # to use just the first two <br>'s to split the meta section
    # into three parts.
    authority = implements = ""

    match (
        "Other Authority" in text,
        "Other Implemented" in text,
    ):
        case [False, False]:
            history = text
        case [False, True]:
            implements, history = text.split("<br>", maxsplit=1)
        case [True, False]:
            authority, history = text.split("<br>", maxsplit=1)
        case _:
            authority, implements, history = text.split("<br>", maxsplit=2)

    return {
        "authority": _list_meta(authority),
        "implements": _list_meta(implements),
        "history": _string_meta(history),
    }


def _list_meta(section: str) -> list[str]:
    if section == "":
        return []
    return _statute_meta(section.split("</b>")[1].strip())


def _string_meta(section: str) -> str:
    return delete_all(section, ["<p>", "<b>History:</b><br>", "<br> </p>"]).strip()


def _statute_meta(text: str) -> list[str]:
    """Parse a statute meta line of text.

    For example:
      input:  'ORS 181A.235 & ORS 192'
      output: ['ORS 181A.235', 'ORS 192']
    """
    return [s.strip() for s in SEPARATOR.split(text)]
