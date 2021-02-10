from argparse import Namespace

import pytest

from columbo import (
    BasicQuestion,
    Choice,
    CliException,
    Confirm,
    DuplicateQuestionNameException,
    Echo,
    parse_args,
)
from columbo._cli import create_parser, format_cli_help, to_answers
from columbo._interaction import canonical_arg_name
from tests.sample_data import (
    DUPLICATE_QUESTION_NAME_PARAMS,
    SOME_ARG_NAME,
    SOME_BOOL,
    SOME_DEFAULT,
    SOME_INVALID_ARG_NAME,
    SOME_INVALID_OPTION,
    SOME_NAME,
    SOME_NAMESPACE,
    SOME_NON_DEFAULT_OPTION,
    SOME_OPTIONS,
    SOME_OTHER_BOOL,
    SOME_OTHER_STRING,
    SOME_STRING,
    SampleQuestion,
    some_dynamic_options,
)

invalid_cli_parameterize = pytest.mark.parametrize(
    ("description", "questions", "args"),
    [
        (
            "invalid static arg, correct arg name",
            [Choice(SOME_NAME, SOME_STRING, SOME_OPTIONS, SOME_DEFAULT)],
            [SOME_ARG_NAME, SOME_INVALID_OPTION],
        ),
        (
            "invalid dynamic arg, correct arg name",
            [Choice(SOME_NAME, SOME_STRING, some_dynamic_options, SOME_DEFAULT)],
            [SOME_ARG_NAME, SOME_INVALID_OPTION],
        ),
        (
            "invalid static arg, incorrect arg name",
            [Choice(SOME_NAME, SOME_STRING, SOME_OPTIONS, SOME_DEFAULT)],
            [SOME_INVALID_ARG_NAME, SOME_NON_DEFAULT_OPTION],
        ),
        (
            "invalid dynamic arg, incorrect arg name",
            [Choice(SOME_NAME, SOME_STRING, some_dynamic_options, SOME_DEFAULT)],
            [SOME_INVALID_ARG_NAME, SOME_NON_DEFAULT_OPTION],
        ),
    ],
)


@invalid_cli_parameterize
def test_parse_args__invalid_arg_default_exit_on_error__system_exit(
    questions, args, description
):
    with pytest.raises(SystemExit):
        parse_args(questions, args)


@invalid_cli_parameterize
def test_parse_args__invalid_arg_exit_on_error__system_exit(
    questions, args, description
):
    with pytest.raises(SystemExit):
        parse_args(questions, args)


@invalid_cli_parameterize
def test_parse_args__invalid_arg_no_exit_on_error__system_exit(
    questions, args, description
):
    with pytest.raises(CliException):
        parse_args(questions, args, exit_on_error=False)


def test_parse_args__valid_arg__answers():
    questions = [Choice(SOME_NAME, SOME_STRING, SOME_OPTIONS, SOME_DEFAULT)]

    answers = parse_args(questions, [SOME_ARG_NAME, SOME_NON_DEFAULT_OPTION])

    assert SOME_NAME in answers
    assert answers[SOME_NAME] == SOME_NON_DEFAULT_OPTION


def test_parse_args__initial_answers__answers():
    initial_key = "initial-key"
    initial_answers = {initial_key: "aa-test-bb"}
    questions = [Choice(SOME_NAME, SOME_STRING, SOME_OPTIONS, SOME_DEFAULT)]

    answers = parse_args(
        questions, [SOME_ARG_NAME, SOME_NON_DEFAULT_OPTION], answers=initial_answers
    )

    assert answers[initial_key] == initial_answers[initial_key]


@pytest.mark.parametrize("questions", DUPLICATE_QUESTION_NAME_PARAMS)
def test_parse_args__duplicate_question_name__exception(questions):
    with pytest.raises(DuplicateQuestionNameException):
        parse_args(questions)


def test_parse_args__duplicate_question_name_in_answers__exception():
    with pytest.raises(DuplicateQuestionNameException):
        parse_args(
            [BasicQuestion(SOME_NAME, SOME_STRING, SOME_DEFAULT)],
            answers={SOME_NAME: "existing value"},
        )


def test_parse_args__parser_name__name_in_result(capsys):
    try:
        parse_args(
            [Confirm(SOME_NAME, SOME_STRING)],
            [SOME_INVALID_ARG_NAME, SOME_INVALID_OPTION],
            parser_name=SOME_OTHER_STRING,
        )
    except SystemExit:
        assert SOME_OTHER_STRING in capsys.readouterr().err
    else:
        pytest.fail("System exit should have been thrown")


