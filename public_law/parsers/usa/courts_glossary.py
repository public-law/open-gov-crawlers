# This parser is a simple, clear example for onboarding new developers.
# It demonstrates how to extract a glossary from a <dl> (definition list) HTML
# structure. The code is intentionally straightforward and well-commented for
# learning purposes.
#
# How execution reaches this code:
#   - Scrapy first runs the paired us_courts_glossary Spider.
#   - The Spider is responsible for downloading the glossary web page.
#   - Once the page is downloaded, the Spider calls the parse_glossary function
#     below to extract structured data.
#
# The glossary source: https://www.uscourts.gov/glossary
#
# The <dl> element contains <dt> (term) and <dd> (definition) pairs. We parse
# these into structured GlossaryEntry objects.

from scrapy.http.response.html import HtmlResponse

from ...glossary_metadata import us_courts_glossary_metadata
from ...models.glossary import GlossaryEntry, GlossaryParseResult
from ...text import (
    make_soup,
    normalize_nonempty,
    Sentence,
)


def parse_glossary(response: HtmlResponse) -> GlossaryParseResult:
    """
    Parses the US Courts glossary page and returns a GlossaryParseResult.
    """
    entries = _parse_entries(response)
    metadata = us_courts_glossary_metadata()
    return GlossaryParseResult(entries=entries, metadata=metadata)


def _parse_entries(response: HtmlResponse) -> tuple[GlossaryEntry, ...]:
    """
    Parses the <dl> definition list into a tuple of GlossaryEntry objects.
    Each <dt> is a term, and each <dd> is its definition.
    """
    soup = make_soup(response)
    dt_list, dd_list = soup("dt"), soup("dd")
    assert len(dt_list) == len(dd_list), "Mismatched <dt> and <dd> count"
    return tuple(
        GlossaryEntry(
            phrase=normalize_nonempty(dt.text),
            definition=Sentence(dd.text),
        )
        for dt, dd in zip(dt_list, dd_list)
    )
