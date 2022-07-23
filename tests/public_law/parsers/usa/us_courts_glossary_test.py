from scrapy.http.response.html import HtmlResponse
from more_itertools import first, last

from public_law.dates import today
from public_law.metadata import Subject
from public_law.models.glossary import GlossaryParseResult
from public_law.parsers.usa.us_courts_glossary import parse_glossary
from public_law.text import URL, NonemptyString


def parsed_fixture(filename: str, url: str) -> GlossaryParseResult:
    with open(f"tests/fixtures/usa/{filename}", encoding="utf8") as f:
        html = HtmlResponse(
            url=url,
            body=f.read(),
            encoding="UTF-8",
        )

    return parse_glossary(html)


GLOSSARY_FIXTURE = parsed_fixture(
    filename="gov.uscourts-glossary.html", url="https://www.uscourts.gov/glossary"
)


def test_the_name():
    assert GLOSSARY_FIXTURE.metadata.dcterms_title == "Glossary of Legal Terms"


def test_the_url():
    assert (
        GLOSSARY_FIXTURE.metadata.dcterms_source == "https://www.uscourts.gov/glossary"
    )


def test_the_author():
    assert GLOSSARY_FIXTURE.metadata.dcterms_creator == "https://public.law"


def test_coverage():
    assert GLOSSARY_FIXTURE.metadata.dcterms_coverage == "USA"


def test_the_source_modified_date():
    assert GLOSSARY_FIXTURE.metadata.publiclaw_sourceModified == "unknown"


def test_the_scrape_date():
    assert GLOSSARY_FIXTURE.metadata.dcterms_modified == today()


def test_phrase():
    assert first(GLOSSARY_FIXTURE.entries).phrase == "Acquittal"


def test_definition():
    assert first(GLOSSARY_FIXTURE.entries).definition == (
        "A jury verdict that a criminal defendant is not guilty, "
        "or the finding of a judge that the evidence is insufficient "
        "to support a conviction."
    )


def test_proper_number_of_entries():
    assert len(tuple(GLOSSARY_FIXTURE.entries)) == 237


def test_the_last_entry():
    last_entry = last(GLOSSARY_FIXTURE.entries)

    assert last_entry.phrase == "Writ of certiorari"
    assert last_entry.definition == (
        "An order issued by the U.S. Supreme Court directing "
        "the lower court to transmit records for a case which "
        "it will hear on appeal."
    )


def test_reading_ease():
    assert GLOSSARY_FIXTURE.metadata.publiclaw_readingEase == "Fairly difficult"


def test_subjects():
    assert GLOSSARY_FIXTURE.metadata.dcterms_subject == (
        Subject(
            uri=URL("https://id.loc.gov/authorities/subjects/sh85033575.html"),
            rdfs_label=NonemptyString("Courts--United States"),
        ),
        Subject(
            uri=URL("https://www.wikidata.org/wiki/Q194907"),
            rdfs_label=NonemptyString("United States federal courts"),
        ),
    )
