from functools import cache
import re
from typing import NamedTuple
from tika import parser
from bs4 import BeautifulSoup
from titlecase import titlecase

from public_law.text import NonemptyString, normalize_whitespace


LANGUAGE_MAP = {
    "Rome Statute of the International Criminal Court": "en",
    "Statut de Rome de la Cour pénale internationale": "fr",
    "نظام روما األسايس للمحكمة اجلنائية ادلويلة": "ar",
    "Estatuto de Roma de la Corte Penal Internacional": "es",
}


class Part(NamedTuple):
    """Represents a 'Part' in the text of the Rome Statute.
    It's basically like a chapter. A Part has many Articles."""

    name: NonemptyString
    number: int

    def __repr__(self) -> str:
        return self._asdict().__repr__()


class Article(NamedTuple):
    """An 'Article' in the Rome Statute; an actual readable
    section of the statute. An Article belongs to one Part."""

    name: str
    number: str  # Is string because of numbers like "8 bis".
    text: str
    part_number: int


def articles(html: str) -> list[Article]:
    """Given the html document, return a list of Articles."""

    articles = []

    # Get only the part that contains the relevant content
    articles_middle = html.split("<p>Have agreed as follows:</p>")[1]
    articles_middle = articles_middle.split("<li>art.9</li>")[0]

    # Split by parts
    rx_parts = re.compile(r"<p>PART\s[0-9]+")
    parts = rx_parts.split(articles_middle)
    current_article_num = 0

    for idx, part in enumerate(parts[1:]):
        part_number = idx + 1

        # Remove page numbers.
        rx_page_number = re.compile(r'<div\sclass="page">.*\n<p>[0-9]+')
        part = rx_page_number.sub("", part)

        # Extract each article.
        rx_articles = re.compile(r"(?=<p>Article\s[0-9]+\s.*\n)")
        articles_raw = rx_articles.split(part)
        for article in articles_raw:
            number = ""
            # Remove tags.
            soup = BeautifulSoup(article, features="lxml")
            article = soup.get_text().split("\n", 2)

            # Extract number, name and text from each article.
            number_raw = article[0].split(" ", 1)[1].strip()
            name = normalize_whitespace(article[1]).strip()
            text = article[2].strip()

            # Remove all extra/unwanted newlines.
            rx_extra_lines = re.compile(r"\n\n\n*")
            text = rx_extra_lines.sub("\n\n", text)
            text = text.split("\n\n")
            text = "\n".join(
                [normalize_whitespace(t.replace("\n", "")) for t in text]
            )

            # Remove the title of each page.
            rx_page_title = re.compile(
                r"Rome\sStatute\sof\sthe\sInternational\sCriminal\sCourt"
            )
            text = rx_page_title.sub("", text).strip()

            # Get number.
            if number_raw:
                if str(number_raw).startswith(str(current_article_num + 1)):
                    current_article_num += 1
                if "bis" in number_raw:
                    number = str(current_article_num) + " bis"
                elif "ter" in number_raw:
                    number = str(current_article_num) + " ter"
                else:
                    number = str(current_article_num)

                # Build Article
                articles.append(
                    Article(
                        name=str(name),
                        number=str(number),
                        text=str(text),
                        part_number=int(part_number),
                    )
                )
    return articles


def parts(pdf_url: str) -> list[Part]:
    """Parse all the Parts from the Rome Statute PDF."""
    soup = BeautifulSoup(tika_pdf(pdf_url)["content"], "html.parser")
    part_paragraphs = [
        normalize_whitespace(p.get_text())
        for p in soup.find_all("p")
        if p.get_text().startswith("PART")
    ]

    parts = []
    for paragaph in part_paragraphs:
        if matches := re.match(r"^PART (\d+)\. +([^\d]+)", paragaph):
            number = matches.group(1)
            name = matches.group(2)

            parts.append(
                Part(
                    number=int(number),
                    name=NonemptyString(normalize_whitespace(titlecase(name))),
                )
            )
        else:
            raise Exception(f"The paragraph didn't match the Part regex: " + paragaph)

    parts = list(dict.fromkeys(parts).keys())
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
