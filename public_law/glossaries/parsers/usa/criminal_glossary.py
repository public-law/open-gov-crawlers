from typed_soup import from_response, TypedSoup
from scrapy.http.response.html import HtmlResponse

from ...models.glossary import GlossaryEntry
from ....shared.utils.text import (
    NonemptyString as String,
    Sentence, ensure_ends_with_period,
)


def parse_entries(html: HtmlResponse) -> tuple[GlossaryEntry, ...]:
    """Parse the glossary entries from the HTML response.

    The entries are in a table, with each <tr> containing two <td>s: 
    the first is the phrase, the second is the definition.
    """
    match(from_response(html).find("table")):
        case None:
            return tuple()
        case table:
            return tuple(
                entry for row in table("tr")
                if (entry := _process_row(row)) is not None
            )


def _process_row(row: TypedSoup) -> GlossaryEntry | None:
    cells = row("td")
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
