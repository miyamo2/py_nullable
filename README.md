# py_nullable

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/py_nullable?logo=python&logoColor=yellow)](https://img.shields.io/pypi/pyversions/py_nullable?logo=python&logoColor=yellow)
[![PyPI](https://img.shields.io/pypi/v/py_nullable?color=blue&logo=pypi&logoColor=yellow)](https://pypi.org/project/py-nullable?latest)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/miyamo2theppl/py_nullable)](https://img.shields.io/github/v/release/miyamo2theppl/py_nullable)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/py-nullable)](https://img.shields.io/pypi/wheel/py-nullable)
[![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/miyamo2theppl/py_nullable/release.yaml?event=release&logo=github%20actions)](https://github.com/miyamo2theppl/py_nullable/actions?query=workflow%3Arelease)
[![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/miyamo2theppl/15e55b51670ba3c88767f9402215e901/raw/pytest-coverage-comment.json)](https://github.com/miyamo2theppl/py_nullable/actions?query=workflow%3Atest)
[![GitHub](https://img.shields.io/github/license/miyamo2theppl/py_nullable)](https://img.shields.io/github/license/miyamo2theppl/py_nullable)
[![Downloads](https://static.pepy.tech/personalized-badge/py-nullable?period=total&units=international_system&left_color=blue&right_color=yellow&left_text=Downloads)](https://pepy.tech/project/py-nullable)

## Introduction

Python's None Wrapper, inspired by java.util.Optional

[Document(latest version only)](https://miyamo2theppl.github.io/py_nullable/)

## Getting Started

### Installing

install from PyPI with:

```sh
python -m pip install py_nullable
```

install from source with:

```sh
git clone https://github.com/miyamo2theppl/py_nullable.git
cd py_nullable
python -m pip install .
```

### Simple Usage

if you want to get value.

```python
from py_nullable import Nullable

nullable: Nullable[str] = Nullable[str]("some string")
if nullable.isPresent():
    print(nullable.get()) # Prints some string
```

if you want to generate a new Nullable from an existing Nullable with the mapping function.

```python
from typing import Callable
from py_nullable import Nullable

nullable: Nullable[str] = Nullable[str]("1234")

callback: Callable[[str], int] = lambda x: int(x) * 2
result: Nullable[int] = nullable.map(callback)

print(result.get()) # Prints 2468
```

if you want to refactor the return value from Optional[T] to Nullable[T].

```python
from yourpackage import YourClass
from py_nullable import Nullable, nullable_wrap


in_memory_db: dict[str, YourClass] = {"A001": YourClass("foo")}


@nullable_wrap
def find_by_id(id: str) -> Optional[YourClass]:
    return in_memory_db.get(id)


nullable: Nullable[YourClass] = find_by_id("B001")
print(nullable.isEmpty()) # Prints True
```

## Contributing

### Create a feature branch

```sh
git checkout -b feature_{example}
```

### Set up your environment

```sh
python -m venv .venv
.venv/bin/activate
pip install -r dev_requirements.txt
pip install -e .
```

### Running Tests

```sh
pytest --cov py_nullable --cov-branch --cov-report=html
```
