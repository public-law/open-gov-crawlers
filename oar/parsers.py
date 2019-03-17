from typing import List


def statute_meta(text: str) -> List[str]:
    """
    Parse a statute meta line of text. E.g.,
    input:  'ORS 181A.235 & ORS 192'
    output: ['181A.235', 'ORS 192']
    """
    return [text]
