from datetime import date

import pytest
from scrapy.http.response.html import HtmlResponse

from public_law.parsers.gbr.fpr_glossary import parse_glossary


def test_parse_glossary():
    """
    Test that the parser correctly extracts glossary entries from the HTML.
    """
    # Load the test HTML file
    with open("tests/fixtures/gbr/fpr_glossary.html", "r") as f:
        html_content = f.read()

    # Create a mock response
    response = HtmlResponse(
        url="https://www.justice.gov.uk/courts/procedure-rules/family/backmatter/fpr_glossary",
        body=html_content.encode(),
        encoding="utf-8",
    )

    # Parse the response
    result = parse_glossary(response)

    # Check metadata
    assert result.metadata.dcterms_title == "Family Procedure Rules Glossary"
    assert result.metadata.dcterms_language == "en"
    assert result.metadata.dcterms_coverage == "GBR"
    assert result.metadata.publiclaw_sourceCreator == "Ministry of Justice"
    assert result.metadata.publiclaw_sourceModified == date(2017, 1, 30)

    # Check entries
    entries = tuple(result.entries)  # Convert to tuple for indexing
    assert len(entries) > 0

    # Check first entry
    first_entry = entries[0]
    assert first_entry.phrase == "Affidavit"
    assert first_entry.definition == "A written, sworn, statement of evidence."

    # Check last entry
    last_entry = entries[-1]
    assert last_entry.phrase == "Without prejudice"
    assert last_entry.definition == "Negotiations with a view to settlement are usually conducted \"without prejudice\" which means that the circumstances in which the content of those negotiations may be revealed to the court are very restricted."
