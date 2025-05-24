from pathlib import Path

import pytest
from scrapy.http.response.html import HtmlResponse

from public_law.parsers.can.patents_glossary import parse_glossary
from public_law.spiders.can.patents_glossary import URL
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
        url=URL,
        body=html_content,
        encoding="utf-8",
    )


@pytest.fixture
def parsed_glossary(glossary_response: HtmlResponse) -> GlossaryParseResult:
    """Parse the glossary response into a GlossaryParseResult."""
    return parse_glossary(glossary_response)


def test_parse_glossary_returns_glossary_parse_result(parsed_glossary: GlossaryParseResult) -> None:
    """Test that parse_glossary returns a GlossaryParseResult."""
    assert isinstance(parsed_glossary, GlossaryParseResult)


def test_parse_glossary_metadata(parsed_glossary: GlossaryParseResult) -> None:
    """Test that the metadata is correctly parsed."""
    assert parsed_glossary.metadata.dcterms_title == String(
        "Canadian Patent Glossary")
    assert parsed_glossary.metadata.dcterms_language == "en"
    assert parsed_glossary.metadata.dcterms_coverage == "CAN"
    assert parsed_glossary.metadata.publiclaw_sourceCreator == String(
        "Canadian Intellectual Property Office")


def test_parse_glossary_has_entries(parsed_glossary: GlossaryParseResult) -> None:
    """Test that the glossary has entries."""
    entries = list(parsed_glossary.entries)
    assert len(entries) > 0


def test_parse_glossary_entry_types(parsed_glossary: GlossaryParseResult) -> None:
    """Test that all entries have the correct types and non-empty content."""
    for entry in parsed_glossary.entries:
        assert isinstance(entry, GlossaryEntry)
        assert isinstance(entry.phrase, String)
        assert isinstance(entry.definition, Sentence)
        assert len(entry.phrase) > 0
        assert len(entry.definition) > 0


def test_abstract_entry(parsed_glossary: GlossaryParseResult) -> None:
    """Test that the Abstract entry is correctly parsed."""
    entries_dict = {
        entry.phrase: entry.definition for entry in parsed_glossary.entries}

    assert String("Abstract") in entries_dict
    assert entries_dict[String("Abstract")] == Sentence(
        "A brief summary of your invention.")


def test_claims_entry(parsed_glossary: GlossaryParseResult) -> None:
    """Test that the Claims entry is correctly parsed."""
    entries_dict = {
        entry.phrase: entry.definition for entry in parsed_glossary.entries}

    assert String("Claims") in entries_dict
    assert entries_dict[String("Claims")] == Sentence(
        "The parts of a patent that define the boundaries of patent protection."
    )


def test_patent_entry(parsed_glossary: GlossaryParseResult) -> None:
    """Test that the Patent entry is correctly parsed."""
    entries_dict = {
        entry.phrase: entry.definition for entry in parsed_glossary.entries}

    assert String("Patent") in entries_dict
    assert entries_dict[String("Patent")] == Sentence(
        "A government grant giving the right to exclude others from making, using, or selling an invention."
    )


def test_first_entry(parsed_glossary: GlossaryParseResult) -> None:
    """Test that the first entry is 'Abstract'."""
    entries = list(parsed_glossary.entries)

    assert entries[0].phrase == String("Abstract")
    assert entries[0].definition == Sentence(
        "A brief summary of your invention.")


def test_last_entry(parsed_glossary: GlossaryParseResult) -> None:
    """Test that the last entry is 'WIPO'."""
    entries = list(parsed_glossary.entries)

    assert entries[-1].phrase == String("WIPO")
    assert entries[-1].definition == Sentence(
        "World Intellectual Property Organization.")


def test_no_date_modified_entry_anywhere(parsed_glossary: GlossaryParseResult) -> None:
    """Test that 'Date modified:' is not present as any glossary entry."""
    phrases = [str(entry.phrase) for entry in parsed_glossary.entries]
    assert "Date modified:" not in phrases, (
        "'Date modified:' should not be present in any glossary entry"
    )


def test_parse_real_glossary_handles_date_modified() -> None:
    """Test that parsing a real glossary response handles the Date modified entry correctly."""
    # Create a response with the actual HTML structure
    html_content = """
    <dl>
        <dt><strong>Abstract</strong></dt>
        <dd>A brief summary of your invention.</dd>
        <dt>Date modified:</dt>
        <dd>2024-03-21</dd>
        <dt><strong>Claims</strong></dt>
        <dd>The parts of a patent that define the boundaries of patent protection.</dd>
    </dl>
    """

    response = HtmlResponse(
        url=URL,
        body=html_content.encode('utf-8'),
        encoding="utf-8",
    )

    result = parse_glossary(response)

    # Verify that Date modified is not included in the entries
    phrases = [str(entry.phrase) for entry in result.entries]
    assert "Date modified:" not in phrases

    # Verify that we still get the other entries
    assert String("Abstract") in phrases
    assert String("Claims") in phrases

    # Verify the total number of entries is correct (should be 2, not 3)
    assert len(result.entries) == 2


def test_date_modified_without_strong_tag() -> None:
    """Test that Date modified is skipped even when it appears without a strong tag.
    This matches the production HTML structure where Date modified appears as plain text."""
    html_content = """
    <dl>
        <dt>Date modified:</dt>
        <dd>2021-06-28</dd>
    </dl>
    """

    response = HtmlResponse(
        url=URL,
        body=html_content.encode('utf-8'),
        encoding="utf-8",
    )

    result = parse_glossary(response)

    # The result should have no entries since Date modified should be skipped
    assert len(result.entries) == 0, (
        "Parser should skip 'Date modified:' entry even when it appears without a strong tag"
    )
