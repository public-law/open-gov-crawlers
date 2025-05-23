from dataclasses import dataclass
from typing import TypeVar, Generic, Any, TypeAlias, Callable

T = TypeVar("T")
U = TypeVar("U")


@dataclass
class Ok(Generic[T]):
    value: T

    def and_then(self, f: Callable[[T], 'Result[U]']) -> 'Result[U]':
        return f(self.value)

    def unwrap(self) -> T:
        return self.value

    def unwrap_or(self, _: T) -> T:
        return self.value


@dataclass
class Err:
    error: Any

    def and_then(self, _: Any) -> 'Err':
        return self

    def unwrap(self) -> Any:
        raise Exception(self.error)

    def unwrap_or(self, default: Any) -> Any:
        return default


Result: TypeAlias = Ok[T] | Err


def cat_oks(results: list[Result[T]]) -> list[T]:
    """
    Concatenate a list of Results into a list of their values.

    Args:
        results: A list of Results.

    Returns:
        A list of the values of the Ok Results.
    """
    return [result.value for result in results if isinstance(result, Ok)]
