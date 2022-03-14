from functools import cache
from tika import parser

LANGUAGE_MAP = {
    "Rome Statute of the International Criminal Court": "en",
    "Statut de Rome de la Cour pénale internationale": "fr",
}


def language(pdf_url: str) -> str:
    pdf_title = title(pdf_url)
    if pdf_title not in LANGUAGE_MAP:
        raise Exception("Unknown language")

    return LANGUAGE_MAP[pdf_title]


def modified_at(pdf_url: str) -> str:
    return metadata(pdf_url)["dcterms:modified"]


def title(pdf_url: str) -> str:
    return metadata(pdf_url)["dc:title"]


def metadata(pdf_url: str) -> dict:
    return tika_pdf(pdf_url)["metadata"]


@cache
def tika_pdf(pdf_url: str) -> dict:
    return parser.from_file(pdf_url, xmlContent=True)
