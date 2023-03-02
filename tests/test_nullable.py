import inspect
import json
from typing import Callable, Optional, Union
import pytest
from py_nullable import Nullable, nullable_wrap,\
    EmptyValueException, Stack, UncallableException,\
    IncompleteCallBackException


class TestTarget:

    def __init__(self, value: int) -> None:
        self.__value = value

    def setValue(self, value: int) -> None:
        self.__value = value

    def getValue(self) -> int:
        return self.__value


def test_isPresent_case_of_empty():
    target: Nullable[str] = Nullable[str](None)
    assert not target.isPresent()


def test_isPresent_case_of_present():
    target: Nullable[str] = Nullable[str]("test")
    assert target.isPresent()


def test_isEmpty_case_of_empty():
    target: Nullable[str] = Nullable[str](None)
    assert target.isEmpty()


def test_isEmpty_case_of_present():
    target: Nullable[str] = Nullable[str]("test")
    assert not target.isEmpty()


def test_get_case_of_present():
    excepted: str = "foo"
    target: Nullable[str] = Nullable[str](excepted)
    assert target.get() == excepted


def test_get_case_of_empty():
    target: Nullable[str] = Nullable[str](None)
    with pytest.raises(Exception) as excinfo:
        target.get()
    assert excinfo.errisinstance(EmptyValueException)


def test_orElse_case_of_present():
    excepted: str = "foo"
    target: Nullable[str] = Nullable[str](excepted)
    assert target.orElse("bar") == excepted


def test_orElse_case_of_empty():
    excepted: str = "foo"
    target: Nullable[str] = Nullable[str](None)
    assert target.orElse(excepted) == excepted


def test_orElseGet_case_of_present():
    target: Nullable[bool] = Nullable[bool](True)
    callback: Callable[[], bool] = lambda: False
    assert target.orElseGet(callback)


def test_orElseGet_case_of_empty():
    excepted: str = "2"
    target: Nullable[str] = Nullable[str](None)
    callback: Callable[[int, int], str] = lambda x, y: str(x + y)
    assert target.orElseGet(callback, 1, 1) == excepted


def test_orElseGet_case_of_invalid_callback():
    target: Nullable[bool] = Nullable[bool](None)

    current_frame = inspect.currentframe()
    code_type = current_frame.f_code  # type: ignore
    current_filename: str = code_type.co_filename
    current_methodname: str = code_type.co_name

    expected_lineno: int = 0
    with pytest.raises(Exception) as excinfo:
        expected_lineno = current_frame.f_lineno + 1  # type: ignore
        target.orElseGet("1")  # type: ignore

    assert excinfo.errisinstance(UncallableException)

    actual_message: str = str(excinfo.value)
    assert "Callback is not callable `1`" in actual_message
    assert json.dumps(
        f"{current_filename}#{current_methodname} {expected_lineno} line"
    ) in actual_message


def test_orElseGet_case_of_incomplete_callback():
    target: Nullable[bool] = Nullable[bool](None)

    current_frame = inspect.currentframe()
    code_type = current_frame.f_code  # type: ignore
    current_filename: str = code_type.co_filename
    current_methodname: str = code_type.co_name

    expected_lineno: int = 0
    with pytest.raises(Exception) as excinfo:
        expected_lineno = current_frame.f_lineno + 1  # type: ignore
        target.orElseGet(lambda x, y: x / y, 0, 0)

    assert excinfo.errisinstance(IncompleteCallBackException)

    actual_message: str = str(excinfo.value)
    assert "division by zero" in actual_message
    assert "target.orElseGet(lambda x, y: x / y, 0, 0)" in actual_message
    assert json.dumps(
        f"{current_filename}#{current_methodname} {expected_lineno} line"
    ) in actual_message


def test_orElseRaise_case_of_empty():
    excepted: str = "foo"
    target: Nullable[str] = Nullable[str](None)
    callback: Callable[[str], Exception] = lambda x: Exception(x)

    with pytest.raises(Exception) as excinfo:
        target.orElseRaise(callback, excepted)

    actual_message: str = str(excinfo.value)
    assert actual_message == excepted


def test_orElseRaise_case_of_present():
    excepted: str = "foo"
    target: Nullable[str] = Nullable[str](excepted)
    callback: Callable[[str], Exception] = lambda x: Exception(x)

    assert target.orElseRaise(callback, "") == excepted


def test_orElseRaise_case_of_invalid_callback():
    target: Nullable[str] = Nullable[str](None)

    current_frame = inspect.currentframe()
    code_type = current_frame.f_code  # type: ignore
    current_filename: str = code_type.co_filename
    current_methodname: str = code_type.co_name

    expected_lineno: int = 0
    with pytest.raises(Exception) as excinfo:
        expected_lineno = current_frame.f_lineno + 1  # type: ignore
        target.orElseRaise("1")  # type: ignore

    assert excinfo.errisinstance(UncallableException)

    actual_message: str = str(excinfo.value)
    assert "Callback is not callable `1`" in actual_message
    assert json.dumps(
        f"{current_filename}#{current_methodname} {expected_lineno} line"
    ) in actual_message


