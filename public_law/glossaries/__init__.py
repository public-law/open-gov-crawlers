"""
Glossary-related functionality for parsing and crawling legal glossaries.

This package contains:
- models: Data structures for glossary entries and metadata
- parsers: Functions to parse glossary content from various jurisdictions  
- spiders: Scrapy spiders for crawling glossary websites
- utils: Utility functions specific to glossary processing
"""

# Expose key glossary models and functions
from .models.glossary import (
    GlossaryEntry,
    GlossaryParseResult, 
    glossary_fixture
)

__all__ = [
    "GlossaryEntry",
    "GlossaryParseResult", 
    "glossary_fixture"
]
