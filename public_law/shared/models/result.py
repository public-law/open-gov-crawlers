"""
A Rust-like Result type. 

It's not yet used in the project, but it'd be interesting to see
if it creates cleaner code.
"""

from dataclasses import dataclass
from typing import TypeVar, Generic, Any, TypeAlias, Callable

T = TypeVar("T")
U = TypeVar("U")


@dataclass
class Ok(Generic[T]):
    value: T

    def and_then(self, f: Callable[[T], 'Result[U]']) -> 'Result[U]':
        return f(self.value)

    def map(self, f: Callable[[T], U]) -> 'Result[U]':
        return Ok(f(self.value))

    def unwrap(self) -> T:
        return self.value

    def unwrap_or(self, _: T) -> T:
        return self.value


@dataclass
class Err:
    error: Any

    def and_then(self, _: Any) -> 'Err':
        return self

    def map(self, _: Any) -> 'Err':
        return self

    def unwrap(self) -> Any:
        raise Exception(self.error)

    def unwrap_or(self, default: Any) -> Any:
        return default


Result: TypeAlias = Ok[T] | Err


def cat_oks(results: list[Result[T]]) -> tuple[T, ...]:
    """
    Concatenate a list of Results into a tuple of their values.

    Args:
        results: A list of Results.

    Returns:
        A tuple of the values of the Ok Results.
    """
    return tuple(result.value for result in results if isinstance(result, Ok))