def test_orElseRaise_case_of_incomplete_callback():
    target: Nullable[str] = Nullable[str](None)

    current_frame = inspect.currentframe()
    code_type = current_frame.f_code  # type: ignore
    current_filename: str = code_type.co_filename
    current_methodname: str = code_type.co_name

    expected_lineno: int = 0
    with pytest.raises(Exception) as excinfo:
        expected_lineno = current_frame.f_lineno + 1  # type: ignore
        target.orElseRaise(lambda x, y: Exception(x / y), 0, 0)

    assert excinfo.errisinstance(IncompleteCallBackException)

    actual_message: str = str(excinfo.value)
    assert "division by zero" in actual_message
    assert "target.orElseRaise(lambda x, y: Exception(x / y), 0, 0)" in actual_message
    assert json.dumps(
        f"{current_filename}#{current_methodname} {expected_lineno} line"
    ) in actual_message


def test_ifPresent_case_of_passing_by_reference_value():
    test_target: TestTarget = TestTarget(3)
    nullable: Nullable[TestTarget] = Nullable[TestTarget](test_target)
    nullable.ifPresent(lambda x: x.setValue(x.getValue() * 2))

    actual: TestTarget = nullable.get()

    assert actual.getValue() == test_target.getValue()
    assert actual != test_target


def test_ifPresent_case_of_present():
    excepted: int = 8
    target: Nullable[int] = Nullable[int](3)
    callback, actual = ifPresentCallback(5)[:2]
    target.ifPresent(callback)

    assert actual() == excepted


def test_ifPresent_case_of_empty():
    excepted: int = 5
    target: Nullable[int] = Nullable[int](None)
    callback, actual = ifPresentCallback(5)[:2]
    target.ifPresent(callback)

    assert actual() == excepted


def test_ifPresent_case_of_invalid_callback():
    target: Nullable[int] = Nullable[int](3)

    current_frame = inspect.currentframe()
    code_type = current_frame.f_code  # type: ignore
    current_filename: str = code_type.co_filename
    current_methodname: str = code_type.co_name

    expected_lineno: int = 0
    with pytest.raises(Exception) as excinfo:
        expected_lineno = current_frame.f_lineno + 1  # type: ignore
        target.ifPresent("1")  # type: ignore

    assert excinfo.errisinstance(UncallableException)

    actual_message: str = str(excinfo.value)
    assert "Callback is not callable `1`" in actual_message
    assert json.dumps(
        f"{current_filename}#{current_methodname} {expected_lineno} line"
    ) in actual_message


def ifPresentCallback(val: int):

    x: int = val

    def add(y: int):
        nonlocal x
        x += y

    def get():
        return x

    def display_division(z: int):
        print(x / z)

    return add, get, display_division


def test_ifPresent_case_of_incomplete_callback():
    target: Nullable[int] = Nullable[int](0)
    display_division = ifPresentCallback(0)[2]

    current_frame = inspect.currentframe()
    code_type = current_frame.f_code  # type: ignore
    current_filename: str = code_type.co_filename
    current_methodname: str = code_type.co_name

    expected_lineno: int = 0
    with pytest.raises(Exception) as excinfo:
        expected_lineno = current_frame.f_lineno + 1  # type: ignore
        target.ifPresent(display_division)
    assert excinfo.errisinstance(IncompleteCallBackException)

    actual_message: str = str(excinfo.value)
    assert "division by zero" in actual_message
    assert "def display_division(z: int):" in actual_message
    assert json.dumps(
        f"{current_filename}#{current_methodname} {expected_lineno} line"
    ) in actual_message


def test_filter_case_of_present():
    target: Nullable[str] = Nullable[str]("1234")
    callback: Callable[[str], bool] = lambda x: x.isdigit()

    assert target.filter(extractor=callback).isPresent()


def test_filter_case_of_not_matched():
    target: Nullable[str] = Nullable[str]("abcd")
    callback: Callable[[str], bool] = lambda x: x.isdigit()

    assert target.filter(extractor=callback).isEmpty()


def test_filter_case_of_empty():
    target: Nullable[str] = Nullable[str](None)
    callback: Callable[[str], bool] = lambda x: x.isdigit()

    assert target.filter(extractor=callback).isEmpty()


