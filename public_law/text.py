"""
String functions and types.
"""

import re
from typing import Any, Callable, cast

import titlecase
from bs4 import BeautifulSoup
from scrapy.http.response.html import HtmlResponse


class NonemptyString(str):
    """
    A str subclass which is guaranteed to have length > 0

    Accepts `Any` type instead of `str` so that it will work
    seamlessly with untyped 3rd party libraries like Scrapy.
    Therefore, the constructor does a certain amount of type
    checking. This class is meant to sit on the boundary
    between our local code and library code.
    """

    def __new__(cls, content: Any):
        """
        Create a new Nonempty String
        """
        match (content):
            case str(content) if len(content) > 0:
                return super().__new__(cls, content)
            case _:
                raise ValueError(f"Content is empty or not a string: {content}")


class URI(NonemptyString):
    """
    A Uniform Resource Identifier

    See: https://blog.hubspot.com/website/uri-vs-url
    """

    pass


class URL(URI):
    """
    A Uniform Resource Locator
    """

    pass


class LoCSubject(URL):
    """
    A Library of Congress subject heading URI.
    """

    def __new__(cls, id: str):
        # Accept a fully formed URI.
        # This is needed by the dataclasses deepcopy process.
        if re.match(r"^http://id.loc.gov/authorities/subjects/sh[0-9]+$", id):
            return super().__new__(cls, id)

        # Accept a bare ID.
        if re.match(r"^sh\d+$", id):
            return super().__new__(cls, f"http://id.loc.gov/authorities/subjects/{id}")

        raise ValueError(f"Invalid subject ID: {id}")


class WikidataTopic(URL):
    """
    A wikidata subject.
    """

    def __new__(cls, id: str):
        # Accept a fully formed URI.
        # This is needed by the dataclasses deepcopy process.
        if re.match(r"^https://www.wikidata.org/wiki/Q[0-9]+$", id):
            return super().__new__(cls, id)

        # Accept a bare ID.
        if re.match(r"^Q[0-9]+$", id):
            return super().__new__(cls, f"https://www.wikidata.org/wiki/{id}")

        raise ValueError(f"Invalid subject ID: {id}")


class Sentence(NonemptyString):
    """
    Currently NOP.
    
    A str subclass that generally begins with a capital letter
    and ends with a period.

    It can actually end in a few ways, due to punction style. E.g.,

        He said, "This is a sentence."

    It can also start with a number or open quote.
    """

    def __new__(cls, content: Any):
        """
        Create a new Sentence.
        """
        return super().__new__(cls, content)


def ensure_ends_with_period(text: str) -> NonemptyString:
    """
    Ensure that the string ends with a period.
    """
    match (text):
        case s if s.endswith(".") or s.endswith('."') or s.endswith('</p>'):
            return NonemptyString(text)
        case s:
            return NonemptyString(s + ".")


def make_soup(html: HtmlResponse) -> BeautifulSoup:
    """
    Create a BeautifulSoup object from the Response body.
    """
    return BeautifulSoup(
        cast(str, html.body), "html.parser"
    )  


def title_case(text: str) -> str:
    """
    A type-hinted titlecase().
    """
    hinted = cast_as_str_func(titlecase.titlecase)

    return hinted(text)


def cast_as_str_func(func: Any) -> Callable[[str], str]:
    """
    Cast a function to a function that takes a string and returns a string.
    """
    return cast(Callable[[str], str], func)


def delete_all(text: str, fragments: list[str]) -> str:
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
    """
    Remove extra whitespace from around and within the string
    """
    assert isinstance(text, str)
    
    no_newlines = text.replace("\n", " ")
    return " ".join(no_newlines.strip().split())


def normalize_nonempty(text: str) -> NonemptyString:
    """
    Remove extra whitespace from around and within the string,
    combined with instantiation of a NonemptyString.
    """
    assert isinstance(text, str)

    return NonemptyString(normalize_whitespace(text))


def capitalize_first_char(text: str) -> str:
    """
    Capitalize the first character of the string
    """
    return text[0].upper() + text[1:]


def truncate_words(text: str, words_count: int) -> str:
    """
    Truncates a given text after a given number of words (words_count).
    """
    words = text.split()
    if len(words) <= words_count:
        return text

    return " ".join(words[:words_count]) + "..."
