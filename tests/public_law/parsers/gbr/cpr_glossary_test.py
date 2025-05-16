from datetime import date

import pytest
from scrapy.http.response.html import HtmlResponse

from public_law.parsers.gbr.cpr_glossary import parse_glossary


def test_parse_glossary():
    """
    Test that the parser correctly extracts glossary entries from the HTML table.
    """
    # Load the test HTML file
    with open("tests/fixtures/gbr/cpr_glossary.html", "r") as f:
        html_content = f.read()

    # Create a mock response
    response = HtmlResponse(
        url="https://www.legislation.gov.uk/uksi/2020/759/part/Glossary?view=plain",
        body=html_content.encode(),
        encoding="utf-8",
    )

    # Parse the response
    result = parse_glossary(response)

    # Check metadata
    assert result.metadata.dcterms_title == "Criminal Procedure Rules Glossary"
    assert result.metadata.dcterms_language == "en"
    assert result.metadata.dcterms_coverage == "GBR"
    assert result.metadata.publiclaw_sourceCreator == "Ministry of Justice"
    assert result.metadata.publiclaw_sourceModified == date(2020, 10, 5)

    # Check entries
    entries = tuple(result.entries)  # Convert to tuple for indexing
    assert len(entries) > 0

    # Check first entry
    first_entry = entries[0]
    assert first_entry.phrase == "account monitoring order"
    assert first_entry.definition == "an order requiring certain types of financial institution to provide certain information held by them relating to a customer for the purposes of an investigation;."

    # Check last entry
    last_entry = entries[-1]
    assert last_entry.phrase == "youth court"
    assert last_entry.definition == "a magistrates' court exercising jurisdiction over offences committed by, and other matters related to, children and young persons."
