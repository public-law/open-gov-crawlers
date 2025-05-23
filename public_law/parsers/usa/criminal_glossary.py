from scrapy.http.response.html import HtmlResponse

from ...metadata import Metadata, Subject
from ...models.glossary import GlossaryEntry, GlossaryParseResult
from ...text import URL, LoCSubject, WikidataTopic
from ...text import NonemptyString as String
from ...text import Sentence, ensure_ends_with_period
from ...html import parse_html, TypedSoup


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
        Subject(LoCSubject("sh85034086"), String("Criminal Procedure")),
        Subject(WikidataTopic("Q146071"), String("Criminal Procedure")),
    )

    return Metadata(
        dcterms_title=String("Criminal Glossary"),
        dcterms_language="en",
        dcterms_coverage="USA",
        # Info about original source
        dcterms_source=source_url,
        publiclaw_sourceModified="unknown",
        publiclaw_sourceCreator=String(
            "Superior Court of California, County of San Diego"),
        dcterms_subject=subjects,
    )


def _parse_entries(html: HtmlResponse) -> tuple[GlossaryEntry, ...]:
    """Parse the glossary entries from the HTML response.

    The entries are in a table, with each <tr> containing two <td>s: 
    the first is the phrase, the second is the definition.
    """
    match(parse_html(html).find("table")):
        case None:
            return tuple()
        case table:
            return tuple(
                entry for row in table.find_all("tr")
                if (entry := _process_row(row)) is not None
            )


def _process_row(row: TypedSoup) -> GlossaryEntry | None:
    cells = row.find_all("td")
    if len(cells) < 2:
        return None

    phrase = cells[0].get_text()
    definition = cells[1].get_text()

    if not phrase or not definition:
        return None

    return GlossaryEntry(
        phrase=String(phrase),
        definition=Sentence(
            ensure_ends_with_period(definition)),
    )
