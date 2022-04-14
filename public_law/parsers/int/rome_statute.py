import re
from functools import cache
from typing import NamedTuple, List

from bs4 import BeautifulSoup
from public_law.metadata import Metadata
from public_law.text import NonemptyString as S, normalize_whitespace
from tika import parser
from titlecase import titlecase

LANGUAGE_MAP = {
    "Rome Statute of the International Criminal Court": "en-US",
    "Statut de Rome de la Cour pénale internationale": "fr",
    "نظام روما األسايس للمحكمة اجلنائية ادلويلة": "ar",
    "Estatuto de Roma de la Corte Penal Internacional": "es",
}

JSON_OUTPUT_URL_EN = "https://github.com/public-law/datasets/blob/master/Intergovernmental/RomeStatute/RomeStatute.json"  # pylint:disable=line-too-long


class Part(NamedTuple):
    """Represents a 'Part' in the text of the Rome Statute.
    It's basically like a chapter. A Part has many Articles."""

    number: int
    name: S


class Article(NamedTuple):
    """An 'Article' in the Rome Statute; an actual readable
    section of the statute. An Article belongs to one Part."""

    number: str  # Is string because of numbers like "8 bis".
    part_number: int
    name: str
    text: str


def new_metadata(pdf_url: str) -> Metadata:
    pdf_data = metadata(pdf_url)

    return Metadata(
        dc_creator=S(pdf_data["dc:creator"]),
        dc_identifier=S(JSON_OUTPUT_URL_EN),
        dc_source=S(pdf_url),
        dc_title=S(title(pdf_url)),
        dc_language=S(language(pdf_url)),
    )


def parts(pdf_url: str) -> list[Part]:
    """Parse all the Parts from the Rome Statute PDF."""
    soup = BeautifulSoup(tika_pdf(pdf_url)["content"], "html.parser")
    part_paragraphs = [
        normalize_whitespace(p.get_text())
        for p in soup.find_all("p")
        if p.get_text().startswith("PART")
    ]

    part_objects = []
    for paragaph in part_paragraphs:
        if matches := re.match(r"^PART (\d+)\. +([^\d]+)", paragaph):
            number = matches.group(1)
            name = matches.group(2)

            part_objects.append(
                Part(
                    number=int(number),
                    name=S(normalize_whitespace(titlecase(name))),
                )
            )
        else:
            raise Exception(
                f"The paragraph didn't match the Part regex: {paragaph}"
            )

    part_objects = list(dict.fromkeys(part_objects).keys())
    return part_objects


def articles(pdf_url: str) -> list[Article]:
    """Given the html document, return a list of Articles."""

    html = tika_pdf(pdf_url)["content"]
    article_objects = []
    current_article_num = 0
    document_body = _document_body(
        html, "<p>Have agreed as follows:</p>", "<li>art.9</li>"
    )

    for part_number, part in enumerate(
        _parts(document_body, r"<p>PART\s[0-9]+"), start=1
    ):
        for raw_article in _articles_in_part(part):
            article = _article(raw_article, part_number)
            if article.number:

                current_article_num = _current_article_num(
                    article.number, current_article_num
                )
                number = _article_number(article.number, current_article_num)
                article_objects.append(_remove_annotations(article, number))

    return article_objects


def _document_body(text: str, top: str, bottom: str) -> str:
    """The document body with table of contents etc. removed"""
    return text.split(top)[1].split(bottom)[0]


def _parts(text: str, pattern: str) -> List[str]:
    """Raw parts."""
    return re.split(pattern, text)[1:]


def _articles_in_part(part: str) -> List[str]:
    """Raw Articles in a part."""
    return re.split(r"(?=<p>Article\s[0-9]+\s.*\n)", _clean_part(part))


def _article(article: str, part_number: int) -> Article:
    """Split a raw article and return as an Article"""

    soup = BeautifulSoup(article, features="lxml")
    raw_article = re.split(r"\n", soup.get_text(), 2)

    return Article(
        name=normalize_whitespace(raw_article[1]).strip(),
        number=raw_article[0].split(" ", 1)[1].strip(),
        text=_clean_article_text(raw_article[2].strip()),
        part_number=part_number,
    )


def _clean_part(part: str) -> str:
    """Remove page numbers and annotation links from a part."""
    part = re.sub(r'<div\sclass="page">.*\n<p>[0-9]+', "", part)
    return _remove_annotation_links(part, r"^<div\sclass='annotation'>.*\n?")


def _remove_extra_newlines(text: str) -> str:
    """Remove all extra/unwanted newlines."""
    raw_text = re.sub(r"\n\n\n*", "\n\n", text).split("\n\n")
    return "\n".join(
        [normalize_whitespace(t.replace("\n", "")) for t in raw_text]
    )


def _remove_annotation_links(text: str, pattern: str) -> str:
    """Remove hyperlinks from the annotations."""
    return re.sub(pattern, "", text, flags=re.MULTILINE)


def _current_article_num(number_raw: str, current_article_num: int) -> int:
    """
    Keep track of the digits of the article number.
    This is necesary in order to get the correct article numbers from annotated articles.
    For example, article 124 has annotation 10, but they two are written together as "12410" in the
    raw document.
    """
    if str(number_raw).startswith(str(current_article_num + 1)):
        return current_article_num + 1
    return current_article_num


def _article_number(number_raw: str, current_article_num: int) -> str:
    """Article number"""
    if "bis" in number_raw:
        number = str(current_article_num) + " bis"
    elif "ter" in number_raw:
        number = str(current_article_num) + " ter"
    else:
        number = str(current_article_num)
    return number


def _remove_annotations(article: Article, number: str) -> Article:
    """Remove annotations from text if they exist."""
    name = article.name
    text = article.text
    annotation = article.number.replace(str(number), "")
    if annotation:
        name_text = article.text.split("\n", 1)
        if len(name_text) > 1 and not article.name:
            name = name_text[0].strip()
            text = name_text[1].strip()
        annotations = [int(x) for x in annotation.split()]
        for annotation in annotations:
            text = re.sub(
                rf"^{annotation}\s.*\n?", "", text, flags=re.MULTILINE
            )
    return Article(
        name=name,
        number=number,
        text=text.replace("\n\n", "\n"),
        part_number=article.part_number,
    )


def _clean_article_text(text: str) -> str:
    """Article text with page titles and superfluous newlines removed"""
    return _remove_page_title(
        _remove_extra_newlines(text),
        r"Rome\sStatute\sof\sthe\sInternational\sCriminal\sCourt",
    )


def _remove_page_title(text: str, page_title: str) -> str:
    """Remove page titles from the document."""
    return re.sub(page_title, "", text,).strip()


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
