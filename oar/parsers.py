import re
from typing import Any, Dict, List
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
