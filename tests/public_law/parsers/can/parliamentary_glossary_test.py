# pyright: reportSelfClsParameterName=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownParameterType=false
# pyright: reportMissingParameterType=false
# pyright: reportUnknownVariableType=false


from more_itertools import first, last, nth
from datetime import date

import pytest
from scrapy.http.response.html import HtmlResponse

from public_law.dates import today
from public_law.metadata import Subject
from public_law.models.glossary import glossary_fixture
# The System Under Test
from public_law.parsers.can.parliamentary_glossary import parse_glossary
from public_law.text import URL, NonemptyString

ORIG_URL = URL("https://www.ourcommons.ca/procedure/glossary/index-e.html")
GLOSSARY = glossary_fixture(
    "can/procedure-glossary.html", ORIG_URL, parse_glossary)
METADATA = GLOSSARY.metadata
ENTRIES = tuple(GLOSSARY.entries)


class TestTheMetadata:
    def test_the_name(_):
        assert (
            METADATA.dcterms_title
            == "Glossary of Parliamentary Procedure"
        )

    def test_the_url(_):
        assert METADATA.dcterms_source == ORIG_URL

    def test_the_author(_):
        assert METADATA.dcterms_creator == "https://public.law"

    def test_coverage(_):
        assert METADATA.dcterms_coverage == "CAN"

    def test_creator(_):
        assert METADATA.publiclaw_sourceCreator == "House of Commons"

    def test_the_source_modified_date(_):
        assert METADATA.publiclaw_sourceModified == "unknown"

    def test_the_scrape_date(_):
        assert METADATA.dcterms_modified == today()

    def test_subjects(_):
        assert METADATA.dcterms_subject == (
            Subject(
                uri=URL("http://id.loc.gov/authorities/subjects/sh85075807"),
                rdfs_label=NonemptyString("Legislative bodies"),
            ),
            Subject(
                uri=URL("https://www.wikidata.org/wiki/Q35749"),
                rdfs_label=NonemptyString("Parliament"),
            ),
        )


class TestTheEntries:
    def test_phrase(_):
        assert first(ENTRIES).phrase == "abstention"

    def test_definition(_):
        assert first(ENTRIES).definition == (
            "The act of refraining from voting either for or against a motion. Members are not obliged to vote, and the records of the House take no official notice of an abstention; a list of paired members is appended, if necessary, to every division list in the Journals and Debates. "
        )

    def test_proper_number_of_entries(_):
        assert len(tuple(ENTRIES)) == 526

    def test_the_last_entry(_):
        last_entry = last(ENTRIES)

        assert last_entry.phrase == "Written question"
        assert last_entry.definition == (
            "See: Questions on the Order Paper"
        )

    def test_the_third_to_the_last_entry(_):
        entry = nth(ENTRIES, 523)

        assert entry
        assert entry.phrase == "Witness"


@pytest.fixture
def glossary_response():
    """Create a mock response with the glossary HTML content."""
    with open("tests/fixtures/can/procedure-glossary.html", "r") as f:
        html_content = f.read()

    return HtmlResponse(
        url="https://www.ourcommons.ca/procedure/glossary/index-e.html",
        body=html_content.encode(),
        encoding="utf-8",
    )


@pytest.fixture
def parsed_glossary(glossary_response):
    """Parse the glossary and return the result."""
    return parse_glossary(glossary_response)


def test_glossary_has_entries(parsed_glossary):
    """Test that the glossary has entries."""
    assert len(tuple(parsed_glossary.entries)) > 0


@pytest.mark.parametrize("field,expected", [
    ("dcterms_title", "Glossary of Parliamentary Terms"),
    ("dcterms_language", "en"),
    ("dcterms_coverage", "CAN"),
    ("publiclaw_sourceCreator", "House of Commons of Canada"),
    ("publiclaw_sourceModified", "unknown"),
])
def test_glossary_metadata(parsed_glossary, field, expected):
    """Test individual metadata fields."""
    assert getattr(parsed_glossary.metadata, field) == expected


def test_first_glossary_entry(parsed_glossary):
    """Test the first glossary entry."""
    entries = tuple(parsed_glossary.entries)
    first_entry = entries[0]

    assert first_entry.phrase == "Abstention"
    assert first_entry.definition == "The practice of refraining from voting on a motion or bill."


def test_last_glossary_entry(parsed_glossary):
    """Test the last glossary entry."""
    entries = tuple(parsed_glossary.entries)
    last_entry = entries[-1]

    assert last_entry.phrase == "Whip"
    assert last_entry.definition == "A Member of Parliament who is responsible for ensuring party discipline and attendance in the House of Commons."
