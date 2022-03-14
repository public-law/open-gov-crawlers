from functools import cache
from tika import parser


@cache
def tika_pdf(url: str) -> dict:
    return parser.from_file(url, xmlContent=True)


def metadata(url: str) -> dict:
    return tika_pdf(url)["metadata"]
