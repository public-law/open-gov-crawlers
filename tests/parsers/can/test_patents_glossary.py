# pyright: reportArgumentType=false

from pathlib import Path

import pytest
from scrapy.http.response.html import HtmlResponse

from public_law.parsers.can.patents_glossary import parse_glossary
from public_law.models.glossary import GlossaryEntry, GlossaryParseResult
from public_law.text import NonemptyString as String
from public_law.text import Sentence


def test_parse_glossary():
    # Load the test fixture
    fixture_path = Path(__file__).parent.parent / \
        "fixtures" / "can" / "patents-glossary.html"
    with open(fixture_path, "rb") as f:
        html_content = f.read()

    # Create a Scrapy response object
    response = HtmlResponse(
        url="https://ised-isde.canada.ca/site/canadian-intellectual-property-office/en/patents/glossary",
        body=html_content,
        encoding="utf-8",
    )

    # Parse the glossary
    result = parse_glossary(response)
    entries = list(result.entries)

    # Verify the result is a GlossaryParseResult
    assert isinstance(result, GlossaryParseResult)

    # Verify metadata
    assert result.metadata.dcterms_title == String("Patents Glossary")
    assert result.metadata.dcterms_language == "en"
    assert result.metadata.dcterms_coverage == "CAN"
    assert result.metadata.publiclaw_sourceCreator == String(
        "Canadian Intellectual Property Office")

    # Verify we got the expected number of entries
    assert len(entries) > 0

    # Verify some specific entries
    entries_dict = {entry.phrase: entry.definition for entry in entries}

    # Test a few key entries
    assert String("Abstract") in entries_dict
    assert entries_dict[String("Abstract")] == Sentence(
        "A brief summary of your invention.")

    assert String("Claims") in entries_dict
    assert entries_dict[String("Claims")] == Sentence(
        "The parts of a patent that define the boundaries of patent protection.")

    assert String("Patent") in entries_dict
    assert entries_dict[String("Patent")] == Sentence(
        "A government grant giving the right to exclude others from making, using, or selling an invention.")

    # Verify all entries have non-empty phrases and definitions
    for entry in entries:
        assert isinstance(entry, GlossaryEntry)
        assert isinstance(entry.phrase, String)
        assert isinstance(entry.definition, Sentence)
        assert len(entry.phrase) > 0
        assert len(entry.definition) > 0

    # The first entry should be "Abstract"
    assert entries[0].phrase == String("Abstract")
    assert entries[0].definition == Sentence(
        "A brief summary of your invention.")

    # The last entry should be "WIPO"
    assert entries[-1].phrase == String("WIPO")
    assert entries[-1].definition == Sentence(
        "World Intellectual Property Organization")
