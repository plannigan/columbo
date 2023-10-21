import pytest

from columbo import (
    Acknowledge,
    Answers,
    BasicQuestion,
    Choice,
    Confirm,
    DuplicateQuestionNameException,
    Echo,
    Interaction,
    ValidationFailure,
    ValidationSuccess,
)
from columbo._interaction import (
    canonical_arg_name,
    get_answers,
    to_labeled_options,
    to_value,
)
from tests.sample_data import (
    DUPLICATE_QUESTION_NAME_PARAMS,
    QUESTION_NAME_STANDARDIZATION_PARAMS,
    SOME_ANSWERS,
    SOME_BOOL,
    SOME_DEFAULT,
    SOME_DYNAMIC_DEFAULT_RESULT,
    SOME_DYNAMIC_MAPPING_OPTION_RESULT,
    SOME_DYNAMIC_OPTION_RESULT,
    SOME_DYNAMIC_STRING_RESULT,
    SOME_FAILURE_MESSAGE,
    SOME_INVALID_OPTION,
    SOME_MAPPING_OPTIONS,
    SOME_NAME,
    SOME_NON_DEFAULT_OPTION,
    SOME_OPTIONS,
    SOME_OTHER_BOOL,
    SOME_STRING,
    SampleDisplayable,
    SampleQuestion,
    always_fail_validator,
    some_dynamic_bool,
    some_dynamic_default,
    some_dynamic_mapping_options,
    some_dynamic_options,
    some_dynamic_string,
)


def test_echo__static_message__echo_message(mocker):
    user_io = mocker.patch("columbo._interaction.user_io")

    Echo(SOME_STRING).display(SOME_ANSWERS)

    user_io.echo.assert_called_once_with(SOME_STRING)


def test_echo__dynamic_message__echo_dynamic_message(mocker):
    user_io = mocker.patch("columbo._interaction.user_io")

    Echo(some_dynamic_string).display(SOME_ANSWERS)

    user_io.echo.assert_called_once_with(SOME_DYNAMIC_STRING_RESULT)


def test_echo_copy__new_instance():
    original = Echo(SOME_STRING)

    copy = original.copy()

    assert copy is not original


def test_echo_copy__no_args__echo_same_message(mocker):
    user_io = mocker.patch("columbo._interaction.user_io")

    interaction = Echo(SOME_STRING)
    interaction.display(SOME_ANSWERS)

    interaction.copy().display(SOME_ANSWERS)

    calls = user_io.echo.mock_calls
    assert len(calls) == 2
    assert calls[0] == calls[1]


def test_echo_copy__diff_message__echo_diff_message(mocker):
    user_io = mocker.patch("columbo._interaction.user_io")

    Echo(some_dynamic_string).copy(message=SOME_STRING).display(SOME_ANSWERS)

    user_io.echo.assert_called_once_with(SOME_STRING)


def test_acknowledge__static_message__acknowledge_message(mocker):
    user_io = mocker.patch("columbo._interaction.user_io")

    Acknowledge(SOME_STRING).display(SOME_ANSWERS)

    user_io.acknowledge.assert_called_once_with(SOME_STRING, no_user_input=False)


def test_acknowledge__dynamic_message__acknowledge_dynamic_message(mocker):
    user_io = mocker.patch("columbo._interaction.user_io")

    Acknowledge(some_dynamic_string).display(SOME_ANSWERS)

    user_io.acknowledge.assert_called_once_with(
        SOME_DYNAMIC_STRING_RESULT, no_user_input=False
    )


def test_acknowledge__no_user_imput__acknowledge_dynamic_message(mocker):
    user_io = mocker.patch("columbo._interaction.user_io")

    Acknowledge(SOME_STRING).display(SOME_ANSWERS, no_user_input=True)

    user_io.acknowledge.assert_called_once_with(SOME_STRING, no_user_input=True)


