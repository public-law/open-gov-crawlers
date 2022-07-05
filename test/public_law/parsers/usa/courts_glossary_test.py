from datetime import date
from scrapy.http.response.html import HtmlResponse
from pytest import fixture, mark

from public_law.dates import today
from public_law.models.glossary import GlossaryParseResult
from public_law.parsers.us.courts_glossary import parse_glossary


def parsed_fixture(filename: str, url: str) -> GlossaryParseResult:
    with open(f"test/fixtures/usa/{filename}", encoding="utf8") as f:
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


@mark.skip(reason="Not implemented yet")
def test_gets_the_scrape_date(parsed_glossary: GlossaryParseResult):
    assert parsed_glossary.metadata.dcterms_modified == today()


@mark.skip(reason="Not implemented yet")
def test_phrase(parsed_glossary: GlossaryParseResult):
    assert parsed_glossary.entries[0].phrase == "Alienated Parent"


@mark.skip(reason="Not implemented yet")
def test_gets_proper_number_of_entries(parsed_glossary: GlossaryParseResult):
    assert len(parsed_glossary.entries) == 127


@mark.skip(reason="Not implemented yet")
def test_gets_a_term_case_1(parsed_glossary: GlossaryParseResult):
    entry = parsed_glossary.entries[2]
    assert entry.phrase == "Adjournment"
    assert entry.definition == "Postponement of a court hearing to another date."
