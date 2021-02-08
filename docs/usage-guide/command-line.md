# Command Line Interface

In addition to providing an interactive terminal based UI to ask the user each question, `columbo` can also generate a
command line argument parser based on the list of `Interaction`s. When used in this manner, `Echo` & `Acknowledge` are
ignored. To produce a consistent command line argument format, `columbo` will do the following to the value of each
question's `name`:

* Make it lowercase.
* Replace space characters with dashes
* Replace underscore character with dash

For example:

| Original   | Result     |
| ---------- | ---------- |
| user       | user       |
| user_email | user-email |
| User Email | user-email |

!!! warning
    As a result of the transformation process, it is possible to have a sequence of questions with unique `name`s for the
    `Answers` dictionary, but cause a collision when creating command line arguments.

For `BasicQuestion` & `Choice`, the result will be preceded with two dashes (ex: `--user` or `--user-email`).

For `Confirm`, `columbo` produces two command lines arguments. After following the transformation rules, the command
line arguments will be `--{NAME}` & `--no-{NAME}` to explicitly specify `True` or `False`, respectively (ex:
`--likes-dogs` and `--no-likes-dogs`)

Since the argument parser must be constructed before receiving any user input, all `Question`s produce arguments.
`should_ask` is only considered when processing the given arguments.
