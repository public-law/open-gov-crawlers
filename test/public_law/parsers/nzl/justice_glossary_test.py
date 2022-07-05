# pyright: reportUntypedFunctionDecorator=false
# pyright: reportOptionalMemberAccess=false

from functools import cache
from more_itertools import first, last, nth


from scrapy.http.response.html import HtmlResponse
from pytest import fixture, mark

from public_law.dates import today
from public_law.models.glossary import GlossaryParseResult
from public_law.parsers.nzl.justice_glossary import parse_glossary


def parsed_fixture(filename: str, url: str) -> GlossaryParseResult:
    with open(f"test/fixtures/nzl/{filename}", encoding="utf8") as f:
        html = HtmlResponse(
            url=url,
            body=f.read(),
            encoding="UTF-8",
        )

    return parse_glossary(html)


@fixture
@cache
def parsed_glossary() -> GlossaryParseResult:
    return parsed_fixture(
        filename="nz.govt.justice-glossary.html",
        url="https://www.justice.govt.nz/about/glossary/",
    )


def test_gets_the_name(parsed_glossary: GlossaryParseResult):
    assert parsed_glossary.metadata.dcterms_title == "Glossary"


def test_gets_the_url(parsed_glossary: GlossaryParseResult):
    assert (
        parsed_glossary.metadata.dcterms_source
        == "https://www.justice.govt.nz/about/glossary/"
    )


def test_gets_the_author(parsed_glossary: GlossaryParseResult):
    assert parsed_glossary.metadata.dcterms_creator == "https://public.law"


def test_gets_coverage(parsed_glossary: GlossaryParseResult):
    assert parsed_glossary.metadata.dcterms_coverage == "NZL"


def test_gets_the_source_modified_date(parsed_glossary: GlossaryParseResult):
    assert parsed_glossary.metadata.publiclaw_sourceModified == "unknown"


def test_gets_the_scrape_date(parsed_glossary: GlossaryParseResult):
    assert parsed_glossary.metadata.dcterms_modified == today()


def test_phrase(parsed_glossary: GlossaryParseResult):
    assert first(parsed_glossary.entries).phrase == "acquit"


@mark.skip(reason="Not implemented yet")
def test_definition(parsed_glossary: GlossaryParseResult):
    assert (
        nth(parsed_glossary.entries, 2).definition
        == "A judge in the full-time service of the court. Compare to senior judge."
    )


@mark.skip(reason="Not implemented yet")
def test_gets_proper_number_of_entries(parsed_glossary: GlossaryParseResult):
    assert len(tuple(parsed_glossary.entries)) == 237


@mark.skip(reason="Not implemented yet")
def test_gets_the_last_entry(parsed_glossary: GlossaryParseResult):
    last_entry = last(parsed_glossary.entries)

    assert last_entry.phrase == "Writ of certiorari"
    assert last_entry.definition == (
        "An order issued by the U.S. Supreme Court directing "
        "the lower court to transmit records for a case which "
        "it will hear on appeal."
    )
