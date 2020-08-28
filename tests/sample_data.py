from argparse import Namespace

from columbo._cli import _canonical_arg_name
from columbo._interaction import BasicQuestion, Choice, Confirm, Question

SOME_BOOL = True
SOME_OTHER_BOOL = False
SOME_NAME = "my-test-value"
SOME_ARG_NAME = _canonical_arg_name(SOME_NAME)
SOME_STRING = "hello"
SOME_OTHER_STRING = "good-bye"
SOME_ANSWERS = {"a": "one", "b": "two"}
SOME_OPTIONS = ["x", "y", "z"]
SOME_DEFAULT = "x"
SOME_NON_DEFAULT_OPTION = "y"
SOME_INVALID_OPTION = "NOT_VALID_OPTION"
SOME_INVALID_ARG_NAME = "--NOT_VALID_OPTION"


def some_dynamic_string(answers):
    return f"--{answers['a']}--"


def some_dynamic_options(answers):
    return [f"--{x}--" for x in answers.values()]


def some_dynamic_default(answers):
    return f"--{answers['b']}--"


def some_dynamic_bool(_):
    return SOME_OTHER_BOOL


SOME_DYNAMIC_STRING_RESULT = "--one--"
SOME_DYNAMIC_OPTION_RESULT = ["--one--", "--two--"]
SOME_DYNAMIC_DEFAULT_RESULT = "--two--"

SOME_NAMESPACE = Namespace(**{SOME_NAME: SOME_STRING})


class SampleQuestion(Question):
    """Question class for testing base class functionality or where subclasses need specific handling"""

    def ask(self, answers, no_user_input=False):
        raise Exception("Don't call")


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
]
