from argparse import Namespace
from typing import List, Mapping, NoReturn, Optional

from columbo import Answers, ShouldAsk, ValidationFailure
from columbo._interaction import (
    BasicQuestion,
    Choice,
    Confirm,
    Displayable,
    Question,
    canonical_arg_name,
)

SOME_BOOL = True
SOME_OTHER_BOOL = False
SOME_NAME = "my-test-value"
SOME_NAME_WITH_SPACES = "my test value"
SOME_ARG_NAME = canonical_arg_name(SOME_NAME)
SOME_STRING = "hello"
SOME_OTHER_STRING = "good-bye"
SOME_ANSWERS = {"a": "one", "b": "two"}
SOME_OPTIONS = ["x", "y", "z"]
SOME_MAPPING_OPTIONS = {"x": "The Letter X", "y": "The Letter Y", "z": "The Letter Z"}
SOME_DEFAULT = "x"
SOME_NON_DEFAULT_OPTION = "y"
SOME_INVALID_OPTION = "NOT_VALID_OPTION"
SOME_INVALID_ARG_NAME = "--NOT_VALID_OPTION"
SOME_FAILURE_MESSAGE = "always fail"


def some_dynamic_string(answers: Answers) -> str:
    return f"--{answers['a']}--"


def some_dynamic_options(answers: Answers) -> List[str]:
    return [f"--{x}--" for x in answers.values()]


def some_dynamic_mapping_options(answers: Answers) -> Mapping[str, str]:
    return {f"--{x}--": f"~~{x}~~" for x in answers.values()}


def some_dynamic_default(answers: Answers) -> str:
    return f"--{answers['b']}--"


def some_dynamic_bool(_: Answers) -> bool:
    return SOME_OTHER_BOOL


def always_fail_validator(value: str, answers: Answers) -> ValidationFailure:
    return ValidationFailure(SOME_FAILURE_MESSAGE)


SOME_DYNAMIC_STRING_RESULT = "--one--"
SOME_DYNAMIC_OPTION_RESULT = ["--one--", "--two--"]
SOME_DYNAMIC_MAPPING_OPTION_RESULT = {"--one--": "~~one~~", "--two--": "~~two~~"}
SOME_DYNAMIC_DEFAULT_RESULT = "--two--"

SOME_NAMESPACE = Namespace(**{SOME_NAME: SOME_STRING})


class SampleQuestion(Question[str]):
    """Question class for testing base class functionality or where subclasses need specific handling"""

    def ask(self, answers: Answers, no_user_input: bool = False) -> NoReturn:
        raise Exception("Don't call")


class SampleDisplayable(Displayable):
    """Displayable for testing base class functionality"""

    def __init__(self, message: str, should_ask: Optional[ShouldAsk] = None) -> None:
        super().__init__(message, should_ask)
        self._display_called = False

    def display(self, answers: Answers, no_user_input: bool = False) -> None:
        self._display_called = True

    @property
    def display_called(self) -> bool:
        return self._display_called


# combination of questions that reuse the same name
DUPLICATE_QUESTION_NAME_PARAMS = [
    [
        BasicQuestion(SOME_NAME, SOME_STRING, SOME_DEFAULT),
        BasicQuestion(SOME_NAME, SOME_STRING, SOME_DEFAULT),
    ],
    [
        Choice(SOME_NAME, SOME_STRING, SOME_OPTIONS, SOME_DEFAULT),
        Choice(SOME_NAME, SOME_STRING, SOME_OPTIONS, SOME_DEFAULT),
    ],
    [Confirm(SOME_NAME, SOME_STRING), Confirm(SOME_NAME, SOME_STRING)],
    [
        BasicQuestion(SOME_NAME, SOME_STRING, SOME_DEFAULT),
        Choice(SOME_NAME, SOME_STRING, SOME_OPTIONS, SOME_DEFAULT),
    ],
    [
        BasicQuestion(SOME_NAME, SOME_STRING, SOME_DEFAULT),
        Confirm(SOME_NAME, SOME_STRING),
    ],
    [
        Choice(SOME_NAME, SOME_STRING, SOME_OPTIONS, SOME_DEFAULT),
        Confirm(SOME_NAME, SOME_STRING),
    ],
    [
        BasicQuestion(SOME_NAME, SOME_STRING, SOME_DEFAULT),
        BasicQuestion(
            SOME_NAME_WITH_SPACES, SOME_OTHER_STRING, SOME_NON_DEFAULT_OPTION
        ),
    ],
]

QUESTION_NAME_STANDARDIZATION_PARAMS = [
    ["basic name", "foo", "--foo"],
    ["name with one leading dash", "-foo", "--foo"],
    ["name with trailing dash", "foo-", "--foo"],
    ["name with trailing and leading spaces", " foo ", "--foo"],
    ["name with trailing and leading underscores", "__foo__", "--foo"],
    ["name with leading dashes", "--foo", "--foo"],
    ["name with spaces", "foo bar", "--foo-bar"],
    ["name with underscore", "foo_bar", "--foo-bar"],
    ["name with double underscore", "foo__bar", "--foo-bar"],
    ["name with double underscore", "foo__bar", "--foo-bar"],
    ["name with mixed capitalization", "Foo-Bar", "--foo-bar"],
    ["name with multiple mixed dashes", "foo--bar__baz", "--foo-bar-baz"],
]
