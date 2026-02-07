"""Type aliases used by the public API"""

from collections.abc import Callable, Mapping, MutableMapping
from dataclasses import dataclass
from typing import Literal, TypeVar, Union


@dataclass
class ValidationSuccess:
    valid: Literal[True] = True


@dataclass
class ValidationFailure:
    error: str
    valid: Literal[False] = False


Answer = bool | str
Answers = Mapping[str, Answer]
MutableAnswers = MutableMapping[str, Answer]
OptionList = list[str]
Options = list[str] | Mapping[str, str]
V = TypeVar("V")
StaticOrDynamicValue = Union[V, Callable[[Answers], V]]
ShouldAsk = Callable[[Answers], bool]
ValidationResponse = ValidationSuccess | ValidationFailure
Validator = Callable[[str, Answers], ValidationResponse]
