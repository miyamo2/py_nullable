from __future__ import annotations
import copy
from typing import Any, Callable, Generic, Optional, TypeVar
from .exception\
    import IncompleteCallBackException, EmptyValueException, UncallableException

T = TypeVar('T')
U = TypeVar('U')


class Nullable(Generic[T]):
    """
    Wrap instances of generic type or None.

    Attributes:
        __val (Optional[T]): None or generic type value
    """

    __slots__ = ['__val']

    __val: Optional[T]

    def __init__(self, value: Optional[T] = None) -> None:
        """
        constructor.

        Args:
            val (Optional[T]): None or generic type value
        """
        self.__val = value

    @property
    def __value(self) -> Optional[T]:
        return copy.deepcopy(self.__val)

    def isPresent(self) -> bool:
        """
        If a value is not None, returns true, otherwise false.

        Returns:
            bool: true if a value is not None, otherwise false.

        Example:
            >>> nullable: Nullable[str] = Nullable[str]("some string")
                if nullable.isPresent():
                    print("has valid value")
            has valid value
        """
        return self.__value is not None

    def isEmpty(self) -> bool:
        """
        If a value is None, returns true, otherwise false.

        Returns:
            bool: true if a value is None, otherwise false.

        Example:
            >>> nullable: Nullable[str] = Nullable[str](None)
                if nullable.isEmpty():
                    print("empty obj")
            empty obj
        """
        return self.__value is None

    def get(self) -> T:
        """
        If a value is not None, returns the value,
        otherwise raises EmptyValueException.

        Raises:
            EmptyValueException: If a value is None.

        Returns:
            T: If a value is not None, returns the value.

        Example:
            >>> nullable: Nullable[str] = Nullable[str]("some string")
                val: str = nullable.get()
                print(val)
            some string
        """
        if self.__value is None:
            raise EmptyValueException()
        return self.__value

    def orElse(self, other: T) -> T:
        """
        If a value is not None, returns the value,
        otherwise returns other.

        Args:
            other (T): to be returned, if value is None.

        Returns:
            T: the value, if not None, otherwise other

        Example:
            >>> nullable: Nullable[str] = Nullable[str](None)
                val: str = nullable.orElse("other string")
                print(val)
            other string
        """
        if self.__value is None:
            return other
        else:
            return self.__value

    def orElseGet(
        self,
        supplier: Callable[..., T],
        *args: Any,
        **kwargs: Any
    ) -> T:
        """
        If a value is not None, returns the value,
        otherwise returns the result produced by the supplier.

        Args:
            supplier (Callable[..., T]):
                the supplying function that produces a value to be returned.

        Raises:
            UncallableException:
                if the value is None, and the given supplier is not callable.
            IncompleteCallBackException:
                if the value is None, and the given supplier raises some exception.

        Returns:
            T: the value, if not None, otherwise the result produced by the supplier.

        Example:
            >>> nullable: Nullable[str] = Nullable[str](None)
                val: str = nullable.orElse(lambda x, y: str(x + y), 1, 2)
                print(val)
            3
        """
        result: T

        if self.__value is None:
            if not isinstance(supplier, Callable):
                raise UncallableException(callback=supplier)
            try:
                result = supplier(*args, **kwargs)
            except Exception as e:
                raise IncompleteCallBackException(cause=e, callback=supplier)
        else:
            result = self.__value

        return result

    def orElseRaise(
        self,
        supplier: Callable[..., Exception],
        *args: Any,
        **kwargs: Any
    ) -> T:
        """
        If a value is present, returns the value,
        otherwise raises an exception produced by the supplier.

        Args:
            supplier (Callable[..., Exception]):
                the supplying function that produces an exception to be raised.

        Raises:
            UncallableException:
                if the value is None, and the given supplier is not callable.
            IncompleteCallBackException:
                if the value is None, and the given supplier raises some exception.

        Returns:
            T: If a value is not None, returns the value.

        Example:
            >>> nullable: Nullable[str] = Nullable[str](None)
                try:
                    val: str = nullable.orElseRaise(lambda x: Exception(str(x)), 1)
                except Exception as e:
                    print(str(e))
            1
        """
        exception: Optional[Exception] = None
        if self.__value is None:
            if not isinstance(supplier, Callable):
                raise UncallableException(callback=supplier)

            try:
                exception = supplier(*args, **kwargs)
            except Exception as e:
                raise IncompleteCallBackException(cause=e, callback=supplier)

            raise exception
        else:
            return self.__value

    def ifPresent(self, action: Callable[[T], None]) -> None:
        """
        If a value is not None,
        performs the given action with the value,
        otherwise does nothing.

        Args:
            action (Callable[[T], None]):
                to be performed, if a value is not None.

        Raises:
            UncallableException:
                if the value is None, and the given action is not callable.
            IncompleteCallBackException:
                if the value is None, and the given action raises some exception.

        Example:
            >>> nullable: Nullable[str] = Nullable[str]("some string")
                nullable.ifPresent(lambda x: print(x))
            some string
        """
        if self.__value is not None:
            if not isinstance(action, Callable):
                raise UncallableException(callback=action)
            try:
                action(self.__value)
            except Exception as e:
                raise IncompleteCallBackException(cause=e, callback=action)

    def filter(self, extractor: Callable[[T], bool]) -> Nullable[T]:
        """
        If a value is not None,
        and the value matches the given extractor,
        returns an Optional describing the value,
        otherwise returns an empty Optional.

        Args:
            extractor (Callable[[T], bool]):
                the extract to apply to a value, if a value is not None.

        Raises:
            UncallableException:
                if the given extractor is not callable.
            IncompleteCallBackException:
                if the given extractor raises some exception.

        Returns:
            Nullable[T]:
                a Nullable describing the value of this Nullable,
                if a value is not None and the value matches the given extractor,
                otherwise an empty Nullable

        Example:
            >>> nullable: Nullable[str] = Nullable[str]("1")
                result: Nullable[str] = nullable.filter(lambda x: lambda x: x.isdigit())
                val: str = result.get()
                print(val)
            1
        """
        result: Nullable[T]

        if not isinstance(extractor, Callable):
            raise UncallableException(callback=extractor)

        if self.__value is None:
            result = Nullable[T](None)
        else:
            try:
                result = self if extractor(self.__value) else Nullable[T](None)
            except Exception as e:
                raise IncompleteCallBackException(cause=e, callback=extractor)

        return result

    def map(self, mapper: Callable[[T], U]) -> Nullable[U]:
        """
        If a value is not None,
        returns an Nullable describing the result of applying the given mapper to the value,
        otherwise returns an empty Nullable.

        Args:
            mapper (Callable[[T], U]):
                the mapping function to apply to a value, if a value is not None.
                U: The type of the value returned from the mapping function.

        Raises:
            UncallableException:
                if the given mapper is not callable.
            IncompleteCallBackException:
                if the given mapper raises some exception.

        Returns:
            Nullable[U]: _description_

        Examples:
            >>> nullable: Nullable[int] = Nullable[int](1)
                result: Nullable[int] = nullable.map(lambda x: x * 2)
                print(result.get())
            2
        """
        result: Nullable[U]

        if not isinstance(mapper, Callable):
            raise UncallableException(callback=mapper)

        if self.__value is None:
            result = Nullable(None)
        else:
            try:
                result = Nullable(mapper(self.__value))
            except Exception as e:
                raise IncompleteCallBackException(cause=e, callback=mapper)

        return result

    def flatMap(self, mapper: Callable[[T], Nullable[U]]) -> Nullable[U]:
        """
        If a value is not None,
        returns the result of applying the given mapper to the value,
        otherwise returns an empty Nullable.

        Args:
            mapper (Callable[[T], Nullable[U]]):
                the mapping function to apply to a value, if a value is not None.
                U:
                    The type of value of the Nullable returned by the mapping function.

        Raises:
            UncallableException:
                if the mapper is not callable.
            IncompleteCallBackException:
                if the mapper raises some exception.

        Returns:
            Nullable[U]:
                the result of applying a Nullable-bearing mapper to the value of this Nullable,
                if a value is not None, otherwise an empty Nullable.

        Examples:
            >>> nullable: Nullable[str] = Nullable[str]("1234")
                callback: Callable[[str], Nullable[int]] = lambda x: Nullable[int](int(x) * 2)
                result = target.flatMap(mapper=callback)
                print(result.get())
            2468
        """
        result: Nullable[U]

        if not isinstance(mapper, Callable):
            raise UncallableException(callback=mapper)

        if self.__value is None:
            result = Nullable(None)
        else:
            try:
                result = mapper(self.__value)
            except Exception as e:
                raise IncompleteCallBackException(cause=e, callback=mapper)

        return result

    def equals(self, compare_target: Nullable[Any]) -> bool:
        """
        Compare whether two Nullable object are equal.

        If the two conditions are satisfied,
        Nullable object are considered equal...
            * both Nullable have equal type
            * both Nullable have equal value


        Args:
            compare_target (Nullable[Any]):
                Nullable object to be tested for equality.

        Returns:
            bool:
                true if the compare_target is "equal to" this object otherwise false.

        Examples:
            >>> nullable: Nullable[str] = Nullable[str]("1234")
                compare: Nullable[str] = Nullable[str]("1234")
                print(nullable.equals(compare))
            True

            >>> nullable: Nullable[str] = Nullable[str]("1234")
                compare: Nullable[str] = Nullable[str]("12345")
                print(nullable.equals(compare))
            False

            >>> nullable: Nullable[str] = Nullable[str]("1234")
                compare: Nullable[int] = Nullable[int](1234)
                print(nullable.equals(compare))
            False
        """
        return (
            isinstance(compare_target.__value, self.__value.__class__)
            and self.__value == compare_target.__value
        )
