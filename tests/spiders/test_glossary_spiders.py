from pathlib import Path
from typing import Any

import importlib
import inspect
import pkgutil

import pytest
from scrapy import Spider
from scrapy.http.response.html import HtmlResponse

from public_law.spiders.base import BaseGlossarySpider

# --------------------------------------------------------------------------------
# Automatic discovery of glossary spiders
# --------------------------------------------------------------------------------


def _discover_glossary_spiders() -> list[type[Spider]]:
    """Dynamically discover all glossary spider classes.

    We import every module in the ``public_law.spiders`` package tree and
    collect classes that:

    1. Inherit from ``scrapy.Spider`` (excluding the base class itself)
    2. Have a ``name`` attribute containing the substring ``glossar``

    This captures both *glossary* and *glossaries* variations.
    """

    import public_law.spiders as spiders_pkg  # Local import to avoid cycles

    spiders: list[type[Spider]] = []

    for module_info in pkgutil.walk_packages(spiders_pkg.__path__, prefix=f"{spiders_pkg.__name__}."):
        module = importlib.import_module(module_info.name)

        for obj in module.__dict__.values():
            if (
                inspect.isclass(obj)
                and issubclass(obj, BaseGlossarySpider)
                and obj is not BaseGlossarySpider
                and "glossar" in getattr(obj, "name", "")
            ):
                spiders.append(obj)  # type: ignore[arg-type]

    # Ensure deterministic ordering for pytest collection stability
    return sorted(spiders, key=lambda cls: cls.__name__)


# List of all glossary spiders to test (auto-generated)
GLOSSARY_SPIDERS = _discover_glossary_spiders()

assert GLOSSARY_SPIDERS, "No glossary spiders were discovered."


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
            f"Fixture file not found for {spider_name}: {fixture_path}")

    with open(fixture_path, "rb") as f:
        html_content = f.read()

    return HtmlResponse(
        url=f"https://example.com/{spider_name}",
        body=html_content,
        encoding="utf-8",
    )


@pytest.mark.parametrize("spider_class", GLOSSARY_SPIDERS)
def test_dublin_core_naming(spider_class: Any, mock_response: HtmlResponse):
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
