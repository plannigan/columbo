import re
import sys
from typing import List, Optional, cast

from columbo import (
    Acknowledge,
    Answers,
    BasicQuestion,
    Choice,
    Confirm,
    Echo,
    Interaction,
    get_answers,
    parse_args,
)


def user_to_email(answers: Answers) -> str:
    return f"""{cast(str, answers["user"]).lower().replace(' ', '')}@example.com"""


def is_email(value: str, _: Answers) -> Optional[str]:
    error_message: Optional[str] = None

    if not re.match(r"^\w+@\w+", value):
        error_message = f"{value} is not a valid email"

    return error_message


interactions: List[Interaction] = [
    Echo("Welcome to the Columbo example"),
    Acknowledge(
        "Press enter to start"
    ),
    BasicQuestion(
        "user",
        "What is your name?",
        default="Patrick",
        cli_help="Name of the user providing answers",
    ),
    BasicQuestion(
        "user_email",
        lambda answers: f"""What email address should be used to contact {answers["user"]}?""",
        default=user_to_email,
        validator=is_email,
    ),
    Choice(
        "mood",
        "How are you feeling today?",
        options=["happy", "sad", "sleepy", "confused"],
        default="happy",
        cli_help="The mood of the user.",
    ),
    Confirm("likes_dogs", "Do you like dogs?", default=True),
]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(parse_args(interactions, sys.argv[1:]))
    else:
        print(get_answers(interactions))
