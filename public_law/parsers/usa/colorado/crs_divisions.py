# pyright: reportUnknownMemberType=false
# pyright: reportOptionalMemberAccess=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownLambdaType=false


from scrapy.selector.unified import Selector
from scrapy.http.response import Response

from typing import Any

from public_law.selector_util import just_text
from public_law.text import NonemptyString
from public_law.items.crs import Division, Subdivision
from public_law.parsers.usa.colorado.crs_articles import div_name_text, parse_articles_from_division



def parse_divisions(title_number: NonemptyString, dom: Selector | Response, logger: Any) -> list[Division]:
    division_nodes = dom.xpath("//T-DIV")

    divs = []
    for div_node in division_nodes:
        name = div_name_text(div_node)
        if name is None:
            logger.warn(f"Could not parse division name in {div_node.get()}, Title {title_number}")
            continue

        try:
            if _has_subdivisions(dom):
                if Division.is_valid_raw_name(name):
                    divs.append(
                        Division(
                            raw_name     = name,
                            children     = parse_subdivisions_from_division(title_number, dom, name),
                            title_number = title_number
                            )
                        )
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


def _has_subdivisions(dom: Selector | Response) -> bool:
    raw_div_names = [just_text(e) for e in dom.xpath("//TITLE-ANAL/T-DIV")]
    
    return not all([Division.is_valid_raw_name(n) for n in raw_div_names])


def parse_subdivisions_from_division(title_number: NonemptyString, dom: Selector | Response, raw_div_name: str) -> list[Subdivision]:
    return []
