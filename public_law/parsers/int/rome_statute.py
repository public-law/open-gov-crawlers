from functools import cache
import re
from typing import NamedTuple
from tika import parser
from bs4 import BeautifulSoup
from titlecase import titlecase

from public_law.text import NonemptyString


LANGUAGE_MAP = {
    "Rome Statute of the International Criminal Court": "en",
    "Statut de Rome de la Cour pénale internationale": "fr",
    "نظام روما األسايس للمحكمة اجلنائية ادلويلة": "ar",
    "Estatuto de Roma de la Corte Penal Internacional": "es",
}


class Part(NamedTuple):
    """Represents one term and its definition in a particular Glossary"""

    name: NonemptyString

    def __repr__(self) -> str:
        return self._asdict().__repr__()


def parts(pdf_url: str) -> list[Part]:
    soup = BeautifulSoup(tika_pdf(pdf_url)["content"], "html.parser")
    part_paragraphs = [
        p.get_text().strip().replace("\n", " ")
        for p in soup.find_all("p")
        if p.get_text().startswith("PART")
    ]
    just_the_names = [re.sub(r"PART \d+\. +", "", n) for n in part_paragraphs]
    just_the_names = [re.sub(r" \d+$", "", n) for n in just_the_names]

    parts = [Part(name=NonemptyString(titlecase(n))) for n in just_the_names]

    return parts


def language(pdf_url: str) -> str:
    return LANGUAGE_MAP[title(pdf_url)]


def modified_at(pdf_url: str) -> str:
    return metadata(pdf_url)["dcterms:modified"]


def title(pdf_url: str) -> str:
    # TODO: Somehow get rid of this hack. The Spanish-language
    #       version doesn't have a `dc:title` attribute.
    if "dc:title" not in metadata(pdf_url):
        return "Estatuto de Roma de la Corte Penal Internacional"

    return metadata(pdf_url)["dc:title"]


def metadata(pdf_url: str) -> dict:
    return tika_pdf(pdf_url)["metadata"]


@cache
def tika_pdf(pdf_url: str) -> dict:
    return parser.from_file(pdf_url, xmlContent=True)
