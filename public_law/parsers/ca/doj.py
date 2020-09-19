from typing import List, NamedTuple, Union
from scrapy.http import Response


class GlossarySourceParseResult(NamedTuple):
    """All the info about a glossary source"""

    name: str


def parse_glossary(html: Response) -> GlossarySourceParseResult:
    return GlossarySourceParseResult(name="xxx")
