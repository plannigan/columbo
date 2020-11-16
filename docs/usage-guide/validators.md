# Validators

`BasicQuestion` allows the user to provide arbitrary text as the answer to the question. However, there are frequently
constraints on what is considered a valid answer. Providing a `Validator` for the question allows `columbo` to verify
that the text provided by the user satisfies those constraints. If the answer is not valid, `columbo` will tell the user that
the answer is not valid and ask them to try again.

!!! Note Implicit Validators
    While, `Choice` and `Confirm` do not expose a `validator` argument, they still ensure that the answer is valid.
    A `Confirm` question will only continue when ++y++, ++n++, or ++enter++ are pressed. Any other keys will be ignored.
    A `Choice` question will only continue when ++enter++ is pressed if the input matches the number `columbo` assigned
    to one of the choices.

A `Validator` should be a function that accepts a string & an `Answers` dictionary and returns `None` or a string
(`Callable[[str,Answers],Optional[str]]`). The first value is the response provided by the user. The second value is an
`Answers` dictionary that will contain the value for each previous question that has been asked. If the response is a
valid answer, the function should return `None`. If the response is invalid, the function should return a string
describing why the value is invalid. This message will be displayed to the user and the question will be re-asked.

The example below shows a question that asks for the user's email address. The `Validator` provides a simple check to see if
the email address seems valid<sup>1</sup>. If the user's response doesn't contain an `@` character with at least one
word character on each side then the response will not be accepted.

```python
from typing import List, Optional
import re

import columbo

def is_email(value: str, _: columbo.Answers) -> Optional[str]:
    error_message: Optional[str] = None

    if not re.match(r"^\w+@\w+", value):
        error_message = f"{value} is not a valid email"

    return error_message

interactions: List[columbo.Interaction] = [
    columbo.BasicQuestion(
        "user_email",
        "What email address should be used to contact you?",
        default="me@example.com",
        validator=is_email,
    )
]

user_answers = columbo.get_answers(interactions)
print(user_answers)
```

<sup>1</sup>: The regular expression for checking for an RFC 822 compliant email address is
[overly complicated](http://www.ex-parrot.com/~pdw/Mail-RFC822-Address.html). Additionally, that only ensures that the
text is valid. It does not confirm if the host will accept emails sent to that address or if the user is the owner of
the email address.
