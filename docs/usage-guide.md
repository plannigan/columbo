# Usage Guide

This is page provides detailed descriptions of al the ways `columbo` can be used. If you are new to `columbo`, the
[Getting Started][getting-started] page provides a gradual introduction of the basic functionality with examples.

### Static vs Dynamic Values

Before diving into the specifics about each `Interaction` type, it is important to understand how `columbo` supports
both static and dynamic values. A static value is a value that is known when creating an `Interaction` instance.
Frequently this will be a value like a string literal, but that is not a requirement.

In contrast, a dynamic value is one which depends on one or more answer provided by the user from a previous question.
This is supported by accepting a function that takes an `Answers` dictionary as an argument and returns a value with
the type of that static value would have. For example, the static value for `message` is `str`. Therefore, tye dynamic
value would be a function that accepts `Answers` and returns a string (`Callable[[Answers],str]`).

In most cases, any argument to an `Interaction`'s constructor can be dynamic. This guide will explicitly mention when
the constructor requires an argument to be a static value.

## Interactions

`columbo` provides five types of `Interactions` that can be used to control how the program will interact with the user:

* `Echo` - Print text to the terminal, but don't stop to accept any input from the user.
* `Acknowledge` - Print text to the terminal. Wait for the user to press ++enter++.
* `BasicQuestion` - Print text to the terminal. Allow the user to type a text response. Pressing ++enter++ submits the
    response.
* `Choice` - Print text to the terminal, followed by a numbered list of options. Allow the user to enter the number
    of the option they wish to select. Pressing ++enter++ submits the response.
* `Confirm` - Print text to the terminal which expects a Yes or No answer. Pressing ++y++ or ++n++ submits the
    corresponding response.

## Creating Interactions

### Echo & Acknowledge

`Echo` and `Acknowledge` both accept `message` as their only argument. This is the message to be displayed to the user.

### All Questions

`BasicQuestion`, `Choice`, & `Confirm` all accept the following arguments.

* `name`: The identifier that will be used as the key to access this question's answer. Each question must have a unique
    value for `name`. **Can't be dynamic**.
