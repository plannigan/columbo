import re
import sys
from abc import ABC, abstractmethod
from enum import Enum
from typing import Collection, Generic, Mapping, Optional, Type, TypeVar, Union, cast

from columbo import _user_io as user_io
from columbo._exception import DuplicateQuestionNameException
from columbo._types import (
    Answer,
    Answers,
    MutableAnswers,
    Options,
    ShouldAsk,
    StaticOrDynamicValue,
    V,
    ValidationFailure,
    ValidationResponse,
    ValidationSuccess,
    Validator,
)

if sys.version_info < (3, 10):
    from typing_extensions import TypeGuard
else:
    from typing import TypeGuard

QuestionValue = TypeVar("QuestionValue", str, bool)
# Explicitly list each possible question value to prevent making the type alias generic
Interaction = Union["Displayable", "Question[bool]", "Question[str]"]


# Used by copy() implementations. Since some arguments can be None, None can't be used as the value to indicate that the
# argument was not given.
class _Sentinel(Enum):
    A = 0


T = TypeVar("T")
_NOT_GIVEN = _Sentinel.A
Possible = Union[T, _Sentinel]


# The type of value is Possible[T]. object is used because of a conflict when T is a union. The type system flattens
# unions of unions. This causes the type system to infer that T is object instead of the nested union type.
def _or_default(value: object, default: T) -> T:
    return default if isinstance(value, _Sentinel) else cast(T, value)


def _should_ask_or_display(should_ask: Optional[ShouldAsk], answers: Answers) -> bool:
    if should_ask is None:
        return True
    if callable(should_ask):
        return should_ask(answers)
    raise ValueError(f"Invalid value for should_ask: {should_ask}")


class Displayable(ABC):
    """
    Base class for a message to the user that is displayed.
    """

    def __init__(
        self, message: StaticOrDynamicValue[str], should_ask: Optional[ShouldAsk] = None
    ) -> None:
        """
        Initialize an instance.

        :param message: The message to be displayed to the user. If the value is callable, the argument passed in will
            be the answers that have been provided this far.
        :param should_ask: If `None`, the message is displayed to the user. Otherwise, the callable will be passed the
            answers that have been provided this far and should return `True` if the message should be displayed.
        """
        self._message = message
        self._should_ask = should_ask

    @abstractmethod
    def display(
        self, answers: Answers, no_user_input: bool = False
    ) -> None:  # pragma: no cover
        """
        Display a message to the user.

        :param answers: The answers that have been provided this far.
        :param no_user_input: If `True` the message will be displayed without waiting for the user to interact.
            Default: `False`
        """
        pass

    def should_ask(self, answers: Answers) -> bool:
        """
        Should the user be displayed this message.

        :param answers: The answers that have been provided this far.
        :return: `True` if this message should be displayed
        :raises ValueError: The value for `should_ask` did not have the correct type.
        """
        return _should_ask_or_display(self._should_ask, answers)


class Echo(Displayable):
    """Display a message to the user."""

    def __init__(
        self, message: StaticOrDynamicValue[str], should_ask: Optional[ShouldAsk] = None
    ) -> None:
        """
        Initialize an instance.

        :param message: The message to be displayed to the user. If the value is callable, the argument passed in will
            be the answers that have been provided this far.
        :param should_ask: If `None`, the message is displayed to the user. Otherwise, the callable will be passed the
            answers that have been provided this far and should return `True` if the message should be displayed.
        """
        super().__init__(message, should_ask)

    def display(self, answers: Answers, no_user_input: bool = False) -> None:
        """
        Display a message to the user.

        :param answers: The answers that have been provided this far.
        :param no_user_input: Has no effect because no user input is expected. Default: `False`
        :raises ValueError: The value for `message` did not have the correct type.
        """
        user_io.echo(to_value(self._message, answers, str))

    def copy(
        self,
        *,
        message: Possible[StaticOrDynamicValue[str]] = _NOT_GIVEN,
        should_ask: Possible[Optional[ShouldAsk]] = _NOT_GIVEN,
    ) -> "Echo":
        """
        Create a new instance like this one, potentially with different values.

        :param message: The message to be displayed to the user. If the value is callable, the argument passed in will
            be the answers that have been provided this far.
        :param should_ask: If `None`, the message is displayed. Otherwise, the callable will be passed the answers that
            have been provided this far and should return `True` if the message should be displayed.
        :return: A newly constructed instance with the given values in place of the values of this instance.
        """
        return Echo(
            _or_default(message, self._message),
            should_ask=_or_default(should_ask, self._should_ask),
        )


