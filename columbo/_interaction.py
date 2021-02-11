import re
import warnings
from abc import ABC, abstractmethod
from enum import Enum
from typing import Collection, Optional, Type, TypeVar, Union

from columbo import _user_io as user_io
from columbo._exception import DuplicateQuestionNameException
from columbo._types import (
    Answer,
    Answers,
    MutableAnswers,
    OptionList,
    ShouldAsk,
    StaticOrDynamicValue,
    V,
    ValidationFailure,
    ValidationResponse,
    ValidationSuccess,
    Validator,
)

Interaction = Union["Echo", "Acknowledge", "Question"]


# Used by copy() implementations. Since some arguments can be None, None can't be used as the value to indicate that the
# the argument was not given.
class _Sentinel(Enum):
    A = 0


T = TypeVar("T")
_NOT_GIVEN = _Sentinel.A
Possible = Union[T, _Sentinel]

VALIDATOR_UPGRADE_DOCS_LINK = "https://wayfair-incubator.github.io/columbo/0.10.0/usage-guide/validators/#upgrading-validator-structure"


# value is Possible[T]. The type is explicitly not annotated because of a conflict when T is a union. The type system
# flattens unions of unions. This causes the type system to infer that T is object instead of the nested union type.
def _or_default(value, default: T) -> T:
    return default if isinstance(value, _Sentinel) else value


class Echo:
    """Display a message to the user."""

    def __init__(self, message: StaticOrDynamicValue[str]) -> None:
        """
        Initialize an instance.

        :param message: The message to be displayed to the user. If the value is callable, the argument passed in will
            be the answers that have been provided this far.
        """
        self._message = message

    def display(self, answers: Answers) -> None:
        user_io.echo(to_value(self._message, answers, str))

    def copy(
        self, *, message: Possible[StaticOrDynamicValue[str]] = _NOT_GIVEN
    ) -> "Echo":
        """
        Create a new instance like this one, potentially with different values.

        :param message: The message to be displayed to the user. If the value is callable, the argument passed in will
            be the answers that have been provided this far.
        :return: A newly constructed instance with the given values in place of the values of this instance.
        """
        return Echo(_or_default(message, self._message))


class Acknowledge:
    """Display a message to the user and require the user to press ENTER to continue."""

    def __init__(self, message: StaticOrDynamicValue[str]) -> None:
        """
        Initialize an instance.

        :param message: The message to be displayed to the user. If the value is callable, the argument passed in will
            be the answers that have been provided this far.
        """
        self._message = message

    def display(self, answers: Answers) -> None:
        user_io.acknowledge(to_value(self._message, answers, str))

    def copy(
        self, *, message: Possible[StaticOrDynamicValue[str]] = _NOT_GIVEN
    ) -> "Acknowledge":
        """
        Create a new instance like this one, potentially with different values.

        :param message: The message to be displayed to the user. If the value is callable, the argument passed in will
            be the answers that have been provided this far.
        :return: A newly constructed instance with the given values in place of the values of this instance.
        """
        return Acknowledge(_or_default(message, self._message))


class Question(ABC):
    """
    Base class for a prompt to the user that produces an answer.
    """

    def __init__(
        self,
        name: str,
        message: StaticOrDynamicValue[str],
        cli_help: Optional[str] = None,
        should_ask: Optional[ShouldAsk] = None,
    ) -> None:
        """
        Initialize an instance.

        :param name: The identifier that will be used as the key to access the this question's answer.
        :param message: The message to be displayed to the user. If the value is callable, the argument passed in will
            be the answers that have been provided this far.
        :param cli_help: Optional help message to be displayed for command line interface.
        :param should_ask: If `None`, the question is asked. Otherwise, the callable will be passed the answers that
            have been provided this far and should return `True` if the question should be asked.
        """
        self._name = name
        self._message = message
        self._cli_help = cli_help
        self._should_ask = should_ask

    @property
    def name(self) -> str:
        return self._name

    @property
    def cli_help(self) -> Optional[str]:
        return self._cli_help

    @abstractmethod
    def ask(self, answers: Answers, no_user_input: bool = False) -> Answer:
        """
        Prompt the user with this question.

        :param answers: The answers that have been provided this far.
        :return: The answer to the question.
        :param no_user_input: If `True` the default value for the question will be used without waiting for the user
            to provide an answer. Default: False
        :return: The answer to the question.
        """
        pass

    def should_ask(self, answers: Answers) -> bool:
        """
        Should the user be asked this question.

        :param answers: The answers that have been provided this far.
        :return: `True` if this questions should be asked
        """
        if self._should_ask is None:
            return True
        if callable(self._should_ask):
            return self._should_ask(answers)
        raise ValueError(f"Invalid value for should_ask: {self._should_ask}")