def test_acknowledge_copy__new_instance():
    original = Acknowledge(SOME_STRING)

    copy = original.copy()

    assert copy is not original


def test_acknowledge_copy__no_args__acknowledge_same_message(mocker):
    user_io = mocker.patch("columbo._interaction.user_io")

    interaction = Acknowledge(SOME_STRING)
    interaction.display(SOME_ANSWERS)

    interaction.copy().display(SOME_ANSWERS)

    calls = user_io.acknowledge.mock_calls
    assert len(calls) == 2
    assert calls[0] == calls[1]


def test_acknowledge_copy__diff_message__acknowledge_diff_message(mocker):
    user_io = mocker.patch("columbo._interaction.user_io")

    Acknowledge(some_dynamic_string).copy(message=SOME_STRING).display(SOME_ANSWERS)

    user_io.acknowledge.assert_called_once_with(SOME_STRING, no_user_input=False)


def test_choice__no_input__default_value():
    result = Choice(SOME_NAME, SOME_STRING, SOME_OPTIONS, SOME_DEFAULT).ask(
        SOME_ANSWERS, no_user_input=True
    )

    assert result == SOME_DEFAULT


@pytest.mark.parametrize(
    "options,options_to_mc",
    [
        (SOME_OPTIONS, {v: v for v in SOME_OPTIONS}),
        (SOME_MAPPING_OPTIONS, SOME_MAPPING_OPTIONS),
    ],
)
def test_choice__static_message__multiple_choice_called_with_mapping_of_options(
    options, options_to_mc, mocker
):
    user_io = mocker.patch("columbo._interaction.user_io")

    Choice(SOME_NAME, SOME_STRING, options, SOME_DEFAULT).ask(
        SOME_ANSWERS, no_user_input=True
    )

    user_io.multiple_choice.assert_called_once_with(
        SOME_STRING, options_to_mc, default=SOME_DEFAULT, no_user_input=True
    )


@pytest.mark.parametrize(
    "dy_options,dy_options_to_mc",
    [
        (some_dynamic_options, {v: v for v in SOME_DYNAMIC_OPTION_RESULT}),
        (some_dynamic_mapping_options, SOME_DYNAMIC_MAPPING_OPTION_RESULT),
    ],
)
def test_choice__dynamic_message__multiple_choice_dynamic_message(
    dy_options, dy_options_to_mc, mocker
):
    user_io = mocker.patch("columbo._interaction.user_io")

    Choice(SOME_NAME, some_dynamic_string, dy_options, some_dynamic_default).ask(
        SOME_ANSWERS, no_user_input=True
    )

    user_io.multiple_choice.assert_called_once_with(
        SOME_DYNAMIC_STRING_RESULT,
        dy_options_to_mc,
        default=SOME_DYNAMIC_DEFAULT_RESULT,
        no_user_input=True,
    )


@pytest.mark.parametrize("value,is_valid", [(SOME_DEFAULT, True), (SOME_STRING, False)])
def test_choice_is_valid__static_options__expected_result(value, is_valid):
    question = Choice(SOME_NAME, SOME_STRING, SOME_OPTIONS, SOME_DEFAULT)

    result = question.validate(value, SOME_ANSWERS)

    assert result.valid == is_valid


@pytest.mark.parametrize(
    "value,is_valid,options",
    [
        (SOME_DYNAMIC_DEFAULT_RESULT, True, some_dynamic_options),
        (SOME_STRING, False, some_dynamic_options),
        (SOME_DYNAMIC_DEFAULT_RESULT, True, some_dynamic_mapping_options),
        (SOME_STRING, False, some_dynamic_mapping_options),
    ],
)
def test_choice_is_valid__dynamic_options__expected_result(value, is_valid, options):
    question = Choice(SOME_NAME, SOME_STRING, options, SOME_DEFAULT)

    result = question.validate(value, SOME_ANSWERS)

    assert result.valid == is_valid


