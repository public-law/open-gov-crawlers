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

from ...metadata import Metadata, Subject
from ...models.glossary import GlossaryEntry, GlossaryParseResult
from ...text import (
    URL,
    LoCSubject,
    NonemptyString as String,
    Sentence,
    make_soup,
    normalize_nonempty,
)


def parse_glossary(response: HtmlResponse) -> GlossaryParseResult:
    """
    Main entry point for parsing the glossary page.
    Returns a GlossaryParseResult containing all parsed entries and metadata.
    """
    entries  = __parse_entries(response)
    metadata = __parse_metadata(response)

    return GlossaryParseResult(
        entries=entries,
        metadata=metadata,
    )


def __parse_entries(response: HtmlResponse) -> tuple[GlossaryEntry, ...]:
    """
    Parses the <dl> definition list into a tuple of GlossaryEntry objects.
    Each <dt> is a term, and each <dd> is its definition.
    """
    soup = make_soup(response)
    # Pair up each <dt> (term) with its corresponding <dd> (definition)
    raw_entries = zip(soup("dt"), soup("dd"))

    return tuple(
        GlossaryEntry(
            phrase=normalize_nonempty(phrase.text),  # Clean and normalize the term
            definition=Sentence(defn.text),          # Wrap the definition as a Sentence
        )
        for phrase, defn in raw_entries
    )


def __parse_metadata(response: HtmlResponse) -> Metadata:
    """
    Returns static metadata about the glossary source.
    This is mostly hardcoded, as the source is known and stable.
    """
    return Metadata(
            dcterms_title=String("Glossary of Legal Terms"),
            dcterms_language="en",
            dcterms_coverage="USA",
            # Info about original source
            dcterms_source=String("https://www.uscourts.gov/glossary"),
            publiclaw_sourceModified="unknown",
            publiclaw_sourceCreator=String("United States Courts"),
            dcterms_subject=(
                Subject(
                    uri=LoCSubject("sh85033575"),
                    rdfs_label=String("Courts--United States"),
                ),
                Subject(
                    uri=URL("https://www.wikidata.org/wiki/Q194907"),
                    rdfs_label=String("United States federal courts"),
                ),
            ),
        )
