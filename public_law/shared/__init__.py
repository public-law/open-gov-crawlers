"""
Shared functionality used across the public_law package.

This package contains:
- models: Core data structures and metadata
- utils: Utility functions for text processing, HTML parsing, dates, etc.
- spiders: Base spider classes and protocols
- exceptions: Shared exception classes
"""

# Expose key shared models and utilities
from .models.metadata import Metadata, Subject
from .models.result import Result
from .utils.text import NonemptyString, titleize, truncate_words
from .utils.dates import today, todays_date
from .utils.html import just_text, xpath

__all__ = [
    "Metadata", 
    "Subject",
    "Result",
    "NonemptyString",
    "titleize", 
    "truncate_words",
    "today",
    "todays_date", 
    "just_text",
    "xpath"
] 