class Confirm(Question):
    """
    A question with a yes or no answer.
    """

    def __init__(
        self,
        name: str,
        message: StaticOrDynamicValue[str],
        default: StaticOrDynamicValue[bool] = False,
        cli_help: Optional[str] = None,
        should_ask: Optional[ShouldAsk] = None,
    ) -> None:
        """
        Initialize an instance.

        :param name: The identifier that will be used as the key to access the this question's answer.
        :param message: The message to be displayed to the user. If the value is callable, the argument passed in will
            be the answers that have been provided this far.
        :param default: The default answer to the question. If the value is callable, the argument passed in will be the
            answers that have been provided this far.
        :param cli_help: Optional help message to be displayed for command line interface.
        :param should_ask: If `None`, the question is asked. Otherwise, the callable will be passed the answers that
            have been provided this far and should return `True` if the question should be asked.
        """
        super().__init__(name, message, cli_help, should_ask)
        self._default = default

    @property
    def default(self) -> StaticOrDynamicValue[bool]:
        return self._default

    def ask(self, answers: Answers, no_user_input: bool = False) -> bool:
        """
        Prompt the user with this question.

        :param answers: The answers that have been provided this far.
        :param no_user_input: If `True` the default value for the question will be used without waiting for the user
            to provide an answer. Default: False
        :return: The answer to the question.
        """
        return user_io.confirm(
            to_value(self._message, answers, str),
            default=to_value(self._default, answers, bool),
            no_user_input=no_user_input,
        )

    def copy(
        self,
        *,
        name: Possible[str] = _NOT_GIVEN,
        message: Possible[StaticOrDynamicValue[str]] = _NOT_GIVEN,
        default: Possible[StaticOrDynamicValue[bool]] = _NOT_GIVEN,
        cli_help: Possible[Optional[str]] = _NOT_GIVEN,
        should_ask: Possible[Optional[ShouldAsk]] = _NOT_GIVEN,
    ) -> "Confirm":
        """
        Create a new instance like this one, potentially with different values.

        :param name: The identifier that will be used as the key to access the this question's answer.
        :param message: The message to be displayed to the user. If the value is callable, the argument passed in will
            be the answers that have been provided this far.
        :param default: The default answer to the question. If the value is callable, the argument passed in will be the
            answers that have been provided this far.
        :param cli_help: Optional help message to be displayed for command line interface.
        :param should_ask: If `None`, the question is asked. Otherwise, the callable will be passed the answers that
            have been provided this far and should return `True` if the question should be asked.
        :return: A newly constructed instance with the given values in place of the values of this instance.
        """
        return Confirm(
            _or_default(name, self._name),
            _or_default(message, self._message),
            _or_default(default, self._default),
            _or_default(cli_help, self._cli_help),
            _or_default(should_ask, self._should_ask),
        )


