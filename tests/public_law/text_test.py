import pytest

from public_law.shared.utils.text import NonemptyString, titleize, truncate_words, ensure_ends_with_period, ensure_starts_with_capital


class TestTitleize:
    def test_roman_numeral(self):
        assert titleize("title i") == "Title I"


class TestNonemptyString:
    def test_supports_value_equality(self):
        ns = NonemptyString("hello")
        assert ns == "hello"

    def test_supports_lt(self):
        a = NonemptyString("a")
        assert a < "b"

    def test_supports_gt(self):
        b = NonemptyString("b")
        assert b > "a"

    def test_raises_error_if_no_param_given(self):
        with pytest.raises(Exception):
            NonemptyString()  # type: ignore

    def test_raises_error_if_empty_string_given(self):
        with pytest.raises(ValueError, match="empty"):
            _ = NonemptyString("")

    def test_raises_error_if_non_string_type_given(self):
        with pytest.raises(ValueError):
            _ = NonemptyString(123)


class TestTruncateWords:
    def test_truncates_words_to_length_1(self):
        assert truncate_words("hello world", 1) == "hello..."

    def test_rails_test_case(self):
        input = 'Once upon a time in a world far far away'
        output = "Once upon a time..."

        assert truncate_words(input, 4) == output

    def test_the_current_use_case_1(self):
        input = 'Glossary of Parliamentary Terms for Intermediate Students'
        output = "Glossary of Parliamentary Terms for..."

        assert truncate_words(input, 5) == output

    def test_the_current_use_case_2(self):
        input = 'Dept. of Justice Legal Glossaries'
        output = input

        assert truncate_words(input, 5) == output
