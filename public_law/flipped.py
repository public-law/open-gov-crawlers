"""
Flipped versions of functions.
"""

from typing import Callable

from toolz.functoolz import flip


""" Return a copy of the string with leading characters removed. """
lstrip: Callable[[str, str], str] = flip(str.lstrip)


""" Return a copy of the string with trailing characters removed. """
rstrip: Callable[[str, str], str] = flip(str.rstrip)