@pytest.mark.parametrize(
    "value,is_valid,options",
    [
        (SOME_DYNAMIC_DEFAULT_RESULT, True, some_dynamic_options),
        (SOME_STRING, False, some_dynamic_options),
        (SOME_DYNAMIC_DEFAULT_RESULT, True, some_dynamic_mapping_options),
        (SOME_STRING, False, some_dynamic_mapping_options),
    ],
)
def test_choice__validate__dynamic_options__expected_result(value, is_valid, options):
    question = Choice(SOME_NAME, SOME_STRING, options, SOME_DEFAULT)

    result = question.validate(value, SOME_ANSWERS)

    assert result.valid == is_valid


def test_choice_copy__new_instance():
    original = Choice(
        SOME_NAME, some_dynamic_string, some_dynamic_options, some_dynamic_default
    )

    copy = original.copy()

    assert copy is not original


def test_choice_copy__no_args__multiple_choice_same_message(mocker):
    user_io = mocker.patch("columbo._interaction.user_io")

    question = Choice(SOME_NAME, SOME_STRING, SOME_OPTIONS, SOME_DEFAULT)
    question.ask(SOME_ANSWERS, no_user_input=True)

    question.copy().ask(SOME_ANSWERS, no_user_input=True)

    calls = user_io.multiple_choice.mock_calls
    assert len(calls) == 2
    assert calls[0] == calls[1]


@pytest.mark.parametrize(
    "dy_options,dy_options_to_mc,new_options",
    [
        (some_dynamic_options, {v: v for v in SOME_OPTIONS}, SOME_OPTIONS),
        (some_dynamic_mapping_options, SOME_MAPPING_OPTIONS, SOME_MAPPING_OPTIONS),
    ],
)
def test_choice_copy__diff_message__multiple_choice_diff_message(
    dy_options, dy_options_to_mc, new_options, mocker
):
    user_io = mocker.patch("columbo._interaction.user_io")

    Choice(SOME_NAME, some_dynamic_string, dy_options, some_dynamic_default).copy(
        message=SOME_STRING, options=new_options, default=SOME_DEFAULT
    ).ask(SOME_ANSWERS, no_user_input=True)

    user_io.multiple_choice.assert_called_once_with(
        SOME_STRING, dy_options_to_mc, default=SOME_DEFAULT, no_user_input=True
    )


def test_confirm__no_input__default_value():
    result = Confirm(SOME_NAME, SOME_STRING, SOME_BOOL).ask(
        SOME_ANSWERS, no_user_input=True
    )

    assert result == SOME_BOOL


def test_confirm__static_message__confirm_called(mocker):
    user_io = mocker.patch("columbo._interaction.user_io")

    Confirm(SOME_NAME, SOME_STRING, SOME_BOOL).ask(SOME_ANSWERS, no_user_input=True)

    user_io.confirm.assert_called_once_with(
        SOME_STRING, default=SOME_BOOL, no_user_input=True
    )


def test_confirm__dynamic_message__confirm_dynamic_message(mocker):
    user_io = mocker.patch("columbo._interaction.user_io")

    Confirm(SOME_NAME, some_dynamic_string, some_dynamic_bool).ask(
        SOME_ANSWERS, no_user_input=True
    )

    user_io.confirm.assert_called_once_with(
        SOME_DYNAMIC_STRING_RESULT, default=SOME_OTHER_BOOL, no_user_input=True
    )


def test_confirm_copy__new_instance():
    original = Confirm(SOME_NAME, SOME_STRING, SOME_BOOL)

    copy = original.copy()

    assert copy is not original


def test_confirm_copy__no_args__confirm_same_message(mocker):
    user_io = mocker.patch("columbo._interaction.user_io")

    question = Confirm(SOME_NAME, SOME_STRING, SOME_BOOL)
    question.ask(SOME_ANSWERS, no_user_input=True)

    question.copy().ask(SOME_ANSWERS, no_user_input=True)

    calls = user_io.confirm.mock_calls
    assert len(calls) == 2
    assert calls[0] == calls[1]


