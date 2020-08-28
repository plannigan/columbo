"""Type aliases used by the public API"""

from typing import Callable, List, Mapping, MutableMapping, Optional, TypeVar, Union

Answer = Union[bool, str]
Answers = Mapping[str, Answer]
MutableAnswers = MutableMapping[str, Answer]
OptionList = List[str]
V = TypeVar("V")
StaticOrDynamicValue = Union[V, Callable[[Answers], V]]
ShouldAsk = Callable[[Answers], bool]
Validator = Callable[[str, Answers], Optional[str]]
