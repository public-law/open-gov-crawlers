"""Sequence (Iterables, Lists, etc.) functions."""


from typing import Any

from toolz.functoolz import curry


def get(index: int, x: list[Any]) -> Any:
    return x[index]

get = curry(get)
