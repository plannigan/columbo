import re
from typing import List

import columbo


def is_email_address(value: str, _: columbo.Answers) -> columbo.ValidationResponse:
    if not re.match(r"^\w+@\w+", value):
        error_message = f"{value} is not a valid email address"
        return columbo.ValidationFailure(error=error_message)

    return columbo.ValidationSuccess()


interactions: List[columbo.Interaction] = [
    columbo.BasicQuestion(
        "user_email_address",
        "What email address should be used to contact you?",
        default="me@example.com",
        validator=is_email_address,
    )
]

user_answers = columbo.get_answers(interactions)
print(user_answers)
