"""
Examples of broken spiders to demonstrate validation.
These should fail at import time, not runtime.
"""

from ..enhanced_base import AutoGlossarySpider

# This should work fine


class ValidSpider(AutoGlossarySpider):
    name = "aus_valid_glossary"
    start_urls = ["https://example.com/glossary"]

# Uncomment these to see validation errors at import time:

# class MissingNameSpider(AutoGlossarySpider):
#     # Missing name attribute
#     start_urls = ["https://example.com/glossary"]

# class MissingUrlsSpider(AutoGlossarySpider):
#     name = "aus_missing_urls_glossary"
#     # Missing start_urls attribute

# class InvalidNameSpider(AutoGlossarySpider):
#     name = "invalid-name-format"  # Wrong format
#     start_urls = ["https://example.com/glossary"]

# class EmptyNameSpider(AutoGlossarySpider):
#     name = ""  # Empty name
#     start_urls = ["https://example.com/glossary"]
