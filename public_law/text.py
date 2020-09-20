from typing import Any, List


def delete_all(text: str, fragments: List[str]) -> str:
    """
    A copy of text with all the fragments removed.
    """
    result = text
    for s in fragments:
        result = delete(result, s)
    return result


def delete(text: str, fragment: str) -> str:
    """
    A copy of text with the fragment removed.
    """
    return text.replace(fragment, "")


def normalize_whitespace(text: str) -> str:
    """Remove extra whitespace from around and within the string"""
    return " ".join(text.strip().split())


class NonemptyString(str):
    """A string which is guaranteed to have length > 0"""

    def __new__(cls, content: Any):
        if (not isinstance(content, str)) or len(content) == 0:
            raise ValueError("Content is empty, cannot create a NonemptyString")

        return super().__new__(cls, content)  # type: ignore
