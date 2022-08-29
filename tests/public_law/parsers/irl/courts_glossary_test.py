# pyright: reportUntypedFunctionDecorator=false
# pyright: reportOptionalMemberAccess=false
# pyright: reportUnusedImport=false

from more_itertools import first, last

from scrapy.http.response.html import HtmlResponse
from pytest import fixture, mark

from public_law.dates import today
from public_law.metadata import Subject
from public_law.models.glossary import GlossaryParseResult, glossary_fixture
from public_law.parsers.irl.courts_glossary import parse_glossary
from public_law.text import URL, NonemptyString


@fixture
def parsed_glossary() -> GlossaryParseResult:
    return glossary_fixture(
        path="irl/ie.courts-glossary.html",
        url="https://www.courts.ie/glossary",
        parse_func=parse_glossary,
    )


def test_gets_the_name(parsed_glossary: GlossaryParseResult):
    assert parsed_glossary.metadata.dcterms_title == "Glossary of Legal Terms"


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


def test_phrase(parsed_glossary: GlossaryParseResult):
    assert first(parsed_glossary.entries).phrase == "Affidavit"


def test_definition(parsed_glossary: GlossaryParseResult):
    assert (
        first(parsed_glossary.entries).definition == "A written statement made on oath."
    )


def test_gets_proper_number_of_entries(parsed_glossary: GlossaryParseResult):
    assert len(tuple(parsed_glossary.entries)) == 43


def test_gets_the_last_entry(parsed_glossary: GlossaryParseResult):
    last_entry = last(parsed_glossary.entries)

    assert last_entry.phrase == "Supervision order"
    assert last_entry.definition == (
        "An order allowing Tusla to monitor a child considered to be at risk. "
        "The child is not removed from his or her home environment. A supervision "
        "order is for a fixed period of time not longer than 12 months initially."
    )


def test_subjects(parsed_glossary: GlossaryParseResult):
    assert parsed_glossary.metadata.dcterms_subject == (
        Subject(
            uri=URL("http://id.loc.gov/authorities/subjects/sh85033571"),
            rdfs_label=NonemptyString("Courts"),
        ),
        Subject(
            uri=URL("https://www.wikidata.org/wiki/Q41487"),
            rdfs_label=NonemptyString("Court"),
        ),
    )