def test_filter_case_of_invalid_callback():
    target: Nullable[str] = Nullable[str](None)

    current_frame = inspect.currentframe()
    code_type = current_frame.f_code  # type: ignore
    current_filename: str = code_type.co_filename
    current_methodname: str = code_type.co_name

    expected_lineno: int = 0
    with pytest.raises(Exception) as excinfo:
        expected_lineno = current_frame.f_lineno + 1  # type: ignore
        target.filter("1")  # type: ignore

    assert excinfo.errisinstance(UncallableException)

    actual_message: str = str(excinfo.value)
    assert "Callback is not callable `1`" in actual_message
    assert json.dumps(
        f"{current_filename}#{current_methodname} {expected_lineno} line"
    ) in actual_message


def test_filter_case_of_incomplete_callback():
    target: Nullable[str] = Nullable[str]("1234")

    current_frame = inspect.currentframe()
    code_type = current_frame.f_code  # type: ignore
    current_filename: str = code_type.co_filename
    current_methodname: str = code_type.co_name

    expected_lineno: int = 0
    with pytest.raises(Exception) as excinfo:
        expected_lineno = current_frame.f_lineno + 1  # type: ignore
        target.filter(lambda x: x == str(0 / 0))
    assert excinfo.errisinstance(IncompleteCallBackException)

    actual_message: str = str(excinfo.value)
    assert "division by zero" in actual_message
    assert "target.filter(lambda x: x == str(0 / 0))" in actual_message
    assert json.dumps(
        f"{current_filename}#{current_methodname} {expected_lineno} line"
    ) in actual_message


def test_map_case_of_present():
    target: Nullable[str] = Nullable[str]("1234")
    callback: Callable[[str], int] = lambda x: int(x)

    result: Nullable[int] = target.map(mapper=callback)
    assert isinstance(result, Nullable)
    actual_value = result.get()
    assert isinstance(actual_value, int)
    assert actual_value == 1234


def test_map_case_of_empty():
    target: Nullable[str] = Nullable[str](None)
    callback: Callable[[str], int] = lambda x: int(x)

    result: Nullable[int] = target.map(mapper=callback)
    assert isinstance(result, Nullable)
    assert result.isEmpty()


def test_map_case_of_invalid_callback():
    target: Nullable[str] = Nullable[str]("1234")

    current_frame = inspect.currentframe()
    code_type = current_frame.f_code  # type: ignore
    current_filename: str = code_type.co_filename
    current_methodname: str = code_type.co_name

    expected_lineno: int = 0
    with pytest.raises(Exception) as excinfo:
        expected_lineno = current_frame.f_lineno + 1  # type: ignore
        target.map("1")  # type: ignore

    assert excinfo.errisinstance(UncallableException)

    actual_message: str = str(excinfo.value)
    assert "Callback is not callable `1`" in actual_message
    assert json.dumps(
        f"{current_filename}#{current_methodname} {expected_lineno} line"
    ) in actual_message


def test_map_case_of_incomplete_callback():
    target: Nullable[str] = Nullable("1234")

    current_frame = inspect.currentframe()
    code_type = current_frame.f_code  # type: ignore
    current_filename: str = code_type.co_filename
    current_methodname: str = code_type.co_name

    expected_lineno: int = 0
    with pytest.raises(Exception) as excinfo:
        expected_lineno = current_frame.f_lineno + 1  # type: ignore
        target.map(lambda x: str(0 / 0))
    assert excinfo.errisinstance(IncompleteCallBackException)

    actual_message: str = str(excinfo.value)
    assert "division by zero" in actual_message
    assert "target.map(lambda x: str(0 / 0))" in actual_message
    assert json.dumps(
        f"{current_filename}#{current_methodname} {expected_lineno} line"
    ) in actual_message


def test_flatMap_case_of_present():
    target: Nullable[str] = Nullable[str]("1234")
    callback: Callable[[str], Nullable[int]
                       ] = lambda x: Nullable[int](int(x))

    result = target.flatMap(mapper=callback)
    assert isinstance(result, Nullable)
    actual_value = result.get()
    assert isinstance(actual_value, int)
    assert actual_value == 1234


def test_flatMap_case_of_empty():
    target: Nullable[str] = Nullable[str](None)
    callback: Callable[[str], Nullable[int]
                       ] = lambda x: Nullable[int](int(x))

    result = target.flatMap(mapper=callback)
    assert isinstance(result, Nullable)
    assert result.isEmpty()


def test_flatMap_case_of_invalid_callback():
    target: Nullable[str] = Nullable[str]("1234")

    current_frame = inspect.currentframe()
    code_type = current_frame.f_code  # type: ignore
    current_filename: str = code_type.co_filename
    current_methodname: str = code_type.co_name

    expected_lineno: int = 0
    with pytest.raises(Exception) as excinfo:
        expected_lineno = current_frame.f_lineno + 1  # type: ignore
        target.flatMap("1")  # type: ignore

    assert excinfo.errisinstance(UncallableException)

    actual_message: str = str(excinfo.value)
    assert "Callback is not callable `1`" in actual_message
    assert json.dumps(
        f"{current_filename}#{current_methodname} {expected_lineno} line"
    ) in actual_message


