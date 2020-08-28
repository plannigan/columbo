"""
Helpful wrappers for prompt-toolkit functionality.
"""

from typing import Collection

from prompt_toolkit import shortcuts
from prompt_toolkit.formatted_text import merge_formatted_text
from prompt_toolkit.key_binding.key_bindings import KeyBindings
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from prompt_toolkit.keys import Keys
from prompt_toolkit.validation import Validator

_NO_INPUT = ""


def echo(*args, **kwargs) -> None:
    shortcuts.print_formatted_text(*args, **kwargs)


def acknowledge(*args, no_user_input: bool = False, **kwargs) -> None:
    echo(*args, **kwargs)
    if no_user_input:
        return

    shortcuts.prompt("", **kwargs)
    echo("")


def confirm(
    question: str, default: bool = False, no_user_input: bool = False, **kwargs
) -> bool:
    if no_user_input:
        return default

    answer = _confirm(question, default, **kwargs)
    echo("")

    return answer


def ask(question: str, default: str, no_user_input: bool = False, **kwargs) -> str:
    if no_user_input:
        return default

    # Don't pass real default to prompt as it requires the user to delete the characters to enter something custom
    answer = shortcuts.prompt(f"{question} [{default}]: ", default=_NO_INPUT, **kwargs)
    if answer == _NO_INPUT:
        answer = default
    echo("")

    return answer


def multiple_choice(
    question: str,
    options: Collection[str],
    default: str,
    no_user_input: bool = False,
    **kwargs,
) -> str:
    if len(options) == 0:
        raise ValueError("options must contain at least one value")

    prompt_lines = [question]
    default_choice = None
    choice_map = {}
    for i, value in enumerate(options):
        key = str(i + 1)
        choice_map[key] = value
        prompt_lines.append(f"{key} - {value}")

        if default == value:
            default_choice = key

    if default_choice is None:
        raise ValueError(f"""Default "{default}" was not an option {options}""")

    prompt_lines.append("Enter the number of your choice")

    user_choice = ask(
        "\n".join(prompt_lines),
        validator=Validator.from_callable(
            lambda text: text == _NO_INPUT or text in choice_map.keys()
        ),
        default=default_choice,
        no_user_input=no_user_input,
        **kwargs,
    )

    return choice_map[user_choice]


def _confirm(question: str, default: bool = False, **kwargs) -> bool:
    bindings = KeyBindings()

    @bindings.add("y")
    @bindings.add("Y")
    def _yes(event: KeyPressEvent) -> None:
        session.default_buffer.text = "y"
        event.app.exit(result=True)

    @bindings.add("n")
    @bindings.add("N")
    def _no(event: KeyPressEvent) -> None:
        session.default_buffer.text = "n"
        event.app.exit(result=False)

    @bindings.add(Keys.Any)
    def _any(_: KeyPressEvent) -> None:
        # Disallow inserting other text.
        pass

    if default:
        default_indicator = "Y/n"
        bindings.add(Keys.Enter)(_yes)
    else:
        default_indicator = "y/N"
        bindings.add(Keys.Enter)(_no)

    complete_message = merge_formatted_text([question, f" ({default_indicator}): "])
    session: shortcuts.PromptSession[bool] = shortcuts.PromptSession(
        complete_message, key_bindings=bindings, **kwargs
    )
    return session.prompt(complete_message, key_bindings=bindings, **kwargs)
