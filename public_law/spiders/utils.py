from __future__ import annotations

"""Utilities for working with Scrapy spiders at runtime."""

from typing import List, Type

import importlib
import inspect
import pkgutil

from scrapy import Spider

from .base import BaseGlossarySpider

__all__ = ["discover_glossary_spiders"]


def discover_glossary_spiders() -> list[type[Spider]]:
    """Return all glossary spider classes in *public_law.spiders*.

    A *glossary spider* is defined as any subclass of :class:`BaseGlossarySpider`
    whose :pyattr:`~scrapy.Spider.name` attribute contains the substring
    ``"glossar"`` (matching both *glossary* and *glossaries*).
    The returned list is sorted alphabetically by class name to provide a
    deterministic order for test parametrization.
    """

    # Local import to avoid import-time side-effects
    import public_law.spiders as spiders_pkg

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
                spiders.append(obj)

    return sorted(spiders, key=lambda cls: cls.__name__)
