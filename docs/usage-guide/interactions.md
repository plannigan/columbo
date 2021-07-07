# Interactions

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
    question and not present it to the user. See [Optional Questions & Branching][optional-questions] for more details.
* `cli_help`: Optional. A help message to be displayed for command line interface. See
    [CLI documentation][command-line] for more details. **Can't be dynamic**.
* `value_if_not_asked`: Optional. A value used as an answer if the question is not asked. **Can't be dynamic**.

### Basic Question

In addition to the arguments [mentioned above](#all-questions), `BasicQuestion` also accepts the following argument.

* `validator`: Optional. When given, the argument should be a function that checks if the user response is valid. Not
    providing this argument means that any value provided by the user will be accepted. See
    [Validators][validators] for more details.

### Choice

In addition to the arguments [mentioned above](#all-questions), `Choice` also accepts the following argument.

* `options`: The list of possible value the user can choose from.

### Confirm

`Confirm` doesn't take any additional arguments that weren't [mentioned above](#all-questions). However, the `default`
argument takes a `bool` instead of `str` and defaults to `False`.

[optional-questions]: optional-questions-and-branching.md
[command-line]: command-line.md
[validators]: validators.md
