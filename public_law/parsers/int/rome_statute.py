from functools import cache
from tika import parser


def title(pdf_url: str) -> str:
    return metadata(pdf_url)["dc:title"]


def metadata(pdf_url: str) -> dict:
    return tika_pdf(pdf_url)["metadata"]


@cache
def tika_pdf(pdf_url: str) -> dict:
    return parser.from_file(pdf_url, xmlContent=True)
