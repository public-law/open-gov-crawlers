from scrapy.http.response.html import HtmlResponse

from ...metadata import Metadata, Subject
from ...models.glossary import GlossaryEntry, GlossaryParseResult
from ...text import URL, LoCSubject
from ...text import NonemptyString as String
from ...text import (Sentence, make_soup,
                     normalize_nonempty)


def parse_glossary(response: HtmlResponse) -> GlossaryParseResult:
    entries  = __parse_entries(response)
    metadata = __parse_metadata(response)

    return GlossaryParseResult(
        entries=entries,
        metadata=metadata,
    )


def __parse_entries(response: HtmlResponse) -> tuple[GlossaryEntry, ...]:
    soup = make_soup(response)
    raw_entries = zip(soup("dt"), soup("dd"))

    return tuple(
        GlossaryEntry(
            phrase=normalize_nonempty(phrase.text),
            definition=Sentence(defn.text),
        )
        for phrase, defn in raw_entries
    )


def __parse_metadata(response: HtmlResponse) -> Metadata:
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