def test_create_parser__choice_not_given__no_value():
    parser = create_parser([Choice(SOME_NAME, SOME_STRING, SOME_OPTIONS, SOME_DEFAULT)])

    result = parser.parse_args([])

    assert vars(result)[SOME_NAME] is None


@pytest.mark.parametrize("choice", SOME_OPTIONS)
def test_create_parser__choice__choice_valid(choice):
    parser = create_parser([Choice(SOME_NAME, SOME_STRING, SOME_OPTIONS, SOME_DEFAULT)])

    result = parser.parse_args([SOME_ARG_NAME, choice])

    assert vars(result)[SOME_NAME] == choice


def test_create_parser__choice_invalid_option__exception():
    parser = create_parser([Choice(SOME_NAME, SOME_STRING, SOME_OPTIONS, SOME_DEFAULT)])

    with pytest.raises(SystemExit):
        parser.parse_args([SOME_ARG_NAME, SOME_INVALID_OPTION])


def test_create_parser__choice_dynamic_options_invalid_option__value_stored():
    # dynamic options can't be statically validated, so we store any value
    parser = create_parser(
        [Choice(SOME_NAME, SOME_STRING, some_dynamic_options, SOME_DEFAULT)]
    )

    result = parser.parse_args([SOME_ARG_NAME, SOME_INVALID_OPTION])

    assert vars(result)[SOME_NAME] == SOME_INVALID_OPTION


def test_create_parser__confirm_not_given__no_value():
    parser = create_parser([Confirm(SOME_NAME, SOME_STRING)])

    result = parser.parse_args([])

    assert vars(result)[SOME_NAME] is None


def test_create_parser__confirm_main_option__true():
    parser = create_parser([Confirm(SOME_NAME, SOME_STRING)])

    result = parser.parse_args([SOME_ARG_NAME])

    assert vars(result)[SOME_NAME] is True


def test_create_parser__confirm_no_option__false():
    parser = create_parser([Confirm(SOME_NAME, SOME_STRING)])

    result = parser.parse_args([canonical_arg_name(f"no-{SOME_NAME}")])

    assert vars(result)[SOME_NAME] is False


def test_create_parser__basic_question_not_given__no_value():
    parser = create_parser([BasicQuestion(SOME_NAME, SOME_STRING, SOME_DEFAULT)])

    result = parser.parse_args([])

    assert vars(result)[SOME_NAME] is None


def test_create_parser__basic_question__value():
    parser = create_parser([BasicQuestion(SOME_NAME, SOME_STRING, SOME_DEFAULT)])

    result = parser.parse_args([SOME_ARG_NAME, SOME_STRING])

    assert vars(result)[SOME_NAME] is SOME_STRING


def test_create_parser__unsupported_question__exception():
    with pytest.raises(ValueError):
        create_parser([SampleQuestion(SOME_NAME, SOME_STRING)])


def test_to_answer__basic_question_value_not_set__default():
    questions = [BasicQuestion(SOME_NAME, SOME_STRING, SOME_DEFAULT)]

    answers = to_answers(questions, Namespace())

    assert SOME_NAME in answers
    assert answers[SOME_NAME] == SOME_DEFAULT


def test_to_answer__basic_question_value_set__set_value():
    questions = [BasicQuestion(SOME_NAME, SOME_STRING, SOME_DEFAULT)]

    answers = to_answers(questions, Namespace(**{SOME_NAME: SOME_STRING}))

    assert SOME_NAME in answers
    assert answers[SOME_NAME] == SOME_STRING


def test_to_answer__basic_question_value_not_valid__exception():
    questions = [
        BasicQuestion(
            SOME_NAME, SOME_STRING, SOME_DEFAULT, validator=lambda v, a: "some-error"
        )
    ]

    with pytest.raises(CliException):
        with pytest.deprecated_call():
            to_answers(questions, Namespace(**{SOME_NAME: SOME_STRING}))


def test_to_answer__basic_question_dont_ask__value_not_stored():
    questions = [
        BasicQuestion(SOME_NAME, SOME_STRING, SOME_DEFAULT, should_ask=lambda _: False)
    ]

    result = to_answers(questions, Namespace(**{SOME_NAME: SOME_STRING}))

    assert SOME_NAME not in result


