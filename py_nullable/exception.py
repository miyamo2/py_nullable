from __future__ import annotations
import copy
import inspect
import json
import sys
from typing import Any, Callable, Optional


class Stack:

    def __init__(self, filename: str, functionname: str, linenumber: int):
        self.__filename: str = filename
        self.__functionname: str = functionname
        self.__linenumber: int = linenumber

    def get(self, key: str) -> Any:
        if key == "FileName":
            return self.FileName
        elif key == "FunctionName":
            return self.FunctionName
        elif key == "LineNumber":
            return self.LineNumber
        else:
            return None

    def __getitem__(self, key: str):
        if key == "FileName":
            return self.FileName
        elif key == "FunctionName":
            return self.FunctionName
        elif key == "LineNumber":
            return self.LineNumber
        else:
            raise KeyError(key)

    @property
    def FileName(self) -> str:
        return self.__filename

    @property
    def FunctionName(self) -> str:
        return self.__functionname

    @property
    def LineNumber(self) -> int:
        return self.__linenumber


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

        self.__stacktrace = []
        for stack in stack_list:
            self.__stacktrace.append(
                Stack(
                    filename=stack.filename,
                    functionname=stack.function,
                    linenumber=stack.lineno
                )
            )

        latest_stack: Stack = self.__stacktrace[1]
        file_name: str = latest_stack.FileName
        function_name: str = latest_stack.FunctionName
        line_no: int = latest_stack.LineNumber

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
