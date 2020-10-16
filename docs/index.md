# Columbo

[![CI pipeline status](https://github.com/wayfair-incubator/columbo/workflows/CI/badge.svg?branch=main)][ci]
[![codecov](https://codecov.io/gh/wayfair-incubator/columbo/branch/main/graph/badge.svg)][codecov]
TODO: PyPi Release Badge

`columbo` provides a way to specify a dynamic set of questions to ask a user and get their answers.

## Example

### User Prompts

The primary use of `columbo` is to define a sequence of interaction that are used to prompt a user to provide answers
using a terminal. Below is a sample which shows how this can be used.

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

columbo.get_answers(interactions)
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

{'user': 'Patrick', 'user_email': 'me@example.com', 'mood': 'happy', 'likes_dogs': True}
```

### Command Line Answers

TODO

## Where to Start?

To learn the basics of how to start using `columbo`, read the [Getting Started][getting_started] page.

## Detailed Documentation

To learn more about the various ways `columbo` can be used, read the [Usage Guide][usage_guide] page.

## API Reference

To find specific information about a specific function or class, read the [API Reference][api_reference].

[ci]: https://github.com/wayfair-incubator/columbo/actions
[codecov]: https://codecov.io/gh/wayfair-incubator/columbo
[getting_started]: getting-started.md
[usage_guide]: usage-guide.md
[api_reference]: api.md
