# Advanced Usage

The [Overview][overview] and [Getting Started][getting-started] pages show simplified examples
of how to use `columbo`. These examples have consisted of:

* statically defined list of `Interaction`s which are then passed to [get_answers()][get-answers] or
  [parse_args()][parse-args].
* dynamic values that were deterministic based on specific inputs

However, there are times when the actual situation is more complicated than those examples. To handle these situations
there are alternate strategies that can be utilized.

This page intends to demonstrate some situations that are more complicated and suggest alternative approaches to solving
them. This page may not cover every possible situation. The alternate approaches demonstrated on this page maybe suited
for more than just the example situation each are paired with. But they should help think about alternate approaches
when things get complicated.

## Dynamic Values

Each `Interaction` supports [dynamic values][dynamic-values]. This can be useful when things are deterministic.
However, if the `options` for a `Choice` are retrieved from an external server, it can be hard to implement the
conditional logic. In the following example, the data retrieval logic is encapsulated into a function that is called
ahead of time. This allows the application to handle retrival errors or other validation before utilizing `columbo` to
prompt the user for their selection. Additional, `default` can be set to a value that is known to exist in the options
list, even without prior knowledge of the options. 

```python linenums="1"
{!examples/alternate_dynamic_options.py!}
```

## Optional Questions

Each `Interaction` can be [optional][optional]. However, there are times where a number of those `Interaction`s all
rely on the same check to determine if the questions should be asked. One strategy to achieve this is to have same
function could be passed to `should_ask` for each `Interaction`. An alternate strategy is to not limit the code to a
single list of `Interaction`s. [get_answers()][get-answers] and [parse_args()][parse-args] can be called multiple times
within an application. Both functions can be passed the resultant `Answers` instance returned from the first call in
order to keep the answers context moving forward.

```python linenums="1"
{!examples/alternate_optional_questions.py!}
```

## Branching Paths

The fact that each `Interaction` can be [optional][optional] can be used to support [branching paths][branching].
However, for paths the diverge significantly, it can be hard to keep track of how the `should_ask` values interact.
Similar to [optional questions][optional-questions], a strategy to address this is to not limit the code to a single
list of `Interaction`s. [get_answers()][get-answers] and [parse_args()][parse-args] can be called multiple times within
an application. This allows the application to manage the branching directly. Both functions can be passed the resultant
`Answers` instance returned from the first call in order to keep the answers context moving forward.


```python linenums="1"
{!examples/alternate_branching_story.py!}
```

## Direct Interaction

[get_answers()][get-answers] provides a helpful functionality for iterating over multiple `Interaction`s and collecting
the responses. However, it is implemented using methods that are directly available on each `Interaction` object. If an
application wants full control over the flow of the user prompts, [ask()][ask] and [display()][display] can be called as
needed.

[overview]: ../index.md
[getting-started]: ../getting-started.md
[get-answers]: ../api.md#columbo.get_answers
[parse-args]: ../api.md#columbo.parse_args
[dynamic-values]: ../getting-started.md#dynamic-values
[optional]: optional-questions-and-branching.md#optional-questions
[branching]: optional-questions-and-branching.md#branching-paths
[optional-questions]: #optional-questions
[ask]: ../api.md#columbo._interaction.BasicQuestion.ask
[display]: ../api.md#columbo._interaction.Echo.display