class Acknowledge(Displayable):
    """Display a message to the user and require the user to press ENTER to continue."""

    def __init__(
        self, message: StaticOrDynamicValue[str], should_ask: Optional[ShouldAsk] = None
    ) -> None:
        """
        Initialize an instance.

        :param message: The message to be displayed to the user. If the value is callable, the argument passed in will
            be the answers that have been provided this far.
        :param should_ask: If `None`, the message is displayed to the user. Otherwise, the callable will be passed the
            answers that have been provided this far and should return `True` if the message should be displayed.
        """
        super().__init__(message, should_ask)

    def display(self, answers: Answers, no_user_input: bool = False) -> None:
        """
        Display a message to the user and require the user to press ENTER to continue

        :param answers: The answers that have been provided this far.
        :param no_user_input: If `True` the message will be displayed without waiting for the user to interact.
            Default: `False`
        :raises ValueError: The value for `message` did not have the correct type.
        """
        user_io.acknowledge(
            to_value(self._message, answers, str), no_user_input=no_user_input
        )

    def copy(
        self,
        *,
        message: Possible[StaticOrDynamicValue[str]] = _NOT_GIVEN,
        should_ask: Possible[Optional[ShouldAsk]] = _NOT_GIVEN,
    ) -> "Acknowledge":
        """
        Create a new instance like this one, potentially with different values.

        :param message: The message to be displayed to the user. If the value is callable, the argument passed in will
            be the answers that have been provided this far.
        :param should_ask: If `None`, the message is displayed. Otherwise, the callable will be passed the answers that
            have been provided this far and should return `True` if the message should be displayed.
        :return: A newly constructed instance with the given values in place of the values of this instance.
        """
        return Acknowledge(
            _or_default(message, self._message),
            should_ask=_or_default(should_ask, self._should_ask),
        )


class Question(ABC, Generic[QuestionValue]):
    """
    Base class for a prompt to the user that produces an answer.
    """

    def __init__(
        self,
        name: str,
        message: StaticOrDynamicValue[str],
        cli_help: Optional[str] = None,
        should_ask: Optional[ShouldAsk] = None,
        value_if_not_asked: Optional[QuestionValue] = None,
    ) -> None:
        """
        Initialize an instance.

        :param name: The identifier that will be used as the key to access this question's answer.
        :param message: The message to be displayed to the user. If the value is callable, the argument passed in will
            be the answers that have been provided this far.
        :param cli_help: Optional help message to be displayed for command line interface.
        :param should_ask: If `None`, the question is asked. Otherwise, the callable will be passed the answers that
            have been provided this far and should return `True` if the question should be asked.
        :param value_if_not_asked: If provided and if should_ask is being used, this value will be recorded as an answer
            if should_ask evaluates to False.
        :raises ValueError: A value for `value_if_not_asked` was given without giving a value for `should_ask`.
        """
        self._name = name
        self._message = message
        self._cli_help = cli_help

        if value_if_not_asked is not None and should_ask is None:
            raise ValueError(
                "You provided a value_if_not_asked but not should_ask. "
                "You should either remove value_if_not_asked or add should_ask."
            )

        self._should_ask = should_ask
        self._value_if_not_asked: Optional[QuestionValue] = value_if_not_asked

    @property
    def name(self) -> str:
        return self._name

    @property
    def cli_help(self) -> Optional[str]:
        return self._cli_help

    @property
    def value_if_not_asked(self) -> Optional[QuestionValue]:
        return self._value_if_not_asked

    @abstractmethod
    def ask(
        self, answers: Answers, no_user_input: bool = False
    ) -> Answer:  # pragma: no cover
        """
        Prompt the user with this question.

        :param answers: The answers that have been provided this far.
        :param no_user_input: If `True` the default value for the question will be used without waiting for the user
            to provide an answer. Default: `False`
        :return: The answer to the question.
        """
        pass

    def should_ask(self, answers: Answers) -> bool:
        """
        Should the user be asked this question.

        :param answers: The answers that have been provided this far.
        :return: `True` if this questions should be asked
        :raises ValueError: The value for `should_ask` did not have the correct type.
        """
        return _should_ask_or_display(self._should_ask, answers)


