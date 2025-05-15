from datetime import date
from typing import cast

from scrapy.http.response.html import HtmlResponse

from ...metadata import Metadata, Subject
from ...models.glossary import GlossaryEntry, GlossaryParseResult
from ...text import URL, LoCSubject
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
        Subject(LoCSubject("sh85033572"), String("Family courts")),
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
    Parse the modification date from the footer.
    Format: "Monday, 30 January 2017"
    """
    try:
        soup = make_soup(html)
        date_text = soup.find_all("p")[-2].text  # Second to last paragraph
        date_str = date_text.replace("Updated: ", "").strip()

        # Parse the date string
        from datetime import datetime
        return datetime.strptime(date_str, "%A, %d %B %Y").date()
    except Exception:
        return date.today()


def _parse_entries(html: HtmlResponse) -> tuple[GlossaryEntry, ...]:
    """
    Parse the glossary entries from the HTML response.
    The entries are in a table with two columns: Expression and Meaning.
    """
    soup = make_soup(html)
    rows = soup.find_all("tr")[1:]  # Skip header row

    return tuple(
        GlossaryEntry(
            phrase=normalize_nonempty(row.find("td").text),
            definition=Sentence(
                ensure_ends_with_period(
                    normalize_nonempty(row.find_all("td")[1].text)
                )
            ),
        )
        for row in rows
        if row.find("td") and len(row.find_all("td")) >= 2
    )
