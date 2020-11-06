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
