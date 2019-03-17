import re
from typing import List


def statute_meta(text: str) -> List[str]:
    """
    Parse a statute meta line of text.
    For example:
    input:  'ORS 181A.235 & ORS 192'
    output: ('181A.235', 'ORS 192')
    """
    stemmed_text = text.replace("&", "").replace("  ", " ")
    return re.findall(r"ORS [^ ]+", stemmed_text)