def test_confirm_copy__diff_message__confirm_diff_message(mocker):
    user_io = mocker.patch("columbo._interaction.user_io")

    Confirm(SOME_NAME, some_dynamic_string, some_dynamic_bool).copy(
        message=SOME_STRING, default=SOME_BOOL
    ).ask(SOME_ANSWERS, no_user_input=True)

    user_io.confirm.assert_called_once_with(
        SOME_STRING, default=SOME_BOOL, no_user_input=True
    )


def test_basic_question__no_input__default_value():
    result = BasicQuestion(SOME_NAME, SOME_STRING, SOME_DEFAULT).ask(
        SOME_ANSWERS, no_user_input=True
    )

    assert result == SOME_DEFAULT


def test_basic_question__ask__validator__default_value():
    result = BasicQuestion(
        SOME_NAME, SOME_STRING, SOME_DEFAULT, validator=lambda v, a: ValidationSuccess()
    ).ask(SOME_ANSWERS, no_user_input=True)

    assert result == SOME_DEFAULT


def test_basic_question__static_message__ask_called(mocker):
    user_io = mocker.patch("columbo._interaction.user_io")

    BasicQuestion(SOME_NAME, SOME_STRING, SOME_DEFAULT).ask(
        SOME_ANSWERS, no_user_input=True
    )

    user_io.ask.assert_called_once_with(
        SOME_STRING, default=SOME_DEFAULT, no_user_input=True
    )


def test_basic_question__dynamic_message__ask_dynamic_message(mocker):
    user_io = mocker.patch("columbo._interaction.user_io")

    BasicQuestion(SOME_NAME, some_dynamic_string, some_dynamic_default).ask(
        SOME_ANSWERS, no_user_input=True
    )

    user_io.ask.assert_called_once_with(
        SOME_DYNAMIC_STRING_RESULT,
        default=SOME_DYNAMIC_DEFAULT_RESULT,
        no_user_input=True,
    )


def test_basic_question_copy__new_instance():
    original = BasicQuestion(SOME_NAME, SOME_STRING, SOME_DEFAULT)

    copy = original.copy()

    assert copy is not original


def test_basic_question_copy__no_args__confirm_same_message(mocker):
    user_io = mocker.patch("columbo._interaction.user_io")

    question = BasicQuestion(SOME_NAME, SOME_STRING, SOME_DEFAULT)
    question.ask(SOME_ANSWERS, no_user_input=True)

    question.copy().ask(SOME_ANSWERS, no_user_input=True)

    calls = user_io.ask.mock_calls
    assert len(calls) == 2
    assert calls[0] == calls[1]


def test_basic_question_copy__diff_message__confirm_diff_message(mocker):
    user_io = mocker.patch("columbo._interaction.user_io")

    BasicQuestion(SOME_NAME, some_dynamic_string, some_dynamic_default).copy(
        message=SOME_STRING, default=SOME_DEFAULT
    ).ask(SOME_ANSWERS, no_user_input=True)

    user_io.ask.assert_called_once_with(
        SOME_STRING, default=SOME_DEFAULT, no_user_input=True
    )


@pytest.mark.parametrize("value", [SOME_DEFAULT, SOME_STRING])
def test_basic_question_is_valid__no_validator__always_valid(value):
    question = BasicQuestion(SOME_NAME, SOME_STRING, SOME_DEFAULT)

    result = question.validate(value, SOME_ANSWERS)

    assert result.valid


@pytest.mark.parametrize(
    ["is_valid", "validator_response"],
    [(True, ValidationSuccess()), (False, ValidationFailure(error="some-error"))],
)
def test_basic_question_is_valid__validator__result_of_validator(
    is_valid, validator_response
):
    question = BasicQuestion(
        SOME_NAME, SOME_STRING, SOME_DEFAULT, validator=lambda v, a: validator_response
    )

    result = question.validate(SOME_STRING, SOME_ANSWERS)

    assert result.valid == is_valid


