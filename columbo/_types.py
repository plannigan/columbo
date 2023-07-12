"""Type aliases used by the public API"""

from dataclasses import dataclass
from typing import Callable, List, Literal, Mapping, MutableMapping, TypeVar, Union


@dataclass
class ValidationSuccess:
    valid: Literal[True] = True


@dataclass
class ValidationFailure:
    error: str
    valid: Literal[False] = False


Answer = Union[bool, str]
Answers = Mapping[str, Answer]
MutableAnswers = MutableMapping[str, Answer]
OptionList = List[str]
Options = Union[List[str], Mapping[str, str]]
V = TypeVar("V")
StaticOrDynamicValue = Union[V, Callable[[Answers], V]]
ShouldAsk = Callable[[Answers], bool]
ValidationResponse = Union[ValidationSuccess, ValidationFailure]
Validator = Callable[[str, Answers], ValidationResponse]
