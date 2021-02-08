"""Type aliases used by the public API"""

from dataclasses import dataclass
from typing import (
    Callable,
    List,
    Literal,
    Mapping,
    MutableMapping,
    Optional,
    TypeVar,
    Union,
)


@dataclass
class ValidationSuccess:
    valid: Literal[True] = True


@dataclass
class ValidationFailure:
    valid: Literal[False] = False
    error: Optional[str] = None


Answer = Union[bool, str]
Answers = Mapping[str, Answer]
MutableAnswers = MutableMapping[str, Answer]
OptionList = List[str]
V = TypeVar("V")
StaticOrDynamicValue = Union[V, Callable[[Answers], V]]
ShouldAsk = Callable[[Answers], bool]
ValidationResponse = Union[ValidationSuccess, ValidationFailure]
Validator = Callable[[str, Answers], ValidationResponse]