def test_flatMap_case_of_incomplete_callback():
    target: Nullable[str] = Nullable[str]("1234")

    current_frame = inspect.currentframe()
    code_type = current_frame.f_code  # type: ignore
    current_filename: str = code_type.co_filename
    current_methodname: str = code_type.co_name

    expected_lineno: int = 0
    with pytest.raises(Exception) as excinfo:
        expected_lineno = current_frame.f_lineno + 1  # type: ignore
        target.flatMap(lambda x: Nullable(str(0 / 0)))
    assert excinfo.errisinstance(IncompleteCallBackException)

    actual_message: str = str(excinfo.value)
    assert "division by zero" in actual_message
    assert "target.flatMap(lambda x: Nullable(str(0 / 0)))" in actual_message
    assert json.dumps(
        f"{current_filename}#{current_methodname} {expected_lineno} line"
    ) in actual_message


def test_equals_case_of_true():
    target: Nullable[str] = Nullable[str]("foo")
    comp: Nullable[str] = Nullable("foo")

    assert target.equals(comp)


def test_equals_case_of_false():
    target: Nullable[str] = Nullable[str]("foo")
    comp: Nullable[str] = Nullable("bar")

    assert not target.equals(comp)


def test_equals_case_of_other_type():
    target: Nullable[str] = Nullable[str]("1")
    comp: Nullable[int] = Nullable(1)

    assert not target.equals(comp)


def test_raise_incomplete_callback_case_of_built_in_func():
    target: Nullable[str] = Nullable[str](None)

    current_frame = inspect.currentframe()
    code_type = current_frame.f_code  # type: ignore
    current_filename: str = code_type.co_filename
    current_methodname: str = code_type.co_name

    expected_lineno: int = 0
    with pytest.raises(Exception) as excinfo:
        expected_lineno = current_frame.f_lineno + 1  # type: ignore
        target.orElseRaise(sum, ("a", "b"))  # type: ignore

    assert excinfo.errisinstance(IncompleteCallBackException)

    actual_message: str = str(excinfo.value)
    assert "unsupported operand type(s) for +: 'int' and 'str'" in actual_message
    assert "<built-in function sum>" in actual_message
    assert json.dumps(
        f"{current_filename}#{current_methodname} {expected_lineno} line"
    ) in actual_message


def test_exception_stacktrace():
    target: Nullable[str] = Nullable[str](None)

    current_frame = inspect.currentframe()
    code_type = current_frame.f_code  # type: ignore
    current_filename: str = code_type.co_filename
    current_methodname: str = code_type.co_name
    actual: Optional[IncompleteCallBackException] = None

    expected_lineno: int = 0
    try:
        expected_lineno = current_frame.f_lineno + 1  # type: ignore
        target.orElseRaise(sum, ("a", "b"))  # type: ignore
    except IncompleteCallBackException as e:
        actual = e

    assert actual is not None

    stack_trace: list[Stack] = actual.stacktrace

    test_stacktrace_stack: Stack = stack_trace[1]

    assert test_stacktrace_stack.get(
        "FileName") == current_filename

    assert test_stacktrace_stack.get(
        "FunctionName") == current_methodname

    assert test_stacktrace_stack.get(
        "LineNumber") == expected_lineno


def test_nullable_wrap_case_of_str():
    actual = return_str_optional(1)
    assert isinstance(actual, Nullable)
    assert actual.isEmpty()

    actual2 = return_str_optional(2)
    assert isinstance(actual2, Nullable)
    assert actual2.isPresent()
    assert isinstance(actual2.get(), str)


def test_nullable_wrap_case_of_str_none_union():
    actual = return_str_none_union(1)
    assert isinstance(actual, Nullable)
    assert actual.isEmpty()

    actual2 = return_str_none_union(2)
    assert isinstance(actual2, Nullable)
    assert actual2.isPresent()
    assert isinstance(actual2.get(), str)


@nullable_wrap
def return_str_optional(val: int) -> Optional[str]:
    if val % 2 == 0:
        return str(val)
    else:
        return None


@nullable_wrap
def return_str_none_union(val: int) -> Union[str, None]:
    if val % 2 == 0:
        return str(val)
    else:
        return None


def test_nullable_immutable():
    nullable: Nullable[str] = Nullable[str]("foo")
    with pytest.raises(Exception) as excinfo:
        nullable.__val = "bar"  # type: ignore

    assert excinfo.errisinstance(NotImplementedError)
    assert nullable.get() == "foo"
