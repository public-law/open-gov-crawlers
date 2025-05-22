from pathlib import Path
from typing import Any

import pytest
from scrapy.http.response.html import HtmlResponse

from public_law.spiders.aus.dv_glossary import DVGlossary
from public_law.spiders.aus.ip_glossary import IPGlossary
from public_law.spiders.can.patents_glossary import PatentsGlossarySpider
from public_law.spiders.gbr.cpr_glossary import CPRGlossarySpider
from public_law.spiders.gbr.fpr_glossary import FPRGlossarySpider
from public_law.spiders.irl.courts_glossary import IRLCourtsGlossary
from public_law.spiders.nzl.justice_glossary import NZLJusticeGlossary
from public_law.spiders.usa.uscis_glossary import USCISGlossary
from public_law.spiders.usa.us_courts_glossary import USACourtsGlossary


# List of all glossary spiders to test
GLOSSARY_SPIDERS = [
    DVGlossary,
    IPGlossary,
    PatentsGlossarySpider,
    CPRGlossarySpider,
    FPRGlossarySpider,
    IRLCourtsGlossary,
    NZLJusticeGlossary,
    USCISGlossary,
    USACourtsGlossary,
]


def get_fixture_path(spider_name: str) -> Path:
    """Get the path to the fixture file for a given spider."""
    return Path(__file__).parent.parent / "fixtures" / spider_name.split("_")[0] / f"{spider_name.split('_')[1]}-glossary.html"


@pytest.fixture
def mock_response(spider_class: Any) -> HtmlResponse:
    """Create a response using the appropriate fixture file."""
    spider_name = spider_class.name
    fixture_path = get_fixture_path(spider_name)

    if not fixture_path.exists():
        pytest.skip(
            f"No fixture file found for {spider_name}")

    with open(fixture_path, "rb") as f:
        html_content = f.read()

    return HtmlResponse(
        url=f"https://example.com/{spider_name}",
        body=html_content,
        encoding="utf-8",
    )


@pytest.mark.parametrize("spider_class", GLOSSARY_SPIDERS)
def test_spider_output_format(spider_class: Any, mock_response: HtmlResponse):
    """Test that all glossary spiders use Dublin Core naming format."""
    spider = spider_class()
    result = next(spider.parse(mock_response))

    # List of required Dublin Core keys
    dc_keys = ["title", "language", "coverage", "subject", "source",
               "type", "modified", "license", "format", "creator"]

    # Verify that keys use Dublin Core format (with colons)
    assert all(f"dcterms:{key}" in result["metadata"] for key in dc_keys)

    # Verify that no keys use underscore format
    assert all(f"dcterms_{key}" not in result["metadata"] for key in dc_keys)
