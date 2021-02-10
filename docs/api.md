# Reference

## Type Aliases

`columbo` uses type aliases heavily to simplify the annotations for the functions provided by the
library. The following table defines the aliases that are used.

| Alias | Value |
| ----- | ----- |
| `Answer` | `Union[bool, str]` |
| `Answers` | `Mapping[str, Answer]` |
| `Interaction` | `Union[Echo, Acknowledge, Question]` |
| `MutableAnswers` | `MutableMapping[str, Answer]` |
| `OptionList` | `List[str]` |
| `Possible`* | `Union[T, Literal[_Sentinel]]` |
| `ShouldAsk` | `Callable[[Answers], bool]` |
| `StaticOrDynamicValue` | `Union[V, Callable[[Answers], V]]` |
| `ValidationResponse` | `Union[ValidationSuccess, ValidationFailure]` |
| `Validator` | `Callable[[str, Answers],  Union[ValidationResponse,  Optional[str]]]` |

!!! note
    `Possible` is a special construct used in `copy()` methods to indicate that a value was not
    provided. `Possible` & `_Sentinel` are not exposed by `columbo`, but are documented here for
    completeness.


## Interactions

::: columbo.Acknowledge

::: columbo.BasicQuestion

::: columbo.Choice

::: columbo.Confirm

::: columbo.Echo

::: columbo.Question

## Functions

::: columbo.format_cli_help

::: columbo.get_answers

::: columbo.parse_args

## Exceptions

::: columbo.CliException

::: columbo.ColumboException

::: columbo.DuplicateQuestionNameException