class Confirm(Question[bool]):
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
        value_if_not_asked: Optional[bool] = None,
    ) -> None:
        """
        Initialize an instance.

        :param name: The identifier that will be used as the key to access this question's answer.
        :param message: The message to be displayed to the user. If the value is callable, the argument passed in will
            be the answers that have been provided this far.
        :param default: The default answer to the question. If the value is callable, the argument passed in will be the
            answers that have been provided this far.
        :param cli_help: Optional help message to be displayed for command line interface.
        :param should_ask: If `None`, the question is asked. Otherwise, the callable will be passed the answers that
            have been provided this far and should return `True` if the question should be asked.
        :param value_if_not_asked: If provided and if should_ask is being used, this value will be recorded as an answer
            if should_ask evaluates to False.
        :raises ValueError: A value for `value_if_not_asked` was given without giving a value for `should_ask` or the
            value for `value_if_not_asked` is not a `bool`.
        """
        if value_if_not_asked is not None and not isinstance(value_if_not_asked, bool):
            raise ValueError("value_if_not_asked must be a bool")
        super().__init__(
            name,
            message,
            cli_help=cli_help,
            should_ask=should_ask,
            value_if_not_asked=value_if_not_asked,
        )
        self._default = default

    @property
    def default(self) -> StaticOrDynamicValue[bool]:
        return self._default

    def ask(self, answers: Answers, no_user_input: bool = False) -> bool:
        """
        Prompt the user with this question.

        :param answers: The answers that have been provided this far.
        :param no_user_input: If `True` the default value for the question will be used without waiting for the user
            to provide an answer. Default: `False`
        :return: The answer to the question.
        :raises ValueError: The instance was misconfigured in some way.
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
        value_if_not_asked: Possible[Optional[bool]] = _NOT_GIVEN,
    ) -> "Confirm":
        """
        Create a new instance like this one, potentially with different values.

        :param name: The identifier that will be used as the key to access this question's answer.
        :param message: The message to be displayed to the user. If the value is callable, the argument passed in will
            be the answers that have been provided this far.
        :param default: The default answer to the question. If the value is callable, the argument passed in will be the
            answers that have been provided this far.
        :param cli_help: Optional help message to be displayed for command line interface.
        :param should_ask: If `None`, the question is asked. Otherwise, the callable will be passed the answers that
            have been provided this far and should return `True` if the question should be asked.
        :param value_if_not_asked: If provided and if should_ask is being used, this value will be recorded as an answer
            if should_ask evaluates to False.
        :return: A newly constructed instance with the given values in place of the values of this instance.
        """
        return Confirm(
            _or_default(name, self._name),
            _or_default(message, self._message),
            default=_or_default(default, self._default),
            cli_help=_or_default(cli_help, self._cli_help),
            should_ask=_or_default(should_ask, self._should_ask),
            value_if_not_asked=_or_default(
                value_if_not_asked, self._value_if_not_asked
            ),
        )


class Choice(Question[str]):
    """
    A question with a set of possible answers.
    """

    def __init__(
        self,
        name: str,
        message: StaticOrDynamicValue[str],
        options: StaticOrDynamicValue[Options],
        default: StaticOrDynamicValue[str],
        cli_help: Optional[str] = None,
        should_ask: Optional[ShouldAsk] = None,
        value_if_not_asked: Optional[str] = None,
    ) -> None:
        """
        Initialize an instance.

        :param name: The identifier that will be used as the key to access this question's answer.
        :param message: The message to be displayed to the user. If the value is callable, the argument passed in will
            be the answers that have been provided this far.
        :param options: The set of possible answers to the question. If the value is callable, the argument passed in
            will be the answers that have been provided this far. If the value is a `Mapping`, the values of the mapping
            will be displayed to the user & the respective key will be the returned value.
        :param default: The default answer to the question. If the value is callable, the argument passed in will be the
            answers that have been provided this far.
        :param cli_help: Optional help message to be displayed for command line interface.
        :param should_ask: If `None`, the question is asked. Otherwise, the callable will be passed the answers that
            have been provided this far and should return `True` if the question should be asked.
        :param value_if_not_asked: If provided and if should_ask is being used, this value will be recorded as an answer
            if should_ask evaluates to False.
        :raises ValueError: A value for `value_if_not_asked` was given without giving a value for `should_ask`. Or the
            given value for `value_if_not_asked` was not one of the options.
        """
        super().__init__(
            name,
            message,
            cli_help=cli_help,
            should_ask=should_ask,
            value_if_not_asked=value_if_not_asked,
        )

        self._options = options
        self._default = default
        self._value_if_not_asked = value_if_not_asked

    @property
    def options(self) -> StaticOrDynamicValue[Options]:
        return self._options

    @property
    def default(self) -> StaticOrDynamicValue[str]:
        return self._default

    def validate(self, value: str, answers: Answers) -> ValidationResponse:
        """Validate the value (a new answer).

        :param value: The identifier that will be used as the key to access this question's answer.
        :param answers: The answers that have been provided this far.
        :return: A ValidationFailure or ValidationSuccess object.
        :raises ValueError: The value for `options` did not have the correct type.
        """
        options = list(to_labeled_options(self._options, answers).keys())
        if value not in options:
            return ValidationFailure(error=f"Chosen value: {value} not in options")
        return ValidationSuccess()

    def ask(self, answers: Answers, no_user_input: bool = False) -> str:
        """
        Prompt the user with this question.

        :param answers: The answers that have been provided this far.
        :param no_user_input: If `True` the default value for the question will be used without waiting for the user
            to provide an answer. Default: `False`
        :return: The answer to the question.
        :raises ValueError: The instance was misconfigured in some way.
        """
        return user_io.multiple_choice(
            to_value(self._message, answers, str),
            to_labeled_options(self._options, answers),
            default=to_value(self._default, answers, str),
            no_user_input=no_user_input,
        )

    def copy(
        self,
        *,
        name: Possible[str] = _NOT_GIVEN,
        message: Possible[StaticOrDynamicValue[str]] = _NOT_GIVEN,
        options: Possible[StaticOrDynamicValue[Options]] = _NOT_GIVEN,
        default: Possible[StaticOrDynamicValue[str]] = _NOT_GIVEN,
        cli_help: Possible[Optional[str]] = _NOT_GIVEN,
        should_ask: Possible[Optional[ShouldAsk]] = _NOT_GIVEN,
        value_if_not_asked: Possible[Optional[str]] = _NOT_GIVEN,
    ) -> "Choice":
        """
        Create a new instance like this one, potentially with different values.

        :param name: The identifier that will be used as the key to access this question's answer.
        :param message: The message to be displayed to the user. If the value is callable, the argument passed in will
            be the answers that have been provided this far.
        :param options: The set of possible answers to the question. If the value is callable, the argument passed in
            will be the answers that have been provided this far.
        :param default: The default answer to the question. If the value is callable, the argument passed in will be the
            answers that have been provided this far.
        :param cli_help: Optional help message to be displayed for command line interface.
        :param should_ask: If `None`, the question is asked. Otherwise, the callable will be passed the answers that
            have been provided this far and should return `True` if the question should be asked.
        :param value_if_not_asked: If provided and if should_ask is being used, this value will be recorded as an answer
            if should_ask evaluates to False.
        :return: A newly constructed instance with the given values in place of the values of this instance.
        """
        return Choice(
            _or_default(name, self._name),
            _or_default(message, self._message),
            _or_default(options, self._options),
            _or_default(default, self._default),
            cli_help=_or_default(cli_help, self._cli_help),
            should_ask=_or_default(should_ask, self._should_ask),
            value_if_not_asked=_or_default(
                value_if_not_asked, self._value_if_not_asked
            ),
        )


class BasicQuestion(Question[str]):
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
        value_if_not_asked: Optional[str] = None,
    ) -> None:
        """
        Initialize an instance.

        :param name: The identifier that will be used as the key to access this question's answer.
        :param message: The message to be displayed to the user. If the value is callable, the argument passed in will
            be the answers that have been provided this far.
        :param default: The default answer to the question. If the value is callable, the argument passed in will be the
            answers that have been provided this far.
        :param cli_help: Optional help message to be displayed for command line interface.
        :param should_ask: If `None`, the question is asked. Otherwise, the callable will be passed the answers that
            have been provided this far and should return `True` if the question should be asked.
        :param validator: Callable that will validate the response given by the user.
            A ValidationSuccess object indicates success and a ValidationFailure object indicates failure.
        :param value_if_not_asked: If provided and if should_ask is being used, this value will be recorded as an answer
            if should_ask evaluates to False.
        :raises ValueError: A value for `value_if_not_asked` was given without giving a value for `should_ask`.
        """
        super().__init__(
            name,
            message,
            cli_help=cli_help,
            should_ask=should_ask,
            value_if_not_asked=value_if_not_asked,
        )
        self._default = default
        self._validator = validator

    @property
    def default(self) -> StaticOrDynamicValue[str]:
        return self._default

    def validate(self, value: str, answers: Answers) -> ValidationResponse:
        """Validate the value (a new answer).

        :param value: The identifier that will be used as the key to access this question's answer.
        :param answers: The answers that have been provided this far.
        :return: A ValidationFailure or ValidationSuccess object.
        :raises ValueError: The value for `validator` was not a callable.
        """

        if self._validator is None:
            return ValidationSuccess()

        if callable(self._validator):
            return self._validator(value, answers)

        raise ValueError(f"Invalid value for validate: {self._validator}")

    def ask(self, answers: Answers, no_user_input: bool = False) -> str:
        """
        Prompt the user with this question.

        :param answers: The answers that have been provided this far.
        :param no_user_input: If `True` the default value for the question will be used without waiting for the user
            to provide an answer. Default: `False`
        :return: The answer to the question.
        :raises ValueError: Default value did not satisfy the validator. Or the instance was misconfigured in some way.
        """

        message = to_value(self._message, answers, str)
        default_value = to_value(self._default, answers, str)
        # ask question until answer is valid
        while True:
            answer = user_io.ask(
                message,
                default=default_value,
                no_user_input=no_user_input,
            )

            result = self.validate(answer, answers)
            if result.valid:
                break

            if answer == default_value:
                raise ValueError(
                    f"Default value '{default_value}' must satisfy the validator."
                )

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
        value_if_not_asked: Possible[Optional[str]] = _NOT_GIVEN,
    ) -> "BasicQuestion":
        """
        Create a new instance like this one, potentially with different values.

        :param name: The identifier that will be used as the key to access this question's answer.
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
        :param value_if_not_asked: If provided and if should_ask is being used, this value will be recorded as an answer
            if should_ask evaluates to False.
        :return: A newly constructed instance with the given values in place of the values of this instance.
        """
        return BasicQuestion(
            _or_default(name, self._name),
            _or_default(message, self._message),
            _or_default(default, self._default),
            cli_help=_or_default(cli_help, self._cli_help),
            should_ask=_or_default(should_ask, self._should_ask),
            validator=_or_default(validator, self._validator),
            value_if_not_asked=_or_default(
                value_if_not_asked, self._value_if_not_asked
            ),
        )


def to_value(
    value: StaticOrDynamicValue[V], answers: Answers, value_type: Type[V]
) -> V:
    if isinstance(value, value_type):
        return value
    if callable(value):
        result = value(answers)
        if isinstance(result, value_type):
            return result
        raise ValueError(f"Invalid dynamic value: {result}")
    raise ValueError(f"Invalid value: {value}")


def to_labeled_options(
    options: StaticOrDynamicValue[Options], answers: Answers
) -> Mapping[str, str]:
    resolved_opts = options(answers) if callable(options) else options
    if isinstance(resolved_opts, list):
        return {v: v for v in resolved_opts}
    if isinstance(resolved_opts, Mapping):
        return resolved_opts
    raise ValueError("Invalid options type")


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
        to provide an answer. Default: `False`
    :return: Dictionary of answers.
    :raises DuplicateQuestionNameException: One of the given questions attempted to reuse a name. When a value is
        provided for `answers`, those are considered as well.
    :raises ValueError: One of the given `Interaction`s was not a valid type or was misconfigured in some way.
    """
    validate_duplicate_question_names(interactions, answers)
    result = {} if answers is None else dict(answers)

    for interaction in interactions:
        if isinstance(interaction, (Echo, Acknowledge)):
            if interaction.should_ask(result):
                interaction.display(result)
        elif _is_question(interaction):
            if interaction.should_ask(result):
                result[interaction.name] = interaction.ask(result, no_user_input)
            elif interaction.value_if_not_asked is not None:
                result[interaction.name] = _validate_value_if_not_asked(
                    interaction.value_if_not_asked, interaction, result
                )
        else:
            raise ValueError(f"Unsupported interaction type: {type(interaction)}")

    return result


