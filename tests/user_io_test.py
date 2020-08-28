import pytest

from columbo import _user_io as user_io

SOME_BOOL = True
SOME_OTHER_BOOL = False
SOME_STRING = "hello"
SOME_OTHER_STRING = "good-bye"


def test_acknowledge__yes_user_input__default_value(mocker):
    mock_prompt = mocker.patch("prompt_toolkit.shortcuts.prompt")

    user_io.acknowledge("Some question?")

    mock_prompt.assert_called_once_with("")


def test_acknowledge__no_user_input__default_value(mocker):
    mock_prompt = mocker.patch("prompt_toolkit.shortcuts.prompt")

    user_io.acknowledge("Some question?", no_user_input=True)

    mock_prompt.assert_not_called()


def test_confirm__no_user_input__default_value():
    result = user_io.confirm("Some question?", no_user_input=True, default=SOME_BOOL)

    assert result == SOME_BOOL


@pytest.mark.parametrize("response", [True, False])
def test_confirm__yes_user_input__confirm_result(response, mocker):
    mock_session = mocker.Mock()
    mock_session.prompt.return_value = response
    mocker.patch("prompt_toolkit.shortcuts.PromptSession", return_value=mock_session)

    result = user_io.confirm("Some question?", default=SOME_OTHER_BOOL)

    assert result == response


def test_ask__no_user_input__default_value():
    result = user_io.ask("Some question?", no_user_input=True, default=SOME_STRING)

    assert result == SOME_STRING


def test_ask__yes_user_input__prompt_result(mocker):
    mocker.patch("prompt_toolkit.shortcuts.prompt", return_value=SOME_STRING)

    result = user_io.ask("Some question?", default=SOME_OTHER_STRING)

    assert result == SOME_STRING


def test_ask__yes_user_input_no_answer__default_result(mocker):
    mocker.patch("prompt_toolkit.shortcuts.prompt", return_value="")

    result = user_io.ask("Some question?", default=SOME_OTHER_STRING)

    assert result == SOME_OTHER_STRING


def test_multiple_choice__no_user_input__default_value():
    result = user_io.multiple_choice(
        "Some question?",
        [SOME_STRING, SOME_OTHER_STRING],
        no_user_input=True,
        default=SOME_OTHER_STRING,
    )

    assert result == SOME_OTHER_STRING


def test_multiple_choice__yes_user_input__prompt_result_mapped_to_value(mocker):
    # expected value is second option
    mocker.patch("prompt_toolkit.shortcuts.prompt", return_value="2")

    result = user_io.multiple_choice(
        "Some question?", [SOME_STRING, SOME_OTHER_STRING], default=SOME_STRING
    )

    assert result == SOME_OTHER_STRING


def test_multiple_choice__default_not_option__value_error():
    with pytest.raises(ValueError):
        user_io.multiple_choice("Some question?", ["1", "2", "3"], default="100")


def test_multiple_choice__no_options__value_error():
    with pytest.raises(ValueError):
        user_io.multiple_choice("Some question?", [], default="100")