def test_basic_question_is_valid__invalid_validator__exception():
    question = BasicQuestion(SOME_NAME, SOME_STRING, SOME_DEFAULT, validator=object())  # type: ignore[arg-type]

    with pytest.raises(ValueError):
        question.validate(SOME_STRING, SOME_ANSWERS)


@pytest.mark.parametrize(
    "validity_responses",
    [
        [ValidationSuccess()],
        [ValidationFailure("some-error"), ValidationSuccess()],
        [
            ValidationFailure("some-error1"),
            ValidationFailure("some-error2"),
            ValidationSuccess(),
        ],
    ],
)
def test_basic_question__invalid_asked_multiple_times(mocker, validity_responses):
    """
    A BasicQuestion will continue to be asked until a valid response is provided

    We force the validator to fail several times, and assert the user_io.ask() is invoked the correct amount of times.
    """

    user_io_ask_mock = mocker.patch("columbo._interaction.user_io.ask")

    BasicQuestion(
        SOME_NAME,
        SOME_STRING,
        SOME_DEFAULT,
        validator=mocker.Mock(side_effect=validity_responses),
    ).ask(SOME_ANSWERS)

    assert user_io_ask_mock.call_count == len(validity_responses)


@pytest.mark.parametrize("no_user_input", [True, False])
def test_basic_question__default_invalid_no_user_input__error(no_user_input, mocker):
    """
    Default values should be valid answers. However, if not BasicQuestion's retry loop could cause an infinite loop
    when no_user_input is provided.
    """
    user_io = mocker.patch("columbo._interaction.user_io")
    user_io.ask.return_value = SOME_DEFAULT
    with pytest.raises(ValueError):
        BasicQuestion(
            SOME_NAME,
            SOME_STRING,
            SOME_DEFAULT,
            validator=lambda v, a: ValidationFailure("some error"),
        ).ask(SOME_ANSWERS, no_user_input=no_user_input)


def test_to_value__invalid_type__exception():
    with pytest.raises(ValueError):
        to_value(object(), SOME_ANSWERS, str)  # type: ignore[arg-type]


def test_to_value__invalid_dynamic_type__exception():
    with pytest.raises(ValueError):
        to_value(lambda _: object(), SOME_ANSWERS, str)  # type: ignore[arg-type,return-value]


def test_to_labeled_options__invalid_type__exception():
    with pytest.raises(ValueError):
        to_labeled_options(object(), SOME_ANSWERS)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "description,should_ask,expected_result",
    [("not set", None, True), ("dynamic", some_dynamic_bool, SOME_OTHER_BOOL)],
)
def test_should_ask__expected_result(should_ask, expected_result, description):
    result = SampleQuestion(SOME_NAME, SOME_STRING, should_ask=should_ask).should_ask(
        SOME_ANSWERS
    )

    assert result == expected_result, description


def test_should_ask__invalid_type__exception():
    question = SampleQuestion(SOME_NAME, SOME_STRING, should_ask=object())  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        question.should_ask(SOME_ANSWERS)


@pytest.mark.parametrize(
    "description,should_ask,expected_result",
    [("not set", None, True), ("dynamic", some_dynamic_bool, SOME_OTHER_BOOL)],
)
def test_displayable_should_ask__expected_result(
    should_ask, expected_result, description
):
    result = SampleDisplayable(SOME_STRING, should_ask=should_ask).should_ask(
        SOME_ANSWERS
    )

    assert result == expected_result, description


def test_displayable_should_ask__invalid_type__exception():
    displayable = SampleDisplayable(SOME_STRING, should_ask=object())  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        displayable.should_ask(SOME_ANSWERS)


