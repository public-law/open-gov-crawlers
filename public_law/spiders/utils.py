from __future__ import annotations

"""Utilities for working with Scrapy spiders at runtime."""

import importlib
import inspect
import pkgutil
import sys
from typing import Type

from .base import BaseGlossarySpider
from scrapy.http.response.html import HtmlResponse

from ..models.glossary import GlossaryParseResult


def discover_glossary_spiders() -> list[type[BaseGlossarySpider]]:
    """Return all glossary spider classes in *public_law.spiders*.

    A *glossary spider* is defined as any subclass of :class:`BaseGlossarySpider`
    whose :pyattr:`~scrapy.Spider.name` attribute contains the substring
    ``"glossar"`` (matching both *glossary* and *glossaries*).
    The returned list is sorted alphabetically by class name to provide a
    deterministic order for test parametrization.
    """

    # Local import to avoid import-time side-effects
    import public_law.spiders as spiders_pkg

    spiders: list[type[BaseGlossarySpider]] = []

    for module_info in pkgutil.walk_packages(spiders_pkg.__path__, prefix=f"{spiders_pkg.__name__}."):
        module = importlib.import_module(module_info.name)

        for obj in module.__dict__.values():
            if (
                inspect.isclass(obj)
                and issubclass(obj, BaseGlossarySpider)
                and obj is not BaseGlossarySpider
            ):
                spiders.append(obj)

    return sorted(spiders, key=lambda cls: cls.__name__)


def create_glossary_spider(
    name: str,
    start_urls: list[str],
    parser_module_path: str,
    class_name: str | None = None,
    auto_register: bool = True,
) -> Type[BaseGlossarySpider]:
    """
    Factory function to create glossary spider classes declaratively.

    Args:
        name: Spider name (e.g., "aus_dv_glossary")
        start_urls: List of URLs to crawl
        parser_module_path: Import path to parser module (e.g., "public_law.parsers.aus.dv_glossary")
        class_name: Optional class name. If not provided, generates from spider name.
        auto_register: If True, registers the class in the calling module's namespace for auto-discovery.

    Returns:
        A dynamically created spider class
    """
    # Import the parser module
    parser_module = importlib.import_module(parser_module_path)
    parse_glossary_func = parser_module.parse_glossary

    class DynamicGlossarySpider(BaseGlossarySpider):
        def parse_glossary(self, response: HtmlResponse) -> GlossaryParseResult:
            return parse_glossary_func(response)

    # Set class attributes
    DynamicGlossarySpider.name = name
    DynamicGlossarySpider.start_urls = start_urls

    # Generate a proper class name
    if class_name is None:
        class_name = f"{name.title().replace('_', '')}Spider"
    DynamicGlossarySpider.__name__ = class_name
    DynamicGlossarySpider.__qualname__ = class_name

    # Auto-register in calling module's namespace for auto-discovery
    if auto_register:
        # Get the calling module (the one that called this factory)
        calling_frame = inspect.currentframe().f_back  # type: ignore
        calling_module = inspect.getmodule(calling_frame)  # type: ignore

        if calling_module:
            # Set the class in the calling module's namespace
            setattr(calling_module, class_name, DynamicGlossarySpider)

            # Also set it in sys.modules for the module
            if calling_module.__name__ in sys.modules:
                setattr(sys.modules[calling_module.__name__],
                        class_name, DynamicGlossarySpider)

    return DynamicGlossarySpider