* `message`: The message to be displayed to the user.
* `default`: The default answer to the question. This is used when the user does not provide an explicit value.
* `should_ask`: Optional. When given, the argument should be a function that accepts an `Answers` dictionary and returns
    `True` or `False`. Returning `True` indicates that the question should be asked. Returning `False` will skip the
    question and not present it to the user. See [Only Asking Some Questions](#only-asking-some-questions) for more
    details.
* `cli_help`: Optional. A help message to be displayed for command line interface. See
    [CLI documentation](#command-line-interface) for more details. **Can't be dynamic**.

### Basic Question

In addition to the arguments [mentioned above](#all-questions), `BasicQuestion` also accepts the following argument.

* `validator`: Optional. When given, the argument should be a function that accepts a string and an `Answers`
    dictionary. The first value is the answer provided by the user. The `Answers` dictionary will contain the value for
    each previous question that has been asked. If the value is valid, the function and should return `None`. If the
    value is invalid, the function should return a string describing why the value is invalid. This message will be
    displayed to the user, and the question will be re-asked. Not providing this argument means that any value provided
    by the user will be accepted.

### Choice

In addition to the arguments [mentioned above](#all-questions), `Choice` also accepts the following argument.

* `options`: The list of possible value the user can choose from.

### Confirm

`Confirm` doesn't take any additional arguments that weren't [mentioned above](#all-questions). However, the `default`
argument takes a `bool` instead of `str`.

## Only Asking Some Questions

There are situations where a question should be asked some times, but not all the time. For example, a program that collects
information about a user's pets should not ask the user for the dog's name and breed if the user said they do not have a
dog. The `should_ask` argument that is present on each question provides a way to achieve this functionality.

Similarly, `should_ask` can be used to provide branching paths to the user. An example of these branching paths is a
[Choose Your Own Adventure][choose-your-own-adventure] story. The story provides the reader with choices during the
adventure. These choices introduce diverging paths of interactions that may or may not join at the end.

!!! warning Be careful when skipping a question
    When `columbo` skips over a question, the `Answers` dictionary will **NOT** contain a key-value pair for the
    skipped question. The examples below will demonstrate this result.

### Optional Questions

The following is a basic example that has two optional questions that are not asked based on the answer to the first
question.

```python
import columbo

def does_user_have_a_dog(answers: columbo.Answers) -> bool:
    return answers["has_dog"]

interactions = [
    columbo.Confirm("has_dog", "Do you have a dog?", default=True),
    columbo.BasicQuestion(
        "dog_name",
        "What is the name of the dog?",
        should_ask=does_user_have_a_dog,
        default="Kaylee"
    ),
    columbo.BasicQuestion(
        "dog_breed",
        "What is the breed of the dog?",
        should_ask=does_user_have_a_dog,
        default="Basset Hound"
    )
]

user_answers = columbo.get_answers(interactions)
print(user_answers)
```

If the user accepts the default answers for each of these questions, the output will be:

```
{"has_dog": True, "dog_name": "Kaylee", "dog_breed": "Basset Hound"}
```

However, when the user answers the first question with "no", the output will be:

```
{"has_dog": False}
```

Note that in this case, the `Answers` dictionary only has an answer to the first question.

### Branching Paths

A question that is part of a branching path very similar to an optional question. It is still a question where
`should_ask` was given to determine if the question should be skipped our not. The branching aspect comes there being at
least two sets of optional questions. Each set has a `should_ask` argument that checks for a different state for a
single answer. In this way, only one of the sets of optional questions will ever be asked.

The following is an example of a short story that has two divergent paths that join at the end. Each individual question
isn't different from the optional questions [demonstrated above](#optional-questions). The program achieves the
branching paths by supplying different `should_ask` values that will never both evaluate to `True`.

```python
import columbo

def went_left(answers: columbo.Answers) -> bool:
    return answers["which_door"] == "left"

def went_right(answers: columbo.Answers) -> bool:
    return answers["which_door"] == "right"

def outcome(answers: columbo.Answers) -> str:
    if answers.get("has_key", False):
        return "You try the the key on the lock. With a little jiggling, it finally opens. You open the gate and leave."
    if answers.get("has_hammer", False):
        return "You hit the lock with the hammer and it falls to the ground. You open the gate and leave."
    return (
        "Unable to open the gate yourself, you yell for help. A farmer in the nearby field hears you. "
        "He reaches into his pocket and pulls out a key to unlock the gate and open it. "
        "As you walk through the archway he says, "
        "\"What I don't understand is how you got in there. This is the only key.\""
    )


interactions = [
    columbo.Echo(
        "You wake up in a room that you do not recognize. "
        "In the dim light, you can see a large door to the left and a small door to the right."
    ),
    columbo.Choice(
        "which_door",
        "Which door do you walk through?",
        options=["left", "right"],
        default="left"
    ),
    columbo.Confirm(
        "has_key",
        "You step into a short hallway and the door closes behind you, refusing to open again. "
        "As you walk down the hallway, there is a small side table with a key on it.\n"
        "Do you pick up the key before going through the door at the other end?",
        should_ask=went_left,
        default=True
    ),
    columbo.Confirm(
        "has_hammer",
        "You step into smaller room and the door closes behind, refusing to open again. "
        "The room has a single door on the opposite side of the room and a work bench with a hammer on it.\n"
        "Do you pick up the hammer before going through the door at the other side?",
        should_ask=went_right,
        default=True
    ),
    columbo.Echo(
        "You enter a small courtyard with high walls. There is an archway that would allow you to go free, "
        "but the gate is locked."
    ),
    columbo.Echo(outcome),
]

user_answers = columbo.get_answers(interactions)
print(user_answers)
```

For this example, the output display while iterating over the interactions is the interesting part of the program.
However, it is important to note that is only possible for the `Answers` dictionary to have a key-value pair for
`has_key` or `has_hammer`, not both.

## Command Line Interface

In addition to providing an interactive terminal based UI to ask the user each question, `columbo` can also generate a
command line argument parser based on the list of `Interaction`s. When used in this manor, `Echo` & `Acknowledge` are
ignored. To produce a consistent command line argument format, the value of each question's `name` will be transformed
using the following rule:

* If the there are any upper-case characters, lower-case characters will be used.
* If the there are is a space character, a dash will be used in its place.
* If the there are is an underscore character, a dash will be used in its place.

For example:

| Original   | Result     |
| ---------- | ---------- |
| user       | user       |
| user_email | user-email |
| User Email | user-email |

!!! warning
    As a result of the transformation process, it is possible to have a sequence of question with unique `name`s for the
    `Answers` dictionary, but cause a collision when creating command line arguments.

For `BasicQuestion` & `Choice`, the result will be preceded with two dashes (ex: `--user` or `--user-email`).

For `Confirm`, `columbo` produces two command lines arguments. After following the transformation rules, the command
line arguments will be `--{NAME}` & `--no-{NAME}` to explicitly specify `True` or `False`, respectively (ex:
`--likes-dogs` and `--no-likes-dogs`)

Since the argument parser must be constructed before receiving any user input, all `Question`s produce arguments.
`should_ask` is only considered when processing the given arguments.

[getting-started]: getting-started.md
[choose-your-own-adventure]: https://en.wikipedia.org/wiki/Choose_Your_Own_Adventure
