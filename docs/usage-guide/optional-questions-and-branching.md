## Only Prompting Some Interactions

There are situations where a question should be asked some times, but not all the time. Or, a message should be displayed some times.
For example, a program that collects information about a user's 
pets should not ask the user for the dog's name and breed if the
user said they do not have a dog. If the user has a dog, the program
may want to display a special message. The `should_ask` argument that
is present on each interaction provides a way to achieve this functionality.

Similarly, `should_ask` can be used to provide branching paths to the user. An example of these branching paths is a
[Choose Your Own Adventure][choose-your-own-adventure] story. The story provides the reader with choices during the
adventure. These choices introduce diverging paths of interactions that may or may not join at the end.

!!! warning Be careful when skipping a question
    By default when `columbo` skips over a question, the `Answers` dictionary will **NOT** contain a key-value pair for the
    skipped question. If you want a skipped question to have a specific answer when skipped, you can do so using the
    `value_if_not_asked` kwarg as detailed in the section below.

### Optional Questions

The following is a basic example that has two optional questions that are not asked based on the answer to the first
question. It also has an optional message that is only displayed based on the answer to the first question.

```python
{!examples/optional_questions.py!}
```

If the user accepts the default answers for each of these questions, the output will be:

```python
{"has_dog": True, "dog_name": "Kaylee", "dog_breed": "Basset Hound"}
```

However, when the user answers the first question with "no", the output will be:

```python
{"has_dog": False}
```

Note that the `Answers` dictionary in the previous example has an answer to only the first question (there are no answers for the skipped questions).
The next section shows how to provide an answer for a skipped question.

#### Providing an Answer for Skipped Questions

To provide a specific answer used when a user skips a question, use the `value_if_not_asked` kwarg:

```python hl_lines="14 21"
{!examples/optional_questions_with_value_if_not_asked.py!}
```

If the user answers the first question with "no", the output will now be:

```python
{"has_dog": False, "dog_name": "n/a", "dog_breed": "n/a"}
```

Columbo will not ask the user for a dog name or breed, but the answers will have the values provided with the `value_if_not_asked` kwarg.

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

## Complicated Situations

While `should_ask` is capable of supporting complex combinations of optional questions and branching paths,
there are times where only using that functionality can make the code harder to read and understand. There
are [alternate strategies][advanced-usage] that can be used in order to make the code easier to follow.

[choose-your-own-adventure]: https://en.wikipedia.org/wiki/Choose_Your_Own_Adventure
[advanced-usage]: advanced-usage.md
