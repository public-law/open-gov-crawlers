# pyright: reportGeneralTypeIssues=false
# pyright: reportCallIssue=false
# pyright: reportInvalidTypeForm=false
# pyright: reportAssignmentType=false
# pyright: reportRedeclaration=false
# pyright: reportArgumentType=false


import re
from functools import cache
from typing import Any, List, cast

from bs4 import BeautifulSoup
from pydantic import BaseModel, Field, conint
from tika import parser

from public_law.metadata import Metadata
from public_law.text import NonemptyString as S
from public_law.text import normalize_whitespace, titleize

LANGUAGE_MAP = {
    "Rome Statute of the International Criminal Court": "en-US",
    "Statut de Rome de la Cour pénale internationale": "fr",
    "نظام روما األسايس للمحكمة اجلنائية ادلويلة": "ar",
    "Estatuto de Roma de la Corte Penal Internacional": "es",
}

JSON_OUTPUT_URL_EN = "https://github.com/public-law/datasets/blob/master/Intergovernmental/RomeStatute/RomeStatute.json"


class FrozenModel(BaseModel):
    """Makes the model frozen."""

    class Config:
        frozen = True
        arbitrary_types_allowed = True


class Part(FrozenModel):
    """Represents a 'Part' in the text of the Rome Statute.
    It's basically like a chapter. A Part has many Articles."""

    number: conint(ge=1, le=13)
    name: str = Field(pattern=r"^[ a-zA-Z,]+$")


class Article(FrozenModel):
    """An 'Article' in the Rome Statute; an actual readable
    section of the statute. An Article belongs to one Part."""

    number: str  # Is string because of numbers like "8 bis".
    part_number: conint(ge=1, le=13)  
    name: str = Field(pattern=r"^[ a-zA-Z0-9,:\-\(\)]*$")  
    text: str

    def name(self) -> str:
        return cast(str, self.name)

    def part_number(self) -> int:
        return cast(int, self.part_number)


class Footnote(FrozenModel):
    """Represents a footnote in the document. Each one belongs
    to an Article. There are 10 in the English version."""

    number: conint(ge=1, le=10)
    article_number: S
    text: S


