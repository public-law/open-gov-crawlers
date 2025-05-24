#!/usr/bin/env python3
"""
Test the validation system for AutoGlossarySpider.
"""


def test_missing_name():
    """Test that missing name attribute raises TypeError at class definition."""
    try:
        from public_law.spiders.enhanced_base import AutoGlossarySpider

        class MissingNameSpider(AutoGlossarySpider):
            start_urls = ["https://example.com/glossary"]

        assert False, "Should have raised TypeError for missing name"
    except TypeError as e:
        print(f"✓ Caught missing name error: {e}")
        assert "must define a 'name' class attribute" in str(e)


def test_missing_urls():
    """Test that missing start_urls raises TypeError at class definition."""
    try:
        from public_law.spiders.enhanced_base import AutoGlossarySpider

        class MissingUrlsSpider(AutoGlossarySpider):
            name = "aus_missing_urls_glossary"

        assert False, "Should have raised TypeError for missing start_urls"
    except TypeError as e:
        print(f"✓ Caught missing start_urls error: {e}")
        assert "must define a 'start_urls' class attribute" in str(e)


def test_invalid_name_format():
    """Test that invalid name format raises ValueError."""
    try:
        from public_law.spiders.enhanced_base import AutoGlossarySpider

        class InvalidNameSpider(AutoGlossarySpider):
            name = "invalid-name-format"
            start_urls = ["https://example.com/glossary"]

        assert False, "Should have raised ValueError for invalid name format"
    except ValueError as e:
        print(f"✓ Caught invalid name format error: {e}")
        assert "must follow pattern" in str(e)


def test_valid_spider():
    """Test that valid spider creates successfully."""
    from public_law.spiders.enhanced_base import AutoGlossarySpider

    class ValidSpider(AutoGlossarySpider):
        name = "aus_valid_glossary"
        start_urls = ["https://example.com/glossary"]

    print("✓ Valid spider created successfully")
    assert ValidSpider.name == "aus_valid_glossary"
    assert ValidSpider.start_urls == ["https://example.com/glossary"]


if __name__ == "__main__":
    print("Testing AutoGlossarySpider validation...\n")

    test_missing_name()
    test_missing_urls()
    test_invalid_name_format()
    test_valid_spider()

    print("\n" + "="*50)
    print("All validation tests passed! 🎉")
    print("Invalid spider configurations are caught at class definition time.")
