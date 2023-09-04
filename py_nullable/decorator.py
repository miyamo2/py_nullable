#!/usr/bin/python
# -*- coding: utf-8 -*-
"""py_nullable's decorator function

Function:
    * nullable_wrap

"""
import functools
from typing import Any, Callable, Optional, TypeVar
from .nullable import Nullable

_T = TypeVar("_T")


def nullable_wrap(
    func: Callable[..., Optional[_T]]
) -> Callable[..., Nullable[_T]]:
    """Decorator that wraps the return value of an Optional[T] type in Nullable[T]

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
    def _(*args: Any, **kwargs: Any) -> Nullable[_T]:
        value: Optional[_T] = func(*args, **kwargs)
        return Nullable[_T](value)

    return _
