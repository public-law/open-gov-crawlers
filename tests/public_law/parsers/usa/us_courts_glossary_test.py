# pyright: reportUntypedFunctionDecorator=false


from scrapy.http.response.html import HtmlResponse
from pytest import fixture
from more_itertools import first, last

from public_law.dates import today
from public_law.models.glossary import GlossaryParseResult
from public_law.parsers.usa.us_courts_glossary import parse_glossary


def parsed_fixture(filename: str, url: str) -> GlossaryParseResult:
    with open(f"tests/fixtures/usa/{filename}", encoding="utf8") as f:
        html = HtmlResponse(
            url=url,
            body=f.read(),
            encoding="UTF-8",
        )

    return parse_glossary(html)


@fixture
def parsed_glossary() -> GlossaryParseResult:
    return parsed_fixture(
        filename="gov.uscourts-glossary.html", url="https://www.uscourts.gov/glossary"
    )


def test_gets_the_name(parsed_glossary: GlossaryParseResult):
    assert parsed_glossary.metadata.dcterms_title == "Glossary of Legal Terms"


def test_gets_the_url(parsed_glossary: GlossaryParseResult):
    assert (
        parsed_glossary.metadata.dcterms_source == "https://www.uscourts.gov/glossary"
    )


def test_gets_the_author(parsed_glossary: GlossaryParseResult):
    assert parsed_glossary.metadata.dcterms_creator == "https://public.law"


def test_gets_coverage(parsed_glossary: GlossaryParseResult):
    assert parsed_glossary.metadata.dcterms_coverage == "USA"


def test_gets_the_source_modified_date(parsed_glossary: GlossaryParseResult):
    assert parsed_glossary.metadata.publiclaw_sourceModified == "unknown"


def test_gets_the_scrape_date(parsed_glossary: GlossaryParseResult):
    assert parsed_glossary.metadata.dcterms_modified == today()


def test_phrase(parsed_glossary: GlossaryParseResult):
    assert first(parsed_glossary.entries).phrase == "Acquittal"


def test_definition(parsed_glossary: GlossaryParseResult):
    assert first(parsed_glossary.entries).definition == (
        "A jury verdict that a criminal defendant is not guilty, "
        "or the finding of a judge that the evidence is insufficient "
        "to support a conviction."
    )


def test_gets_proper_number_of_entries(parsed_glossary: GlossaryParseResult):
    assert len(tuple(parsed_glossary.entries)) == 237


def test_gets_the_last_entry(parsed_glossary: GlossaryParseResult):
    last_entry = last(parsed_glossary.entries)

    assert last_entry.phrase == "Writ of certiorari"
    assert last_entry.definition == (
        "An order issued by the U.S. Supreme Court directing "
        "the lower court to transmit records for a case which "
        "it will hear on appeal."
    )


def test_reading_ease(parsed_glossary: GlossaryParseResult):
    assert parsed_glossary.metadata.publiclaw_readingEase == "Fairly difficult"
