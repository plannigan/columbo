[![CI pipeline status](https://github.com/wayfair-incubator/columbo/workflows/CI/badge.svg?branch=main)][ci]
[![PyPI](https://img.shields.io/pypi/v/columbo)][pypi]
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/columbo)][pypi]
[![codecov](https://codecov.io/gh/wayfair-incubator/columbo/branch/main/graph/badge.svg)][codecov]
[![Checked with mypy](https://img.shields.io/badge/mypy-checked-blue)][mypy-home]
[![Code style: black](https://img.shields.io/badge/code%20style-black-black.svg)][black-home]

# Columbo

Specify a dynamic set of questions to ask a user and get their answers.

`columbo`'s feature set allows a program to:

* Ask multiple types of questions:
    * Yes or No
    * Multiple choice
    * Open-ended
* Validate the response provided by the user.
* Use answers from earlier questions:
    * As part of the text of a question
    * As part of the text of a default value
    * To decide if a question should be skipped
* Accept answers from the command line in addition to prompting the user.

## Example

### User Prompts

The primary use of `columbo` is to define a sequence of interactions that are used to prompt a user to provide answers
using a terminal. Below is a sample which shows some ways this can be used.

```python
import columbo

interactions = [
    columbo.Echo("Welcome to the Columbo example"),
    columbo.Acknowledge(
        "Press enter to start"
    ),
    columbo.BasicQuestion(
        "user",
        "What is your name?",
        default="Patrick",
    ),
    columbo.BasicQuestion(
        "user_email",
        lambda answers: f"""What email address should be used to contact {answers["user"]}?""",
        default="me@example.com"
    ),
    columbo.Choice(
        "mood",
        "How are you feeling today?",
        options=["happy", "sad", "sleepy", "confused"],
        default="happy",
    ),
    columbo.Confirm("likes_dogs", "Do you like dogs?", default=True),
]

answers = columbo.get_answers(interactions)
print(answers)
```

Below shows the output when the user accepts the default values for most of the questions. The user provides a different
value for the email and explicitly confirms that they like dogs.

```text
Welcome to the Columbo example
Press enter to start
 
What is your name? [Patrick]:

What email address should be used to contact Patrick? [me@example.com]: patrick@example.com

How are you feeling today?
1 - happy
2 - sad
3 - sleepy
4 - confused
Enter the number of your choice [1]:

Do you like dogs? (Y/n): y

{'user': 'Patrick', 'user_email': 'patrick@example.com', 'mood': 'happy', 'likes_dogs': True}
```

### Command Line Answers

In addition to the interactive prompts, `columbo` can also parse command line arguments for interactions. This is done by
changing `columbo.get_answers()` to `columbo.parse_args()`. Below shows the output when using the same interactions from above.

```shell
$ python columbo_example.py --user-email patrick@example.com --likes-dogs
{'user': 'Patrick', 'user_email': 'patrick@example.com', 'mood': 'happy', 'likes_dogs': True}
```

<details>
    <summary>The full example</summary>

```python
import columbo

interactions = [
    columbo.Echo("Welcome to the Columbo example"),
    columbo.Acknowledge(
        "Press enter to start"
    ),
    columbo.BasicQuestion(
        "user",
        "What is your name?",
        default="Patrick",
    ),
    columbo.BasicQuestion(
        "user_email",
        lambda answers: f"""What email address should be used to contact {answers["user"]}?""",
        default="me@example.com"
    ),
    columbo.Choice(
        "mood",
        "How are you feeling today?",
        options=["happy", "sad", "sleepy", "confused"],
        default="happy",
    ),
    columbo.Confirm("likes_dogs", "Do you like dogs?", default=True),
]

answers = columbo.parse_args(interactions)
print(answers)
```
</details>

## Documentation

Check out the [project documentation][columbo-docs].

For an overview on how repository structure and how to work with the code base, read the
[Development Guide][development-docs].

[ci]: https://github.com/wayfair-incubator/columbo/actions
[pypi]: https://pypi.org/project/columbo/
[codecov]: https://codecov.io/gh/wayfair-incubator/columbo
[mypy-home]: http://mypy-lang.org/
[black-home]: https://github.com/psf/black
[columbo-docs]: https://wayfair-incubator.github.io/columbo/latest/
[development-docs]: https://wayfair-incubator.github.io/columbo/latest/development-guide/
