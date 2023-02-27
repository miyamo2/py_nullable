from __future__ import annotations
import copy
import inspect
import json
import sys
from typing import Any, Callable, Optional, TypedDict


Stack = TypedDict(
    "Stack",
    {
        "FileName": str,
        "FunctionName": str,
        "LineNumber": int
    }
)


class PyNullableError(Exception):
    """
    Base Class for py_nullable's Exception.
    """

    __stacktrace: list[Stack]

    def __init__(
            self,
            cause: Optional[Exception] = None,
            message: Optional[str] = None):
        """
        constructor.

        Args:
            cause (Optional[Exception], optional): causal error.
            message (Optional[str], optional): message.
        """
        exc_obj = cause if cause is not None\
            else sys.exc_info()[1]  # type: ignore

        stack_list: list[inspect.FrameInfo] = inspect.stack()

        from_subclasses: bool = not isinstance(self, stack_list[-1].__class__)

        latest_stack_index: int
        if from_subclasses:
            latest_stack_index = 2
        else:
            latest_stack_index = 1

        stack_list = stack_list[latest_stack_index:]

        self.__stacktrace = list[Stack]()
        for stack in stack_list:
            self.__stacktrace.append(
                Stack(
                    FileName=stack.filename,
                    FunctionName=stack.function,
                    LineNumber=stack.lineno
                )
            )

        latest_stack: Stack = self.__stacktrace[1]
        file_name: str = latest_stack.get("FileName")  # type: ignore
        function_name: str = latest_stack.get(
            "FunctionName")  # type: ignore
        line_no: int = latest_stack.get("LineNumber")  # type: ignore

        message_dict: dict[str, Optional[str]] = {
            "message": message,
            "at": f"{file_name}#{function_name} {line_no} line"
        }
        if exc_obj is not None:
            message_dict.update({
                "cause": str(exc_obj)
            })

        super().__init__(json.dumps(message_dict, indent=2))

    @property
    def stacktrace(self) -> list[Stack]:
        """
        Returns:
            list[Stack]: stack trace
        """
        return copy.deepcopy(self.__stacktrace)


class EmptyValueException(PyNullableError):
    """
    Indicates that the Nullable's value was None
    with behavior that should not have been None.
    """

    def __init__(self) -> None:
        """
        constructor.
        """
        super().__init__(
            message=f"Nullable's value must not to be None in this operation.")


class UncallableException(PyNullableError):
    """
    Indicates that the callback was not callable.
    """

    def __init__(self, callback: Callable[..., Any]) -> None:
        """
        constructor.

        Args:
            callback (Callable[..., Any]):
                Callback function that raised the exception.
        """
        base_class_param: dict[str, Any]
        code: Optional[str]
        try:
            code = str(inspect.getsource(callback.__code__))
        except AttributeError:
            code = str(callback)

        base_class_param: dict[str, Any] = {
            "message": f"Callback is not callable `{code}`."}

        super().__init__(**base_class_param)


class IncompleteCallBackException(PyNullableError):
    """
    Indicates that the callback did not complete successfully.
    """

    def __init__(self, callback: Callable[..., Any],
                 cause: Optional[Exception] = None) -> None:
        """
        constructor.

        Args:
            callback (Callable[..., Any]):
                Callback function that raised the exception.
            cause (Optional[Exception], optional):
                Exception raised in a callback function.
        """
        base_class_param: dict[str, Any]
        code: Optional[str]
        try:
            code = str(inspect.getsource(callback.__code__))
        except AttributeError:
            code = str(callback)

        base_class_param: dict[str, Any] = {
            "message": f"Callback is Incompleted `{code}`."}

        if cause is not None:
            base_class_param.update({"cause": cause})

        super().__init__(**base_class_param)
