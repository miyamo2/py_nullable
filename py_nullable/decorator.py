import functools
from typing import Any, Callable, Optional, TypeVar
from .nullable import Nullable

T = TypeVar("T")


def nullable_wrap(
    func: Callable[..., Optional[T]]
) -> Callable[..., Nullable[T]]:
    """
    Decorator that wraps the return value of an Optional[T] type in Nullable[T]

    Example:
        >>> in_memory_db: dict[str, YourClass] = {"A001": YourClass("foo")}
        ...
        ...
        ... @nullable_wrap
        ... def find_by_id(id: str) -> Optional[YourClass]:
        ...     return in_memory_db.get(id)
        ...
        ...
        ... nullable: Nullable[YourClass] = find_by_id("B001")
        ... print(nullable.isEmpty())
            True
    """
    @functools.wraps(func)
    def _(*args: Any, **kwargs: Any) -> Nullable[T]:
        value: Optional[T] = func(*args, **kwargs)
        return Nullable[T](value)

    return _
