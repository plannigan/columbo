# Columbo - 0.13.0

[![CI pipeline status](https://github.com/plannigan/columbo/workflows/CI/badge.svg?branch=main)][ci]
[![PyPI](https://img.shields.io/pypi/v/columbo)][pypi]
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/columbo)][pypi]
[![codecov](https://codecov.io/gh/plannigan/columbo/branch/main/graph/badge.svg)][codecov]

`columbo` provides a way to specify a dynamic set of questions to ask a user and get their answers.

`columbo`'s feature set allows a program to:

* Ask multiple types of questions:
    * Yes or No
    * Multiple choice
    * Open-ended
* Validate the response provided by the user
* Use answers from earlier questions:
    * As part of the text of a question
    * As part of the text of a default value
    * To decide if a question should be skipped or a message should be displayed
* Accept answers from the command line in addition to prompting the user

## Example

### User Prompts

The primary use of `columbo` is to define a sequence of interactions that are used to prompt a user to provide answers
using a terminal. Below is a sample which shows some ways this can be used.

```python
{!examples/index_user_prompts.py!}
```

Below shows the output when the user accepts the default values for most of the questions. The user provides a different
value for the email and explicitly confirms that they like dogs.

```text
Welcome to the Columbo example
Press enter to start
 
What is your name? [Patrick]:

What email address should be used to contact Patrick? [me@example.com]: patrick@example.com

How are you feeling today?
1 - 😀
2 - 😢
3 - 🥱
4 - 🤔
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
{!examples/index_command_line_answers.py!}
```
</details>

## Where to Start?

To learn the basics of how to start using `columbo`, read the [Getting Started][getting-started] page.

## Detailed Documentation

To learn more about the various ways `columbo` can be used, read the [Usage Guide][usage-guide] page.

## API Reference

To find detailed information about a specific function or class, read the [API Reference][api-reference].

[ci]: https://github.com/plannigan/columbo/actions
[pypi]: https://pypi.org/project/columbo/
[codecov]: https://codecov.io/gh/plannigan/columbo
[getting-started]: getting-started.md
[usage-guide]: usage-guide/fundamentals.md
[api-reference]: api.md