def _is_question(
    value: Union[Question[QuestionValue], object]
) -> TypeGuard[Question[QuestionValue]]:
    # preserve generic type information
    return isinstance(value, Question)


def _validate_value_if_not_asked(
    value_if_not_asked: QuestionValue,
    interaction: Question[QuestionValue],
    current_answers: MutableAnswers,
) -> QuestionValue:
    if isinstance(interaction, (BasicQuestion, Choice)):
        validation_result = interaction.validate(value_if_not_asked, current_answers)
        if not validation_result.valid:
            raise ValueError(f"NotAsked value is not valid: {validation_result.error}")
    return value_if_not_asked


def canonical_arg_name(name: str) -> str:
    sanitized_name = name.lower().replace(" ", "-").replace("_", "-").strip("-")
    # remove any duplicate dashes ("foo--bar" becomes "foo-bar")
    arg_name = re.sub(r"(\-)\1+", r"\1", sanitized_name)
    return f"--{arg_name}"


def validate_duplicate_question_names(
    interactions: Collection[Interaction], answers: Optional[Answers] = None
) -> None:
    """
    Ensure that multiple questions don't use the same name.

    :param interactions: Collection of interactions to check.
    :param answers: An initial dictionary of answers to treat as questions that have already been asked.
    :raises DuplicateQuestionNameException: One of the given questions attempted to reuse a name.
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
