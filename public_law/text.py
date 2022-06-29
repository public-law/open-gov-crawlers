from typing import Any, List


def delete_all(text: str, fragments: List[str]) -> str:
    """
    A copy of text with all the fragments removed.
    """
    result = text
    for string in fragments:
        result = delete(result, string)
    return result


def delete(text: str, fragment: str) -> str:
    """
    A copy of text with the fragment removed.
    """
    return text.replace(fragment, "")


def normalize_whitespace(text: str) -> str:
    """Remove extra whitespace from around and within the string"""
    return " ".join(text.strip().split())


def capitalize_first_char(text: str) -> str:
    """Capitalize the first character of the string"""
    return text[0].upper() + text[1:]


class NonemptyString(str):
    """A string which is guaranteed to have length > 0

    Accepts `Any` type instead of `str` so that it will work
    seamlessly with untyped 3rd party libraries like Scrapy.
    Therefore, the constructor does a certain amount of type
    checking. This class is meant to sit on the boundary
    between our local code and library code.
    """

    def __new__(cls, content: Any):
        """Create a new Nonempty String"""
        if (not isinstance(content, str)) or len(content) == 0:
            raise ValueError("Content is empty, cannot create a NonemptyString")

        return super().__new__(cls, content)  # type: ignore
