import re

from scrapy.http.response.html import HtmlResponse
from bs4 import BeautifulSoup
from typing import Any, Callable, List, cast
import titlecase


class NonemptyString(str):
    """A str subclass which is guaranteed to have length > 0

    Accepts `Any` type instead of `str` so that it will work
    seamlessly with untyped 3rd party libraries like Scrapy.
    Therefore, the constructor does a certain amount of type
    checking. This class is meant to sit on the boundary
    between our local code and library code.
    """

    def __new__(cls, content: Any):
        """Create a new Nonempty String"""
        match (content):
            case str(content) if len(content) > 0:
                return super().__new__(cls, content)
            case _:
                raise ValueError("Content is empty or not a string.")


class Sentence(NonemptyString):
    """A str subclass that begins with a capital letter and ends with a period.

    It can actually end in a few ways, due to punction style. E.g.,

        He said, "This is a sentence."
    """

    def __new__(cls, content: Any):
        """Create a new Sentence."""
        match re.match(r"^[A-Z].*\.[\"\)]?$", content):
            case None:
                raise ValueError(f"Not a proper sentence: {content}")
            case _:
                return super().__new__(cls, content)


def ensure_ends_with_period(text: str) -> str:
    """
    Ensure that the string ends with a period.
    """
    match (text):
        case s if s.endswith(".") or s.endswith('."'):
            return text
        case s:
            return s + "."


def make_soup(html: HtmlResponse) -> BeautifulSoup:
    return BeautifulSoup(cast(str, html.body), "html.parser")


def title_case(text: str) -> str:
    """A type-hinted titlecase()."""

    str_func: Callable[[str], str] = cast(
        Callable[[str], str],
        # pyright: reportUnknownMemberType=false
        titlecase.titlecase,
    )
    return str_func(text)


def cast_as_str_func(func: Any) -> Callable[[str], str]:
    """
    Cast a function to a function that takes a string and returns a string.
    """
    return cast(Callable[[str], str], func)


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


def normalize_nonempty(text: str) -> NonemptyString:
    """Remove extra whitespace from around and within the string"""
    return NonemptyString(normalize_whitespace(text))


def capitalize_first_char(text: str) -> str:
    """Capitalize the first character of the string"""
    return text[0].upper() + text[1:]
