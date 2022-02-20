import pytest
from public_law.text import NonemptyString


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
            NonemptyString()  # pylint: disable=no-value-for-parameter

    def test_raises_error_if_empty_string_given(self):
        with pytest.raises(ValueError, match="empty"):
            NonemptyString("")

    def test_raises_error_if_non_string_type_given(self):
        with pytest.raises(ValueError):
            NonemptyString(123)
