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
{!examples/optional_questions.py!}
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
the `should_ask` function was provided to determine if the question should be skipped or not. The branching aspect comes from there being at
least two sets of optional questions. Each set has a `should_ask` argument that checks for a different state for a
single answer. In this way, only one of the sets of optional questions will ever be asked.

The following is an example of a short story that has two divergent paths that join at the end. Each individual question
isn't different from the optional questions [demonstrated above](#optional-questions). The program achieves the
branching paths by supplying different `should_ask` values that will never both evaluate to `True`.

```python
{!examples/branching_story.py!}
```

The import thing to note in the example above is that the `Answers` dictionary can have a key-value pair for
`has_key` or `has_hammer`, not both.

[choose-your-own-adventure]: https://en.wikipedia.org/wiki/Choose_Your_Own_Adventure