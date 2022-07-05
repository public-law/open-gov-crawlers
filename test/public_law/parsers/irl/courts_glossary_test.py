# pyright: reportUntypedFunctionDecorator=false
# pyright: reportOptionalMemberAccess=false

from more_itertools import first, last


from scrapy.http.response.html import HtmlResponse
from pytest import fixture, mark

from public_law.dates import today
from public_law.models.glossary import GlossaryParseResult
from public_law.parsers.irl.courts_glossary import parse_glossary


def parsed_fixture(filename: str, url: str) -> GlossaryParseResult:
    with open(f"test/fixtures/irl/{filename}", encoding="utf8") as f:
        html = HtmlResponse(
            url=url,
            body=f.read(),
            encoding="UTF-8",
        )

    return parse_glossary(html)


@fixture
def parsed_glossary() -> GlossaryParseResult:
    return parsed_fixture(
        filename="ie.courts-glossary.html",
        url="https://www.courts.ie/glossary",
    )


def test_gets_the_name(parsed_glossary: GlossaryParseResult):
    assert parsed_glossary.metadata.dcterms_title == "Glossary"


def test_gets_the_url(parsed_glossary: GlossaryParseResult):
    assert parsed_glossary.metadata.dcterms_source == "https://www.courts.ie/glossary"


def test_gets_the_author(parsed_glossary: GlossaryParseResult):
    assert parsed_glossary.metadata.dcterms_creator == "https://public.law"


def test_gets_coverage(parsed_glossary: GlossaryParseResult):
    assert parsed_glossary.metadata.dcterms_coverage == "IRL"


def test_gets_the_source_modified_date(parsed_glossary: GlossaryParseResult):
    assert parsed_glossary.metadata.publiclaw_sourceModified == "unknown"


def test_gets_the_scrape_date(parsed_glossary: GlossaryParseResult):
    assert parsed_glossary.metadata.dcterms_modified == today()


@mark.skip
def test_phrase(parsed_glossary: GlossaryParseResult):
    assert first(parsed_glossary.entries).phrase == "acquit"


@mark.skip
def test_definition(parsed_glossary: GlossaryParseResult):
    assert (
        first(parsed_glossary.entries).definition
        == "To decide officially in court that a person is not guilty."
    )


@mark.skip
def test_gets_proper_number_of_entries(parsed_glossary: GlossaryParseResult):
    assert len(tuple(parsed_glossary.entries)) == 154


@mark.skip
def test_gets_the_last_entry(parsed_glossary: GlossaryParseResult):
    last_entry = last(parsed_glossary.entries)

    assert last_entry.phrase == "Youth Court"
    assert last_entry.definition == (
        "The Youth Court has jurisdiction to deal with "
        "young people charged with criminal offences."
    )
