# Validators

## Context

`BasicQuestion` allows the user to provide arbitrary text as the answer to the question. However, there are frequently
constraints on what is considered a valid answer. Providing a `Validator` for the question allows `columbo` to verify
that the text provided by the user satisfies those constraints. If the answer is not valid, `columbo` will tell the user that
the answer is not valid and ask them to try again.

!!! Note Implicit Validators
    While `Choice` and `Confirm` do not expose a `validator` argument they still ensure that the answer is valid.
    A `Confirm` question will only continue when ++y++, ++n++, or ++enter++ are pressed. Any other keys will be ignored.
    A `Choice` question will only continue when ++enter++ is pressed if the input matches the number `columbo` assigned
    to one of the choices.

## Validator Structure

A `Validator` must be a function which has the following type signature: `Callable[[str, Answers], ValidationResponse]`[^1]. We'll walk through this signature explaining each part.

A `Validator` takes two arguments: a string (which is the response provided by the user to a question) and an `Answers` dictionary containing the answer for each previous question.

The `Validator` must return a `ValidationResponse` which is a type alias for: `Union[ValidationFailure, ValidationSuccess]`[^1]. Thus, a `Validator` must return either a `ValidationFailure` or a `ValidationSuccess` object. You should use a `ValidationSuccess` when the user's response is valid and `ValidationFailure` when the user's response is invalid. Both `ValidationFailure` and `ValidationSuccess` have a `valid` attribute that is `False` and `True`, respectively. A `ValidationFailure` requires that you provide an `error` which describes why the given value was invalid (`columbo` will display this message before asking users to answer the question again so users get some feedback about what they are doing wrong).

### Upgrading Validator Structure

The docs in this section detail how to upgrade a `Validator` from a columbo version < `0.10.0` to the newer `Validator` structure. Feel free to skip this section if it's not pertinent to you.

As described in footnote 1[^1], the desired response from a `Validator` has changed in version `0.10.0`. Previously, a `Validator` would return either an error message (as a string) if validation failed or `None` if the validation succeeded. To update a `Validator`, you should update the validator function to return `ValidationFailure` if validation fails and `ValidationSuccess` if the validation succeeds. The table below describes the old and new return values for different validation statuses. If you have questions or would like some clarification, please [raise an issue](https://github.com/wayfair-incubator/columbo/issues) and we'd be happy to help.

| Validation Status | Old Return Value (before `0.10.0`) | New Return Value (since `0.10.0`) |
| ----- | ----- | ----- |
| Failed | "Some error message" | ValidationFailure(error="Some error message") |
| Succeeded | None | ValidationSuccess() |

## Example Validator

Let's say we were asking for a user's email address.
The `Validator` below provides a simple check to see if
the email address seems valid[^2]. If the user's response doesn't contain an `@` character with at least one
word character on each side then the response is invalid and the user will have to
enter an email address again (hopefully a valid one this time).

```python
{!.examples/validators.py!}
```

[^1]:
    Technically, the type alias for a `Validator` is `Callable[[str, Answers], Union[ValidationResponse, Optional[str]]]` - the difference
    from the documentation above is that a `Validator` can return either a `ValidationResponse` *or* `Optional[str]`. Returning `Optional[str]`
    is NOT recommended as we have deprecated `Optional[str]` as a valid return type in version `0.10.0` and will be removing this capability in version `1.0.0`.
    
[^2]:
    The regular expression for checking for an RFC 822 compliant email address is
    [overly complicated](http://www.ex-parrot.com/~pdw/Mail-RFC822-Address.html). Additionally, that only ensures that the
    text is valid. It does not confirm if the host will accept emails sent to that address or if the user is the owner of
    the email address.
