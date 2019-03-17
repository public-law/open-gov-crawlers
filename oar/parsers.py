import re
from typing import List

SEPARATOR = re.compile(r"[,&]")


def statute_meta(text: str) -> List[str]:
    """
    Parse a statute meta line of text.

    For example:
    input:  'ORS 181A.235 & ORS 192'
    output: ['181A.235', 'ORS 192']
    """
    return [s.strip() for s in SEPARATOR.split(text)]
