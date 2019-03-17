from typing import Tuple


def statute_meta(text: str) -> Tuple[str]:
    """
    Parse a statute meta line of text.
    For example:
    input:  'ORS 181A.235 & ORS 192'
    output: ('181A.235', 'ORS 192')
    """
    return (text,)