class Choice(Question):
    """
    A question with a set of possible answers.
    """

    def __init__(
        self,
        name: str,
        message: StaticOrDynamicValue[str],
        options: StaticOrDynamicValue[OptionList],
        default: StaticOrDynamicValue[str],
        cli_help: Optional[str] = None,
        should_ask: Optional[ShouldAsk] = None,
    ) -> None:
        """
        Initialize an instance.

        :param name: The identifier that will be used as the key to access the this question's answer.
        :param message: The message to be displayed to the user. If the value is callable, the argument passed in will
            be the answers that have been provided this far.
        :param options: The set of possible answers to the question. If the value is callable, the argument passed in
            will be the answers that have been provided this far.
        :param default: The default answer to the question. If the value is callable, the argument passed in will be the
            answers that have been provided this far.
        :param cli_help: Optional help message to be displayed for command line interface.
        :param should_ask: If `None`, the question is asked. Otherwise, the callable will be passed the answers that
            have been provided this far and should return `True` if the question should be asked.
        """
        super().__init__(name, message, cli_help, should_ask)
        self._options = options
        self._default = default

    @property
    def options(self) -> StaticOrDynamicValue[OptionList]:
        return self._options

    @property
    def default(self) -> StaticOrDynamicValue[str]:
        return self._default

    def validate(self, value: str, answers: Answers) -> ValidationResponse:
        """Validate the value (a new answer).

        :param value: The identifier that will be used as the key to access the this question's answer.
        :param answers: The answers that have been provided this far.
        :return: A ValidationFailure or ValidationSuccess object.
        """
        options = to_value(self._options, answers, list)
        if value not in options:
            return ValidationFailure(error=f"Chosen value: {value} not in options")
        return ValidationSuccess()

    def ask(self, answers: Answers, no_user_input: bool = False) -> str:
        """
        Prompt the user with this question.

        :param answers: The answers that have been provided this far.
        :param no_user_input: If `True` the default value for the question will be used without waiting for the user
            to provide an answer. Default: False
        :return: The answer to the question.
        """
        return user_io.multiple_choice(
            to_value(self._message, answers, str),
            to_value(self._options, answers, list),
            default=to_value(self._default, answers, str),
            no_user_input=no_user_input,
        )

    def copy(
        self,
        *,
        name: Possible[str] = _NOT_GIVEN,
        message: Possible[StaticOrDynamicValue[str]] = _NOT_GIVEN,
        options: Possible[StaticOrDynamicValue[OptionList]] = _NOT_GIVEN,
        default: Possible[StaticOrDynamicValue[str]] = _NOT_GIVEN,
        cli_help: Possible[Optional[str]] = _NOT_GIVEN,
        should_ask: Possible[Optional[ShouldAsk]] = _NOT_GIVEN,
    ) -> "Choice":
        """
        Create a new instance like this one, potentially with different values.

        :param name: The identifier that will be used as the key to access the this question's answer.
        :param message: The message to be displayed to the user. If the value is callable, the argument passed in will
            be the answers that have been provided this far.
        :param options: The set of possible answers to the question. If the value is callable, the argument passed in
            will be the answers that have been provided this far.
        :param default: The default answer to the question. If the value is callable, the argument passed in will be the
            answers that have been provided this far.
        :param cli_help: Optional help message to be displayed for command line interface.
        :param should_ask: If `None`, the question is asked. Otherwise, the callable will be passed the answers that
            have been provided this far and should return `True` if the question should be asked.
        :return: A newly constructed instance with the given values in place of the values of this instance.
        """
        return Choice(
            _or_default(name, self._name),
            _or_default(message, self._message),
            _or_default(options, self._options),
            _or_default(default, self._default),
            _or_default(cli_help, self._cli_help),
            _or_default(should_ask, self._should_ask),
        )


class BasicQuestion(Question):
    """
    A question with an arbitrary text answer.
    """

    def __init__(
        self,
        name: str,
        message: StaticOrDynamicValue[str],
        default: StaticOrDynamicValue[str],
        cli_help: Optional[str] = None,
        should_ask: Optional[ShouldAsk] = None,
        validator: Optional[Validator] = None,
    ) -> None:
        """
        Initialize an instance.

        :param name: The identifier that will be used as the key to access the this question's answer.
        :param message: The message to be displayed to the user. If the value is callable, the argument passed in will
            be the answers that have been provided this far.
        :param default: The default answer to the question. If the value is callable, the argument passed in will be the
            answers that have been provided this far.
        :param cli_help: Optional help message to be displayed for command line interface.
        :param should_ask: If `None`, the question is asked. Otherwise, the callable will be passed the answers that
            have been provided this far and should return `True` if the question should be asked.
        :param validator: Callable that will validate the response given by the user.
            A ValidationSuccess object indicates success and a ValidationFailure object indicates failure.
        """
        super().__init__(name, message, cli_help, should_ask)
        self._default = default
        self._validator = validator

    @property
    def default(self) -> StaticOrDynamicValue[str]:
        return self._default

    def validate(self, value: str, answers: Answers) -> ValidationResponse:
        """Validate the value (a new answer).

        :param value: The identifier that will be used as the key to access the this question's answer.
        :param answers: The answers that have been provided this far.
        :return: A ValidationFailure or ValidationSuccess object.
        """
        if self._validator is None:
            return ValidationSuccess()
        if callable(self._validator):
            result = self._validator(value, answers)
            if isinstance(result, (ValidationFailure, ValidationSuccess)):
                return result
            else:  # handle deprecated, legacy validator responses
                warnings.warn(
                    f"You are using a validator {self._validator} that returns content in a way is deprecated and will be removed after the 1.0.0 release."
                    + f"For information on how to upgrade, please refer to the documentation here: {VALIDATOR_UPGRADE_DOCS_LINK}",
                    DeprecationWarning,
                )
                if result:
                    return ValidationFailure(error=result)
                return ValidationSuccess()
        raise ValueError(f"Invalid value for validate: {self._validator}")

    def ask(self, answers: Answers, no_user_input: bool = False) -> str:
        """
        Prompt the user with this question.

        :param answers: The answers that have been provided this far.
        :param no_user_input: If `True` the default value for the question will be used without waiting for the user
            to provide an answer. Default: False
        :return: The answer to the question.
        """

        # ask question until answer is valid
        while True:
            answer = user_io.ask(
                to_value(self._message, answers, str),
                default=to_value(self._default, answers, str),
                no_user_input=no_user_input,
            )

            result = self.validate(answer, answers)
            if result.valid:
                break

            user_io.echo(
                f"The answer you have provided is not valid:\n{result.error}\n\n"
                "We will continue asking questions until you provide a valid answer"
            )

        return answer

    def copy(
        self,
        *,
        name: Possible[str] = _NOT_GIVEN,
        message: Possible[StaticOrDynamicValue[str]] = _NOT_GIVEN,
        default: Possible[StaticOrDynamicValue[str]] = _NOT_GIVEN,
        cli_help: Possible[Optional[str]] = _NOT_GIVEN,
        should_ask: Possible[Optional[ShouldAsk]] = _NOT_GIVEN,
        validator: Possible[Optional[Validator]] = _NOT_GIVEN,
    ) -> "BasicQuestion":
        """
        Create a new instance like this one, potentially with different values.

        :param name: The identifier that will be used as the key to access the this question's answer.
        :param message: The message to be displayed to the user. If the value is callable, the argument passed in will
            be the answers that have been provided this far.
        :param default: The default answer to the question. If the value is callable, the argument passed in will be the
            answers that have been provided this far.
        :param cli_help: Optional help message to be displayed for command line interface.
        :param should_ask: If `None`, the question is asked. Otherwise, the callable will be passed the answers that
            have been provided this far and should return `True` if the question should be asked.
        :param validator: Callable that will validate the response given by the user.
            None indicates that validation was successful. Otherwise, a string containing details
            of the error that caused the validation failure.
        """
        return BasicQuestion(
            _or_default(name, self._name),
            _or_default(message, self._message),
            _or_default(default, self._default),
            _or_default(cli_help, self._cli_help),
            _or_default(should_ask, self._should_ask),
            _or_default(validator, self._validator),
        )


