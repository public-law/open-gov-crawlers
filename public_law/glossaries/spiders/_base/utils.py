from __future__ import annotations

"""Utilities for working with Scrapy spiders at runtime."""

import importlib
import inspect
import pkgutil

from public_law.glossaries.spiders._base.base import BaseGlossarySpider
from public_law.glossaries.spiders._base.enhanced_base import AutoGlossarySpider, EnhancedAutoGlossarySpider


def discover_glossary_spiders() -> list[type[BaseGlossarySpider | AutoGlossarySpider | EnhancedAutoGlossarySpider]]:
    """Return all glossary spider classes in *public_law.glossaries.spiders*.

    A *glossary spider* is defined as any subclass of :class:`BaseGlossarySpider`
    or :class:`AutoGlossarySpider` whose :pyattr:`~scrapy.Spider.name` attribute 
    contains the substring ``"glossar"`` (matching both *glossary* and *glossaries*).
    The returned list is sorted alphabetically by class name to provide a
    deterministic order for test parametrization.
    """

    # Local import to avoid import-time side-effects
    import public_law.glossaries.spiders as spiders_pkg

    spiders: list[type[BaseGlossarySpider | AutoGlossarySpider | EnhancedAutoGlossarySpider]] = []

    for module_info in pkgutil.walk_packages(spiders_pkg.__path__, prefix=f"{spiders_pkg.__name__}."):
        module = importlib.import_module(module_info.name)

        for obj in module.__dict__.values():
            if (
                inspect.isclass(obj)
                and (issubclass(obj, BaseGlossarySpider) or issubclass(obj, AutoGlossarySpider) or issubclass(obj, EnhancedAutoGlossarySpider))
                and obj not in (BaseGlossarySpider, AutoGlossarySpider, EnhancedAutoGlossarySpider)
            ):
                spiders.append(obj)

    return sorted(spiders, key=lambda cls: cls.__name__)