def footnotes() -> list[Footnote]:
    return [
        Footnote(
            number=1,
            article_number=S("5"),
            text=S(
                "Paragraph 2 of article 5 (“The Court shall exercise jurisdiction over the crime of aggression once a provision is adopted in accordance with articles 121 and 123 defining the crime and setting out the conditions under which the Court shall exercise jurisdiction with respect to this crime. Such a provision shall be consistent with the relevant provisions of the Charter of the United Nations.”) was deleted in accordance with RC/Res.6, annex I, of 11 June 2010."
            ),
        ),
        Footnote(
            number=2,
            article_number=S("8"),
            text=S(
                "Paragraphs 2 (e) (xiii) to 2 (e) (xv) were inserted by resolution RC/Res.5 of 11 June 2010. See depositary notification C.N.533.2010.TREATIES-6 of 29 November 2010. The UN Treaty Section website detailing the status of the amendment is available at: https://treaties.un.org/Pages/ViewDetails.aspx?src=TREATY&mtdsg_no=XVIII-10-a&chapter=18&clang=_en"
            ),
        ),
        Footnote(
            number=3,
            article_number=S("8"),
            text=S(
                "Paragraphs (2) (b) (xxvii) to (xxix) and 2 (e) (xvi) to (xviii) were inserted by resolution ICC-ASP/16/Res.4 of 14 December 2017. For the amendment regarding “weapons which use microbial or other biological agents, or toxins”, see depositary notification C.N.116.2018.TREATIES-XVIII-10 of 8 March 2018; the UN Treaty Section website detailing the status of the amendment is available at: https://treaties.un.org/Pages/ViewDetails.aspx?src=TREATY&mtdsg_no=XVIII-10-d&chapter=18&clang=_en. For the amendment regarding “weapons the primary effect of which is to injure by fragments undetectable by x-rays in the human body”, see depositary notification C.N.125.2018.TREATIES-XVIII-10 of 8 March 2018; the UN Treaty Section website detailing the status of the amendment is available at: https://treaties.un.org/PAGES/ViewDetails.aspx?src=TREATY&mtdsg_no=XVIII-10-e&chapter=18&clang=_en. For the amendment regarding “blinding laser weapons”, see depositary notification C.N.126.2018.TREATIES-XVIII-10 of 8 March 2018; the UN Treaty Section website detailing the status of the amendment is available at: https://treaties.un.org/Pages/ViewDetails.aspx?src=TREATY&mtdsg_no=XVIII-10-f&chapter=18&clang=_en."
            ),
        ),
        Footnote(
            number=4,
            article_number=S("8 bis"),
            text=S(
                "Article 8 bis was inserted by resolution RC/Res.6 of 11 June 2010. See depositary notification C.N.651.2010.TREATIES-8 of 29 November 2010. The UN Treaty Section website detailing the status of the amendment is available at: https://treaties.un.org/Pages/ViewDetails.aspx?src=TREATY&mtdsg_no=XVIII-10-b&chapter=18&clang=_en."
            ),
        ),
        Footnote(
            number=5,
            article_number=S("9"),
            text=S(
                "As amended by resolution RC/Res.6 of 11 June 2010 (inserting the reference to article 8 bis). See depositary notification C.N.651.2010.TREATIES-8 of 29 November 2010. The UN Treaty Section website detailing the status of the amendment is available at: https://treaties.un.org/Pages/ViewDetails.aspx?src=TREATY&mtdsg_no=XVIII-10-b&chapter=18&clang=_en"
            ),
        ),
        Footnote(
            number=6,
            article_number=S("15 bis"),
            text=S(
                "As amended by resolution RC/Res.6 of 11 June 2010. See depositary notification C.N.651.2010.TREATIES-8 of 29 November 2010. The UN Treaty Section website detailing the status of the amendment is available at: https://treaties.un.org/Pages/ViewDetails.aspx?src=TREATY&mtdsg_no=XVIII-10-b&chapter=18&clang=_en. As regards the status of declarations lodged with the Registrar under article 15 bis, paragraph 4, of the Rome Statute, please see: https://www.icc-cpi.int/resource-library#"
            ),
        ),
        Footnote(
            number=7,
            article_number=S("15 ter"),
            text=S(
                "Article 15 ter was inserted by resolution RC/Res.6 of 11 June 2010. See depositary notification C.N.651.2010. TREATIES-8 of 29 November 2010. The UN Treaty Section website detailing the status of the amendment is available at: https://treaties.un.org/Pages/ViewDetails.aspx?src=TREATY&mtdsg_no=XVIII-10-b&chapter=18&clang=_en."
            ),
        ),
        Footnote(
            number=8,
            article_number=S("20"),
            text=S(
                "As amended by resolution RC/Res.6 of 11 June 2010 (inserting the reference to article 8 bis). See depositary notification C.N.651.2010.TREATIES-8 of 29 November 2010. The UN Treaty Section website detailing the status of the amendment is available at: https://treaties.un.org/Pages/ViewDetails.aspx?src=TREATY&mtdsg_no=XVIII-10-b&chapter=18&clang=_en."
            ),
        ),
        Footnote(
            number=9,
            article_number=S("25"),
            text=S(
                "As amended by resolution RC/Res.6 of 11 June 2010 (adding paragraph 3 bis). See depositary notification C.N.651.2010. TREATIES-8 of 29 November 2010. The UN Treaty Section website detailing the status of the amendment is available at: https://treaties.un.org/Pages/ViewDetails.aspx?src=TREATY&mtdsg_no=XVIII-10-b&chapter=18&clang=_en."
            ),
        ),
        Footnote(
            number=10,
            article_number=S("124"),
            text=S(
                "Article 124 was deleted by resolution ICC-ASP/14/Res.2 of 26 November 2015. See depositary notification C.N.7.2016. treaties XVIII.10 of 15 January 2016C. The UN Treaty Section website detailing the status of the amendment is available at: https://treaties.un.org/Pages/ViewDetails.aspx?src=TREATY&mtdsg_no=XVIII-10-c&chapter=18&clang=_en."
            ),
        ),
    ]


