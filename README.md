# py_nullable

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/py_nullable)](https://img.shields.io/pypi/pyversions/py_nullable)
[![PyPI version](https://badge.fury.io/py/py_nullable.svg)](https://badge.fury.io/py/py_nullable)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/miyamo2theppl/py_nullable)](https://img.shields.io/github/v/release/miyamo2theppl/py_nullable)
[![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/miyamo2theppl/py_nullable/release.yaml?event=release&logo=github%20actions)](https://github.com/miyamo2theppl/py_nullable/actions?query=workflow%3Arelease)
[![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/miyamo2theppl/15e55b51670ba3c88767f9402215e901/raw/pytest-coverage-comment.json)](https://github.com/miyamo2theppl/py_nullable/actions?query=workflow%3Atest)
[![GitHub](https://img.shields.io/github/license/miyamo2theppl/py_nullable)](https://img.shields.io/github/license/miyamo2theppl/py_nullable)

## Introduction

Python's None Wrapper, inspired by java.lang.Optional

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

### Simple usage

if you want to get value.

```python
from py_nullable import Nullable

nullable: Nullable[str] = Nullable[str]("some string")
if nullable.isPresent()
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
