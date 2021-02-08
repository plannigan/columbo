# Getting Started

## Installation

To install `columbo`, simply run this simple command in your terminal of choice:

```bash
python -m pip install columbo
```

## Introduction

The core of `columbo` are the interaction classes. They provide a way to use code to define how information should be
displayed to the user and how the user should provide feedback to the running application.

The most commonly used Interactions are the Questions.

* `BasicQuestion` - Print text to the terminal. Allow the user to type a text response. Pressing ++enter++ submits the
    response.
* `Choice` - Print text to the terminal, followed by a numbered list of options. Allow the user to enter the number
    of the option they wish to select. Pressing ++enter++ submits the response.
* `Confirm` - Print text to the terminal which expects a Yes or No answer. Pressing ++y++ or ++n++ submits the
    corresponding response.

In addition to those question types, there are types for when the user needs to be presented with information without
providing a response.

* `Echo` - Print text to the terminal, but don't stop to accept any input from the user.
* `Acknowledge` - Print text to the terminal. Wait for the user to press ++enter++.

After `columbo` has processed the questions, it returns a dictionary. More specifically the type is
`Dict[str, Union[str, bool]]` (`columbo` exposes`Answers` as an alias for this type). The dictionary maps question names
to question answers. If the `Question` was `Confirm`, the answer will be `bool`. Otherwise, the answer will be `str`.

## Creating Interactions

The constructors for each of these types all take a variety of arguments to configure how they should operate. The
following statements cover the basic functionality:

* Every `Interaction`  has a `message` argument that is the text that should be displayed to the user.
* Every `Question` has a `name` argument that is the key to be used in the `Answers` dictionary. Each question must have
    a unique name.
* Every `Question` has a `default` argument that is used when the user does not provide a specific value.

The [Usage Guide][usage-guide] provides more detailed information about the specifics of each argument for each type of
`Interaction`.

### Dynamic Values

In most cases, an argument to an `Interaction` constructor can be dynamic (the [Usage Guide][usage-guide] details the
cases where the argument **can't** be dynamic). A dynamic value is a function that takes the answers that have been
provided this far and returns the expected value as a result. For example, `message` expects a string. So it also
accepts a function that accepts `Answers` and returns a string.

```python
import columbo

def dynamic_hello(answers):
    return f"Hello, {answers['name']}"

interactions = [
    columbo.BasicQuestion(
        "name",
        "What is your name?",
        default="Patrick",
    ),
    columbo.Echo(dynamic_hello)
]
columbo.get_answers(interactions)
```

When iterating through these interactions, if the user replied "Alice" to the first question, "Hello, Alice" would be
printed next.

## Walking Though Basic Examples

### User Prompts

This is the example that appears on the [main page][docs-main] of the documentation.

```python linenums="1"
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

* Line 1: Import the `columbo` module.
* Line 3 - 25: Create a list of `Interactions` to be stored in the variable `interactions`.
* Line 4: Create an instance of `Echo` that will display a basic welcome message.
* Line 5-7: Create an instance of `Acknowledge` that will tell the user the program will not continue until ++enter++ is
    pressed.
* Line 8-12: Create an instance of `BasicQuestion` that will ask the user to provide their name. The key `user` will be
    used in the `Answers` dictionary for the value from this question. If the user presses ++enter++ without providing a
    value, the default of `Patrick` will be used.
* Line 13-17: Create an instance of `BasicQuestion` that will ask the user to provide their email address. The displayed
    message is dynamic and will include the value from the previous question. The key `user_email` will be used in the
    `Answers` dictionary for the value from this question. If the user presses ++enter++ without providing a value, the
    default of `me@example.com` will be used.
* Line 18-23: Create an instance of `Choice` that will ask the user for their current mood. The question allows the user
    to select one of four options. The key `mood` will be used in the `Answers` dictionary for the value from this
    question. If the user presses ++enter++ without providing a value, the default of `happy` will be used.
* Line 24: Create an instance of `Confirm` that will ask the user if they like dogs. The key `likes_dogs` will be used
    in the `Answers` dictionary for the value from this question. If the user presses ++enter++ without providing a
    value, the default of `True` will be used.
* Line 27: Have `columbo` iterate over the `Interactions` prompting the user for each question.
* Line 28: Print tha `Answers` dictionary so that the values can be seen.

### Command Line Arguments

This is the example will be just like the [previous example](#walking-though-a-basic-example), except it will
demonstrate the Command Line functionality.

The relevant change can be seen here:

```python linenums="24" hl_lines="4-7"
    columbo.Confirm("likes_dogs", "Do you like dogs?", default=True),
]

answers = columbo.parse_args(interactions, args=[
    "--user-email", "patrick@example.com",
    "--likes-dogs",
])
print(answers)
```

<details>
    <summary>The full example</summary>

```python linenums="1" hl_lines="27-30"
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

answers = columbo.parse_args(interactions, args=[
    "--user-email", "patrick@example.com",
    "--likes-dogs",
])
print(answers)
```
</details>

* Line 27-30: Have `columbo` iterate over the `Interactions` parsing the given command line arguments.
* Line 28: Provide the value of `patrick@example.com` for the question requesting the user's email address.
* Line 29: Select the value of `True` for the question asking the user if they like dogs.

!!! note
    If you omit the `args` parameter to `parse_args()` the values in `sys.argv` will be used.

## What's Next?

Read the [Usage Guide][usage-guide] for a more detailed descriptions of ways you can use `columbo`.

Read the [API Reference][api-reference] for specific information about all the functions and classes made available by
`columbo`.

[usage-guide]: usage-guide/fundamentals.md
[docs-main]: index.md
[api-reference]: api.md
