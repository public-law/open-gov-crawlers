# pyright: reportUntypedFunctionDecorator=false
# pyright: reportOptionalMemberAccess=false
# pyright: reportUnusedImport=false

from more_itertools import first, last

from scrapy.http.response.html import HtmlResponse
from pytest import fixture, mark

from public_law.dates import today
from public_law.metadata import Subject
from public_law.models.glossary import GlossaryParseResult
from public_law.text import URL, NonemptyString

from public_law.parsers.usa.uscis_glossary import parse_glossary



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
        filename="uscis-glossary.html",
        url="https://www.uscis.gov/tools/glossary",
    )

@mark.skip
def test_gets_the_name(parsed_glossary: GlossaryParseResult):
    assert parsed_glossary.metadata.dcterms_title == "USCIS Glossary"


@mark.skip
def test_gets_the_url(parsed_glossary: GlossaryParseResult):
    assert parsed_glossary.metadata.dcterms_source == "https://www.uscis.gov/tools/glossary"


@mark.skip
def test_gets_the_author(parsed_glossary: GlossaryParseResult):
    assert parsed_glossary.metadata.dcterms_creator == "https://public.law"


@mark.skip
def test_gets_coverage(parsed_glossary: GlossaryParseResult):
    assert parsed_glossary.metadata.dcterms_coverage == "USA"


@mark.skip
def test_gets_the_source_modified_date(parsed_glossary: GlossaryParseResult):
    assert parsed_glossary.metadata.publiclaw_sourceModified == "unknown"


@mark.skip
def test_gets_the_scrape_date(parsed_glossary: GlossaryParseResult):
    assert parsed_glossary.metadata.dcterms_modified == today()


@mark.skip
def test_phrase(parsed_glossary: GlossaryParseResult):
    assert first(parsed_glossary.entries).phrase == "Alien Registration Number"


@mark.skip
def test_definition(parsed_glossary: GlossaryParseResult):
    assert (
        first(parsed_glossary.entries).definition == "A unique seven-, eight- or nine-digit number assigned to a noncitizen by the Department of Homeland Security. Also see USCIS Number."
    )


@mark.skip
def test_gets_proper_number_of_entries(parsed_glossary: GlossaryParseResult):
    assert len(tuple(parsed_glossary.entries)) == 43


@mark.skip
def test_gets_the_last_entry(parsed_glossary: GlossaryParseResult):
    last_entry = last(parsed_glossary.entries)

    assert last_entry.phrase == "Withdrawal"
    assert last_entry.definition == (
        'This is an arriving noncitizen’s voluntary retraction of an application '
        'for admission to the United States in lieu of a removal hearing before an '
        'immigration judge or an expedited removal.'
    )


@mark.skip
def test_subjects(parsed_glossary: GlossaryParseResult):
    assert parsed_glossary.metadata.dcterms_subject == (
        Subject(
            uri=URL("http://id.loc.gov/authorities/subjects/sh85042790"),
            rdfs_label=NonemptyString("Emigration and immigration law"),
        ),
        Subject(
            uri=URL("https://www.wikidata.org/wiki/Q231147"),
            rdfs_label=NonemptyString("immigration law"),
        ),
    )