def test_to_answer__choice_value_not_set__default():
    questions = [Choice(SOME_NAME, SOME_STRING, SOME_OPTIONS, SOME_DEFAULT)]

    answers = to_answers(questions, Namespace())

    assert SOME_NAME in answers
    assert answers[SOME_NAME] == SOME_DEFAULT


def test_to_answer__choice_value_set__set_value():
    questions = [Choice(SOME_NAME, SOME_STRING, SOME_OPTIONS, SOME_DEFAULT)]

    answers = to_answers(questions, Namespace(**{SOME_NAME: SOME_NON_DEFAULT_OPTION}))

    assert SOME_NAME in answers
    assert answers[SOME_NAME] == SOME_NON_DEFAULT_OPTION


def test_to_answer__choice_value_not_valid__exception():
    questions = [Choice(SOME_NAME, SOME_STRING, SOME_OPTIONS, SOME_DEFAULT)]

    with pytest.raises(CliException):
        to_answers(questions, Namespace(**{SOME_NAME: SOME_STRING}))


def test_to_answer__choice_dont_ask__value_not_stored():
    questions = [
        Choice(
            SOME_NAME,
            SOME_STRING,
            SOME_OPTIONS,
            SOME_DEFAULT,
            should_ask=lambda _: False,
        )
    ]

    result = to_answers(questions, Namespace(**{SOME_NAME: SOME_STRING}))

    assert SOME_NAME not in result


def test_to_answer__confirm_value_not_set__default():
    questions = [Confirm(SOME_NAME, SOME_STRING, default=SOME_BOOL)]

    answers = to_answers(questions, Namespace())

    assert SOME_NAME in answers
    assert answers[SOME_NAME] == SOME_BOOL


def test_to_answer__confirm_value_set__set_value():
    questions = [Confirm(SOME_NAME, SOME_STRING, default=SOME_BOOL)]

    answers = to_answers(questions, Namespace(**{SOME_NAME: SOME_OTHER_BOOL}))

    assert SOME_NAME in answers
    assert answers[SOME_NAME] == SOME_OTHER_BOOL


def test_to_answer__confirm_dont_ask__value_not_stored():
    questions = [Confirm(SOME_NAME, SOME_STRING, should_ask=lambda _: False)]

    result = to_answers(questions, Namespace(**{SOME_NAME: SOME_STRING}))

    assert SOME_NAME not in result


def test_to_answer__echo__value_not_stored():
    questions = [Echo(SOME_STRING)]

    result = to_answers(questions, Namespace(**{SOME_NAME: SOME_STRING}))

    assert SOME_NAME not in result


def test_to_answer__unsupported_question__exception():
    with pytest.raises(ValueError):
        to_answers([SampleQuestion(SOME_NAME, SOME_STRING)], SOME_NAMESPACE)


@pytest.mark.parametrize(
    ["description", "questions", "partial_expected_result"],
    [
        (
            "basic question",
            [BasicQuestion(SOME_NAME, SOME_STRING, SOME_DEFAULT)],
            "--my-test-value MY-TEST-VALUE",
        ),
        (
            "choice static options, options listed",
            [Choice(SOME_NAME, SOME_STRING, SOME_OPTIONS, SOME_DEFAULT)],
            "--my-test-value {x,y,z}",
        ),
        (
            "choice dynamic options, options not listed",
            [Choice(SOME_NAME, SOME_STRING, some_dynamic_options, SOME_DEFAULT)],
            "--my-test-value MY-TEST-VALUE",
        ),
        (
            "confirm, enabled option",
            [Confirm(SOME_NAME, SOME_STRING)],
            "--my-test-value",
        ),
        (
            "confirm, disabled option",
            [Confirm(SOME_NAME, SOME_STRING)],
            "--no-my-test-value",
        ),
    ],
)
def test_format_cli_help__questions__contains_expected_result(
    questions, partial_expected_result, description
):
    result = format_cli_help(questions)

    assert partial_expected_result in result, description


def test_format_cli_help__parser_name__name_in_result():
    result = format_cli_help(
        [Confirm(SOME_NAME, SOME_STRING)], parser_name=SOME_OTHER_STRING
    )

    assert SOME_OTHER_STRING in result


@pytest.mark.parametrize("questions", DUPLICATE_QUESTION_NAME_PARAMS)
def test_format_cli_help__duplicate_question_name__exception(questions):
    with pytest.raises(DuplicateQuestionNameException):
        format_cli_help(questions)