def new_metadata(pdf_url: str) -> Metadata:
    # pdf_data = metadata(pdf_url)

    return Metadata(
        dc_identifier=S(JSON_OUTPUT_URL_EN),
        dc_source=S(pdf_url),
        dc_title=S(title(pdf_url)),
        dc_language=S(language(pdf_url)),
    )


@cache
def parts(pdf_url: str) -> list[Part]:
    """Parse all the Parts from the Rome Statute PDF."""
    soup = BeautifulSoup(tika_pdf(pdf_url)["content"], "html.parser")
    part_paragraphs = [
        normalize_whitespace(p.get_text())
        for p in soup.find_all("p")
        if p.get_text().startswith("PART")
    ]

    part_objects: list[Part] = []
    for paragraph in part_paragraphs:

        match re.findall(r"^PART (\d+)\. +(\D+)", paragraph):
            case [(number, name)]:
                part_objects.append(
                    Part(
                        number=number,
                        name=S(normalize_whitespace(titleize(name))),
                    )
                )
            case _:
                raise Exception(
                    f"The paragraph didn't match the Part regex: {paragraph}"
                )

    part_objects = list(dict.fromkeys(part_objects).keys())
    return part_objects


def articles(pdf_url: str) -> list[Article]:
    """Given the html document, return a list of Articles."""

    html = tika_pdf(pdf_url)["content"]
    article_objects: list[Article] = []
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
    return re.split(r"(?=<p>Article\s\d+\s.*\n)", _clean_part(part))


def _article(article: str, part_number: int) -> Article:
    """Split a raw article and return as an Article"""

    soup = BeautifulSoup(article, features="lxml")
    raw_article = re.split(r"\n", soup.get_text(), 2)

    name = normalize_whitespace(raw_article[1]).strip()

    return Article(
        name=name,
        number=raw_article[0].split(" ", 1)[1].strip(),
        text=_clean_article_text(raw_article[2].strip()),
        part_number=part_number,
    )


def _clean_part(part: str) -> str:
    """Remove page numbers and annotation links from a part."""
    part = re.sub(r'<div\sclass="page">.*\n<p>\d+', "", part)
    return _remove_annotation_links(part, r"^<div\sclass='annotation'>.*\n?")


def _remove_extra_newlines(text: str) -> str:
    """Remove all extra/unwanted newlines."""
    raw_text = re.sub(r"\n\n+", "\n\n", text).split("\n\n")
    return "\n".join([normalize_whitespace(t.replace("\n", "")) for t in raw_text])


def _remove_annotation_links(text: str, pattern: str) -> str:
    """Remove hyperlinks from the annotations."""
    return re.sub(pattern, "", text, flags=re.MULTILINE)


def _current_article_num(number_raw: str, current_article_num: int) -> int:
    """
    Keep track of the digits of the article number.
    This is necessary in order to get the correct article numbers from annotated articles.
    For example, article 124 has annotation 10, but the two are written together as "12410"
    in the raw document.
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
        if len(name_text) > 1 and len(article.name) == 0:
            name = name_text[0].strip()
            text = name_text[1].strip()
        annotations = [int(x) for x in annotation.split()]
        for annotation in annotations:
            text = re.sub(rf"^{annotation}\s.*\n?", "", text, flags=re.MULTILINE)
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
    return re.sub(
        page_title,
        "",
        text,
    ).strip()


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


def metadata(pdf_url: str) -> dict[str, Any]:
    return tika_pdf(pdf_url)["metadata"]


@cache
def tika_pdf(pdf_url: str) -> dict[str, Any]:
    return parser.from_file(pdf_url, xmlContent=True)  # type: ignore
