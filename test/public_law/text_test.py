from public_law.text import NonemptyString


class TestNonemptyString:
    def test_supports_value_equality(self):
        ns = NonemptyString("hello")
        assert ns == "hello"

    def test_supports_lt(self):
        a = NonemptyString("a")
        assert a < "b"