def to_value(
    value: StaticOrDynamicValue[V], answers: Answers, value_type: Type[V]
) -> V:
    if isinstance(value, value_type):
        return value
    if callable(value):
        return value(answers)
    raise ValueError(f"Invalid value: {value}")


def get_answers(
    interactions: Collection[Interaction],
    answers: Optional[Answers] = None,
    no_user_input: bool = False,
) -> MutableAnswers:
    """
    Iterates over collection of interactions, invoking interaction specific behavior.

    :param interactions: Collection of interactions to present the user with.
    :param answers: An initial dictionary of answers to start from.
    :param no_user_input: If `True` the default value for the question will be used without waiting for the user
        to provide an answer. Default: False
    :return: Dictionary of answers.
    :raises DuplicateQuestionNameException: One of the given questions attempts to reuse a name. This includes a
        question that was used to create `answers` if given.
    """
    validate_duplicate_question_names(interactions, answers)
    result = {} if answers is None else dict(answers)

    for interaction in interactions:
        if isinstance(interaction, (Echo, Acknowledge)):
            interaction.display(result)
        elif isinstance(interaction, Question):
            if interaction.should_ask(result):
                result[interaction.name] = interaction.ask(result, no_user_input)
        else:
            raise ValueError(f"Unsupported interaction type: {type(interaction)}")

    return result


def canonical_arg_name(name: str) -> str:
    sanizized_name = name.lower().replace(" ", "-").replace("_", "-").strip("-")
    # remove any duplicate dashes ("foo--bar" becomes "foo-bar")
    arg_name = re.sub(r"(\-)\1+", r"\1", sanizized_name)
    return f"--{arg_name}"


def validate_duplicate_question_names(
    interactions: Collection[Interaction], answers: Optional[Answers] = None
) -> None:
    """
    Ensure that multiple questions don't use the same name.

    :param interactions: Collection of interactions to check.
    :param answers: An initial dictionary of answers to treat as questions that have already been asked.
    :raises DuplicateQuestionNameException: One of the given questions attempts to reuse a name.
    """
    used_names = set() if answers is None else set(answers.keys())
    for interaction in interactions:
        if isinstance(interaction, Question):
            name_variants = {interaction.name, canonical_arg_name(interaction.name)}
            if name_variants.intersection(used_names):
                raise DuplicateQuestionNameException(
                    f"{interaction.name} has already been used"
                )
            used_names.update(name_variants)