def test_get_answers__unknown_interaction_provided():
    """
    An unsupported interaction type should raise a ValueError
    """
    # `5` is not an interaction type that is supported
    interactions = [Echo("foo"), 5]
    with pytest.raises(ValueError):
        get_answers(interactions)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    [
        "basic_question_should_ask",
        "expected_basic_question_ask_call_count",
        "echo_should_ask",
        "expected_echo_display_call_count",
    ],
    [(True, 1, False, 0), (False, 0, True, 1)],
)
def test_get_answers__proper_funcs_called(
    mocker,
    basic_question_should_ask,
    expected_basic_question_ask_call_count,
    echo_should_ask,
    expected_echo_display_call_count,
):
    """
    Given a list of interactions of different types, validate the proper funcs should be invoked on each

    The parametrization asserts that Question interactions are only 'asked' when they should be asked and
    that Displayable interactions are only 'displayed' when they should be displayed.
    """
    echo_interaction_mock = mocker.Mock(
        spec=Echo, should_ask=mocker.Mock(return_value=echo_should_ask)
    )
    basic_question_interaction_mock = mocker.Mock(
        spec=BasicQuestion,
        should_ask=mocker.Mock(return_value=basic_question_should_ask),
    )
    # mock names must be set after mock object is created
    echo_interaction_mock.name = "echo_interaction_mock"
    basic_question_interaction_mock.name = "basic_question_interaction_mock"

    interactions = [echo_interaction_mock, basic_question_interaction_mock]
    get_answers(interactions)

    # functions belonging to interactions should be invoked
    # in the case of a question, it either should or shouldn't be asked
    # in the case of echo, it either should or shouldn't be displayed
    echo_interaction_mock.should_ask.assert_called_once()
    assert echo_interaction_mock.display.call_count == expected_echo_display_call_count
    basic_question_interaction_mock.should_ask.assert_called_once()
    assert (
        basic_question_interaction_mock.ask.call_count
        == expected_basic_question_ask_call_count
    )


def test_get_answers__previous_answers__result_has_previous_answers_and_question_answers():
    existing_key = "question1"
    existing_answer = "some previous answer"
    existing_answers = {existing_key: existing_answer}
    expected_answers = {existing_key: existing_answer, SOME_NAME: SOME_DEFAULT}

    interactions = [
        BasicQuestion(SOME_NAME, "What is the answer to life?", default=SOME_DEFAULT)
    ]

    new_answers = get_answers(interactions, existing_answers, no_user_input=True)

    assert new_answers == expected_answers


@pytest.mark.parametrize("questions", DUPLICATE_QUESTION_NAME_PARAMS)
def test_parse_args__duplicate_question_name__exception(questions):
    with pytest.raises(DuplicateQuestionNameException):
        get_answers(questions)


def test_parse_args__duplicate_question_name_in_answers__exception():
    with pytest.raises(DuplicateQuestionNameException):
        get_answers(
            [BasicQuestion(SOME_NAME, SOME_STRING, SOME_DEFAULT)],
            answers={SOME_NAME: "existing value"},
        )


@pytest.mark.parametrize(
    ["description", "name", "expected_arg"], QUESTION_NAME_STANDARDIZATION_PARAMS
)
def test__canonical_arg_name__nonstandard_characters__normalized(
    description, name, expected_arg
):
    assert canonical_arg_name(name) == expected_arg, description


