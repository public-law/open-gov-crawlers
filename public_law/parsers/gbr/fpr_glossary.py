from datetime import date
from typing import cast
from datetime import datetime

from bs4 import BeautifulSoup, Tag
from scrapy.http.response.html import HtmlResponse

from ...metadata import Metadata, Subject
from ...models.glossary import GlossaryEntry, GlossaryParseResult
from ...text import URL, LoCSubject, WikidataTopic
from ...text import NonemptyString as String
from ...text import Sentence, ensure_ends_with_period, make_soup, normalize_nonempty


def parse_glossary(html: HtmlResponse) -> GlossaryParseResult:
    """
    The top-level, public function of this module. It performs the
    complete parse of the HTTP response.
    """
    metadata = _make_metadata(html)
    entries = _parse_entries(html)

    return GlossaryParseResult(metadata, entries)


def _make_metadata(html: HtmlResponse) -> Metadata:
    source_url = URL(html.url)
    subjects = (
        Subject(LoCSubject("sh85033571"), String("Courts")),
        Subject(WikidataTopic("Q41487"),  String("Court")),
    )

    return Metadata(
        dcterms_title=String("Family Procedure Rules Glossary"),
        dcterms_language="en",
        dcterms_coverage="GBR",
        # Info about original source
        dcterms_source=source_url,
        publiclaw_sourceModified=_parse_mod_date(html),
        publiclaw_sourceCreator=String("Ministry of Justice"),
        dcterms_subject=subjects,
    )


def _parse_mod_date(html: HtmlResponse) -> date:
    """
    Parse the modification date from the HTML.
    Format: "Monday, 30 January 2017"
    """
    try:
        soup = make_soup(html)
        date_span = soup.find("span", class_="right")
        if not date_span:
            return datetime.now().date()

        date_text = date_span.text
        date_str = date_text.replace("Updated: ", "").strip()

        return datetime.strptime(date_str, "%A, %d %B %Y").date()
    except Exception:
        return datetime.now().date()


def _parse_entries(html: HtmlResponse) -> tuple[GlossaryEntry, ...]:
    """
    Parse the glossary entries from the HTML response.
    The entries are in a definition list (<dl>) with <dt> for terms and <dd> for definitions.
    """
    soup = make_soup(html)
    dl = soup.find("dl", class_="wp-block-simple-definition-list-blocks-list")
    if not dl or not isinstance(dl, Tag):
        return tuple()

    # Skip the header row (first dt/dd pair)
    terms = list(dl.find_all("dt"))[1:]  # Skip first dt
    definitions = list(dl.find_all("dd"))[1:]  # Skip first dd

    if not terms or not definitions or len(terms) != len(definitions):
        return tuple()

    return tuple(
        GlossaryEntry(
            phrase=normalize_nonempty(term.text),
            definition=Sentence(
                ensure_ends_with_period(
                    normalize_nonempty(defn.text.replace(
                        "“", '"').replace("”", '"'))
                )
            ),
        )
        for term, defn in zip(terms, definitions)
    )
