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

A question that is part of a branching path is very similar to an optional question. It is still a question where
the `should_ask` function was provided to determine if the question should be skipped or not. The branching aspect comes there being at
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

[choose-your-own-adventure]: https://en.wikipedia.org/wiki/Choose_Your_Own_Adventure
