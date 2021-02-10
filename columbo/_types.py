"""Type aliases used by the public API"""

import sys
from dataclasses import dataclass
from typing import Callable, List, Mapping, MutableMapping, Optional, TypeVar, Union

if sys.version_info < (3, 8):
    from typing_extensions import Literal  # this supports python < 3.8
else:
    from typing import Literal  # this is available in python 3.8+


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
V = TypeVar("V")
StaticOrDynamicValue = Union[V, Callable[[Answers], V]]
ShouldAsk = Callable[[Answers], bool]
ValidationResponse = Union[ValidationSuccess, ValidationFailure]
Validator = Callable[[str, Answers], Union[ValidationResponse, Optional[str]]]
