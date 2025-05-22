# pyright: reportArgumentType=false

from pathlib import Path

import pytest
from scrapy.http.response.html import HtmlResponse

from public_law.parsers.can.patents_glossary import parse_glossary
from public_law.models.glossary import GlossaryEntry, GlossaryParseResult
from public_law.text import NonemptyString as String
from public_law.text import Sentence


@pytest.fixture
def glossary_response() -> HtmlResponse:
    """Create a Scrapy response object from the test fixture."""
    fixture_path = Path(__file__).parent.parent / \
        "fixtures" / "can" / "patents-glossary.html"
    with open(fixture_path, "rb") as f:
        html_content = f.read()

    return HtmlResponse(
        url="https://ised-isde.canada.ca/site/canadian-intellectual-property-office/en/patents/glossary",
        body=html_content,
        encoding="utf-8",
    )


def test_parse_glossary_returns_glossary_parse_result(glossary_response: HtmlResponse) -> None:
    """Test that parse_glossary returns a GlossaryParseResult."""
    result = parse_glossary(glossary_response)
    assert isinstance(result, GlossaryParseResult)


def test_parse_glossary_metadata(glossary_response: HtmlResponse) -> None:
    """Test that the metadata is correctly parsed."""
    result = parse_glossary(glossary_response)

    assert result.metadata.dcterms_title == String("Patents Glossary")
    assert result.metadata.dcterms_language == "en"
    assert result.metadata.dcterms_coverage == "CAN"
    assert result.metadata.publiclaw_sourceCreator == String(
        "Canadian Intellectual Property Office")


def test_parse_glossary_has_entries(glossary_response: HtmlResponse) -> None:
    """Test that the glossary has entries."""
    result = parse_glossary(glossary_response)
    entries = list(result.entries)
    assert len(entries) > 0


def test_parse_glossary_entry_types(glossary_response: HtmlResponse) -> None:
    """Test that all entries have the correct types and non-empty content."""
    result = parse_glossary(glossary_response)

    for entry in result.entries:
        assert isinstance(entry, GlossaryEntry)
        assert isinstance(entry.phrase, String)
        assert isinstance(entry.definition, Sentence)
        assert len(entry.phrase) > 0
        assert len(entry.definition) > 0


def test_abstract_entry(glossary_response: HtmlResponse) -> None:
    """Test that the Abstract entry is correctly parsed."""
    result = parse_glossary(glossary_response)
    entries_dict = {entry.phrase: entry.definition for entry in result.entries}

    assert String("Abstract") in entries_dict
    assert entries_dict[String("Abstract")] == Sentence(
        "A brief summary of your invention.")


def test_claims_entry(glossary_response: HtmlResponse) -> None:
    """Test that the Claims entry is correctly parsed."""
    result = parse_glossary(glossary_response)
    entries_dict = {entry.phrase: entry.definition for entry in result.entries}

    assert String("Claims") in entries_dict
    assert entries_dict[String("Claims")] == Sentence(
        "The parts of a patent that define the boundaries of patent protection."
    )


def test_patent_entry(glossary_response: HtmlResponse) -> None:
    """Test that the Patent entry is correctly parsed."""
    result = parse_glossary(glossary_response)
    entries_dict = {entry.phrase: entry.definition for entry in result.entries}

    assert String("Patent") in entries_dict
    assert entries_dict[String("Patent")] == Sentence(
        "A government grant giving the right to exclude others from making, using, or selling an invention."
    )


def test_first_entry(glossary_response: HtmlResponse) -> None:
    """Test that the first entry is 'Abstract'."""
    result = parse_glossary(glossary_response)
    entries = list(result.entries)

    assert entries[0].phrase == String("Abstract")
    assert entries[0].definition == Sentence(
        "A brief summary of your invention.")


def test_last_entry(glossary_response: HtmlResponse) -> None:
    """Test that the last entry is 'WIPO'."""
    result = parse_glossary(glossary_response)
    entries = list(result.entries)

    assert entries[-1].phrase == String("WIPO")
    assert entries[-1].definition == Sentence(
        "World Intellectual Property Organization")