@pytest.mark.parametrize(
    ["should_ask", "expected_answer"],
    [
        (True, {"confirm": True, "choice": SOME_DEFAULT, "question": SOME_DEFAULT}),
        (
            False,
            {
                "confirm": False,
                "choice": SOME_NON_DEFAULT_OPTION,
                "question": SOME_STRING,
            },
        ),
    ],
)
def test_value_if_not_asked__each_interaction__produces_expected_result(
    should_ask: bool, expected_answer: Answers
) -> None:
    interactions: list[Interaction] = [
        Confirm(
            "confirm",
            SOME_STRING,
            True,
            should_ask=lambda answers: should_ask,
            value_if_not_asked=False,
        ),
        Choice(
            "choice",
            SOME_STRING,
            SOME_OPTIONS,
            SOME_DEFAULT,
            should_ask=lambda answers: should_ask,
            value_if_not_asked=SOME_NON_DEFAULT_OPTION,
        ),
        BasicQuestion(
            "question",
            SOME_STRING,
            SOME_DEFAULT,
            should_ask=lambda answers: should_ask,
            value_if_not_asked=SOME_STRING,
        ),
    ]

    results = get_answers(interactions, no_user_input=True)

    assert results == expected_answer


def test_should_ask__false_without_value_if_not_asked__no_value_in_result():
    interactions: list[Interaction] = [
        Confirm(
            "confirm",
            SOME_STRING,
            True,
            should_ask=lambda answers: False,
        ),
        Choice(
            "choice",
            SOME_STRING,
            SOME_OPTIONS,
            SOME_DEFAULT,
            should_ask=lambda answers: False,
        ),
        BasicQuestion(
            "question", SOME_STRING, SOME_DEFAULT, should_ask=lambda answers: False
        ),
    ]

    results = get_answers(interactions, no_user_input=True)

    assert results == {}


def test_value_if_not_asked__basic_question_no_should_ask__raises_exception():
    with pytest.raises(
        ValueError,
        match="You should either remove value_if_not_asked or add should_ask.",
    ):
        BasicQuestion(
            SOME_NAME,
            SOME_STRING,
            SOME_DEFAULT,
            value_if_not_asked="a",
        )


def test_value_if_not_asked__confirm_no_should_ask__raises_exception():
    with pytest.raises(
        ValueError,
        match="You should either remove value_if_not_asked or add should_ask.",
    ):
        Confirm(
            SOME_NAME,
            SOME_STRING,
            default=SOME_BOOL,
            value_if_not_asked=True,
        )


def test_value_if_not_asked__choice_no_should_ask__raises_exception():
    with pytest.raises(
        ValueError,
        match="You should either remove value_if_not_asked or add should_ask.",
    ):
        Choice(
            SOME_NAME,
            SOME_STRING,
            options=SOME_OPTIONS,
            default=SOME_DEFAULT,
            value_if_not_asked=SOME_NON_DEFAULT_OPTION,
        )


def test_value_if_not_asked__confirm_value_if_not_asked_is_not_bool__raises_exception():
    with pytest.raises(
        ValueError,
        match="value_if_not_asked must be a bool",
    ):
        Confirm(
            SOME_NAME,
            SOME_STRING,
            default=True,
            should_ask=lambda answers: True,
            value_if_not_asked=SOME_INVALID_OPTION,  # type: ignore[arg-type]
        )


def test_value_if_not_asked__basic_question_value_if_not_asked_is_not_valid__raises_exception():
    question = BasicQuestion(
        SOME_NAME,
        SOME_STRING,
        default=SOME_DEFAULT,
        should_ask=lambda answers: False,
        validator=always_fail_validator,
        value_if_not_asked=SOME_NON_DEFAULT_OPTION,
    )
    with pytest.raises(
        ValueError,
        match=f"NotAsked value is not valid: {SOME_FAILURE_MESSAGE}",
    ):
        get_answers([question], no_user_input=True)


def test_value_if_not_asked__choice_value_if_not_asked_is_not_valid__raises_exception():
    question = Choice(
        SOME_NAME,
        SOME_STRING,
        SOME_OPTIONS,
        default=SOME_DEFAULT,
        should_ask=lambda answers: False,
        value_if_not_asked=SOME_INVALID_OPTION,
    )
    with pytest.raises(
        ValueError,
        match=f"NotAsked value is not valid: Chosen value: {SOME_INVALID_OPTION} not in options",
    ):
        get_answers([question], no_user_input=True)
