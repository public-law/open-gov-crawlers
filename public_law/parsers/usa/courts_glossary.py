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
    cleanup,
    Sentence,
)


def parse_glossary(response: HtmlResponse) -> GlossaryParseResult:
    """
    Parses the US Courts glossary page and returns a GlossaryParseResult
    to the Spider.
    """
    # A GlossaryParseResult is a class with just two attributes:
    # the entries and metadata.

    # 1. Create the two pieces of the GlossaryParseResult.
    entries  = _parse_entries(response)       # Parse the entries from the HTML response
    metadata = us_courts_glossary_metadata()  # Call the metadata function

    # 2. Create and return a new GlossaryParseResult object that wraps them up.
    return GlossaryParseResult(entries=entries, metadata=metadata)


def _parse_entries(response: HtmlResponse) -> list[GlossaryEntry]:
    """
    The entries are the <dt> (term) and <dd> (definition) pairs in the <dl>
    definition list:

    <dl>
      <dt>Acquittal</dt>
      <dd>A jury verdict that a criminal defendant is not guilty...</dd>

      <dt>Adversary</dt>
      <dd>A party to a lawsuit who is not the plaintiff or the defendant.</dd>
      ...
    </dl>

    This function parses the <dl> definition list into a list of
    GlossaryEntry objects.
    """
    soup = make_soup(response)                 # Parse the HTML response into a BeautifulSoup object
    dt_list, dd_list = soup("dt"), soup("dd")  # Extract all <dt> (terms) and <dd> (definitions)
    assert len(dt_list) == len(dd_list)        # Ensure each term has a definition
    list_of_pairs = zip(dt_list, dd_list)      # Pair each <dt> with its corresponding <dd>

    # Convert the list of pairs into a list of GlossaryEntry objects
    return [
        GlossaryEntry(phrase=cleanup(dt.text), definition=Sentence(dd.text))
        for dt, dd in list_of_pairs
    ]
