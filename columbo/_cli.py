"""
Produce a CLI based on a sequence of interactions.
"""

from argparse import ArgumentParser, Namespace
from functools import singledispatch
from typing import Any, Collection, Dict, NoReturn, Optional, Sequence, Union, cast

from columbo._exception import CliException
from columbo._interaction import (
    Acknowledge,
    BasicQuestion,
    Choice,
    Confirm,
    Echo,
    Interaction,
    canonical_arg_name,
    to_value,
    validate_duplicate_question_names,
)
from columbo._types import Answers, MutableAnswers

CliResult = Union[str, bool]
CliResults = Dict[str, CliResult]


def parse_args(
    interactions: Collection[Interaction],
    args: Optional[Sequence[str]] = None,
    exit_on_error: bool = True,
    answers: Optional[Answers] = None,
    parser_name: Optional[str] = None,
) -> MutableAnswers:
    """
    Parse command line argument for the given interactions.

    :param interactions: Interactions that should be turned into CLI arguments.
    :param args: Arguments to parse. If `None`, `sys.argv` will be used.
    :param exit_on_error: If `True`, print the CLI usage and exit the application. Otherwise, raise an exception with
        the error information.
    :param answers: An initial dictionary of answers to start from.
    :param parser_name: Optional name to be used in error text. If omitted, the name of the process will be used.
    :return: Answers based on the given arguments.
    :raises SystemExit: A value passed to CLI argument was not valid and `exit_on_error` was `True`.
    :raises CliException: A value passed to CLI argument was not valid and `exit_on_error` was `False`.
    :raises DuplicateQuestionNameException: One of the given questions attempts to reuse a name. This includes a
        question that was used to create `answers` if given.
    """
    validate_duplicate_question_names(interactions, answers)
    parser = create_parser(interactions, parser_name)

    if not exit_on_error:
        _patch_parser_error(parser)

    result = parser.parse_args(args)
    try:
        return to_answers(interactions, result, answers)
    except CliException as ex:
        if exit_on_error:
            parser.error(str(ex))
        else:
            raise


def format_cli_help(
    interactions: Collection[Interaction], parser_name: Optional[str] = None
) -> str:
    """
    Produce CLI help text for a given set of interactions.

    :param interactions: Interactions that should be turned into CLI arguments.
    :param parser_name: Optional name to be used in help text. If omitted, the name of the process will be used.
    :raises DuplicateQuestionNameException: One of the given questions attempts to reuse a name.
    """
    validate_duplicate_question_names(interactions)
    return create_parser(interactions, parser_name).format_help()


def create_parser(
    interactions: Collection[Interaction], parser_name: Optional[str] = None
) -> ArgumentParser:
    parser = ArgumentParser(prog=parser_name, add_help=False)
    for interaction in interactions:
        _add_argument_for(interaction, parser)

    return parser


def _patch_parser_error(parser: ArgumentParser) -> None:
    """
    Patch the error method to raise a CliException instead of printing the usage & exiting the application.

    It is safe to just patch error() because the only things that call exit() are the help and version actions, which
    aren't added.

    :param parser: Parser to be patched.
    """

    def _raise_instead(message: str) -> NoReturn:
        raise CliException(message)

    parser.error = _raise_instead  # type: ignore


@singledispatch
def _add_argument_for(question: Any, _: ArgumentParser) -> None:
    raise ValueError(f"Unsupported interaction type {type(question)}")


@_add_argument_for.register(Acknowledge)
@_add_argument_for.register(Echo)
def _add_argument_for_noop(question, parser: ArgumentParser) -> None:
    pass


@_add_argument_for.register(BasicQuestion)
def _add_argument_for_basic(question: BasicQuestion, parser: ArgumentParser) -> None:
    _add_argument(parser, question.name, question.cli_help)


@_add_argument_for.register(Confirm)
def _add_argument_for_confirm(question: Confirm, parser: ArgumentParser) -> None:
    _add_flag(parser, question.name, question.cli_help, active=True)
    _add_flag(parser, question.name, question.cli_help, active=False)


@_add_argument_for.register(Choice)
def _add_argument_for_choice(question: Choice, parser: ArgumentParser) -> None:
    options = question.options
    _add_argument(
        parser,
        question.name,
        question.cli_help,
        # For dynamic options we don't restrict the values in the CLI.
        # Conflicts will be rejected when processing the results.
        choices=None if callable(options) else options,
    )


def to_answers(
    interactions: Collection[Interaction],
    result: Namespace,
    answers: Optional[Answers] = None,
) -> MutableAnswers:
    cli_values: CliResults = vars(result)
    resultant_answers = {} if answers is None else dict(answers)

    for interaction in interactions:
        _update_answers(interaction, cli_values, resultant_answers)

    return resultant_answers


@singledispatch
def _update_answers(
    question: Any, cli_values: CliResults, answers: MutableAnswers
) -> None:
    raise ValueError(f"Unsupported interaction type {type(question)}")


@_update_answers.register(Acknowledge)
@_update_answers.register(Echo)
def _update_answers_noop(
    question, cli_values: CliResults, answers: MutableAnswers
) -> None:
    pass


@_update_answers.register(BasicQuestion)
@_update_answers.register(Choice)
def _update_answers_validate(
    question: Union[BasicQuestion, Choice],
    cli_values: CliResults,
    answers: MutableAnswers,
) -> None:
    if not question.should_ask(answers):
        return
    value = cast(str, cli_values.get(question.name))
    if value is None:
        value = to_value(question.default, answers, str)
    result = question.validate(value, answers)
    if not result.valid:
        raise CliException.invalid_value(
            value, canonical_arg_name(question.name), result.error
        )
    answers[question.name] = value


@_update_answers.register(Confirm)
def _update_answers_confirm(
    question: Confirm, cli_values: CliResults, answers: MutableAnswers
) -> None:
    if not question.should_ask(answers):
        return
    value = cli_values.get(question.name)
    if value is None:
        value = to_value(question.default, answers, bool)
    answers[question.name] = value


def _add_argument(
    parser: ArgumentParser,
    name: str,
    cli_help: Optional[str],
    dest: Optional[str] = None,
    action: str = "store",
    **kwargs,
) -> None:
    parser.add_argument(
        canonical_arg_name(name),
        action=action,
        dest=dest or name,
        help=cli_help,
        **kwargs,
    )


def _add_flag(
    parser: ArgumentParser,
    name: str,
    cli_help: Optional[str],
    active: bool = True,
    **kwargs,
) -> None:
    # store_const is used for boolean values because store_true/store_false automatically set a default for the
    # argument. For consistency across all args, we don't want this.
    _add_argument(
        parser,
        name if active else f"no-{name}",
        cli_help,
        dest=name,
        action="store_const",
        const=active,
        **kwargs,
    )
