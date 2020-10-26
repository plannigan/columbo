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
    question and not present it to the user. The `Answers` dictionary will contain the value for each previous question
    that has been asked. Not providing this argument means that the question will always be asked. **When  `columbo`
    skips a question, no entry in the `Answers` dictionary will be created**.
* `cli_help`: Optional. A help message to be displayed for command line interface. See
    [CLI documentation](#command-line-interface) to more details. **Can't be dynamic**.

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
