from typing import Any, cast
from toolz.functoolz import pipe # type: ignore

from .text import NonemptyString


def pipe_to_string(*args: Any) -> NonemptyString:
    """A wrapper around pipe() that casts the result to a NonemptyString."""
    args_with_string: Any = args + (NonemptyString,)

    return cast(NonemptyString, pipe(*args_with_string))
    
