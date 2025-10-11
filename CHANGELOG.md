# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Support for Python `3.13`

### Removed

- Support for Python version `3.8` & `3.9`.

 ### Internal
- 
- Use license expression metadata ([PEP 639][pep-639])

## [0.14.0] - 2023-12-02

### Added

- Support for Python `3.11` and  `3.12`
- Support for `no_user_input` in `Acknowledge.display()` and `Echo.display()`.

### Fixed

- Raise `ValueError` when dynamic value returns the wrong type.
- `BasicQuestion` validates `value_if_not_asked` using the `Validator` if provided.
- `Choice` validates `value_if_not_asked` for dynamic options that depend on the current `Answers`.

### Removed

- Support for Python version `3.7`.
- `tests/` directory no longer included in distributions.

### Internal

- Use [hatch][hatch] for build backend.

## [0.13.0.post1] - 2023-05-12

### Changed

- Update project metadata for ownership change.

### Internal

- Use OpenID Connect as a [trusted publisher][trusted-publishers] for uploading releases.

## [0.13.0] - 2022-10-24

### Added

- Ability for `Choice` to display a custom message instead of the value being selected. This includes a new type alias (`Options`) which supports both the `Mapping[str, str]` and `List[str]` forms. ([#389](https://github.com/plannigan/columbo/pull/389))

### Deprecated

- The `OptionList` type for `Choice` in favor of `Options` ([#389](https://github.com/plannigan/columbo/pull/389))

### Fixed

- All exceptions raised by `columbo` listed in the docstrings. Improved phrasing to make messaging consistent.

## [0.12.0] - 2022-09-05

### Changed

- Expand acceptable versions of `typing-extensions` to include v4

### Added

- Python version `3.10` tested during CI
- Python version `3.10` added to package classifiers
- `should_ask` keyword argument for `Echo` and `Acknowledge` interactions ([#356](https://github.com/plannigan/columbo/issues/356))

### Changed

- `BasicQuestion.ask()` will only evaluate dynamic values for the prompt message and default value once instead of
  repeatedly when the response was invalid.

### Fixed

- Prevent infinite loop when the default value for a `BasicQuestion` does not satisfy the `Validator` and `no_user_input`
  was set to `True`. Now raises a `ValueError` when this situation is detected.

  The intent was that the default value would always satisfy the `Validator`, but that was not enforced or explicitly
  documented.

### Removed

- Support for Python version `3.6`.

## [0.11.0] - 2021-08-04

### Added

- `value_if_not_asked` kwarg for `Question` interactions to set a value if the question is not asked ([#169](https://github.com/plannigan/columbo/pull/169))

## [0.10.1] - 2021-02-26

### Fixed

* `dataclasses` was not listed as a dependency for versions of Python < 3.7

### Removed

- Support for `Validator`s that return `Optional[str]`

## [0.10.0] - 2021-02-18

### Added

* Python 3.9 support ([#73](https://github.com/plannigan/columbo/pull/73))
* New `Validator` signature ([#37](https://github.com/plannigan/columbo/issues/37))

### Changed

* Improved validation for converting question names to command line arguments ([#82](https://github.com/plannigan/columbo/pull/82))

### Deprecated

* Support for `Validator`s that return `Optional[str]` ([#39](https://github.com/plannigan/columbo/issues/39))

## [0.9.0] - 2020-12-18

First public release. No code changes from v0.8.0.

## [0.8.0] - 2020-02-17

### Added

* All `Interaction`s gained a `copy()` method to allow for creating slightly altered instances of an existing
    `Interaction`.
* `parse_args()` and `format_cli_help()` accept an optional `parser_name` to be displayed in errors and help text.

### Changed

* Stop producing universal wheels.

### Fixed

* `StaticOrDynamicValue` enforces that the result of the callable must be the same type as the static type.

### Removed

* `DynamicValue` is no longer exposed as a type alias.

## [0.7.0] - 2020-02-10

### Added

* `format_cli_help()` function to produce CLI help text.

### Changed

* Type hints on public API. Be more restrictive when functions should not be making mutations. Be less restrictive when
    functions don't rely on specific implementations.

### Fixed

* `CliException` inherits from `ColumboException`.
* Raise `DuplicateQuestionNameException` if a list of interactions contains multiple questions with the same name. The
    same exception is also raised when an existing answers dictionary already contains a name used by a given questions.

## [0.6.0] - 2020-01-13

### Added

* `parse_args()` function now accepts an initial dictionary of `answers`.

### Fixed

* Expose additional type hints used in signatures of public API.

## [0.5.0] - 2020-01-06

### Added

* `exit_on_error` added to `parse_args()` as an optional argument. When `False`, the function will raise an exception
    instead of exiting the application if the arguments can't be parsed.

### Changed

* Rewrote Columbo example script text.
* Made example script stand alone.
* Test against each supported python version in CI.
* Add support for python 3.8.
* Use `prompt-toolkit` for user interaction instead of `click`.
* Mark `user_io` sub-module as private.
* Expose exception types raised by library.

### Fixed

* Add `Args` class that `user_io` relies on.
* Explicit type is required for `singledispatch` on python 3.6.
* Specify minimum supported python version.

### Removed

* Ability to run the module as an application.
* Dynamic loading of questions from a file.

## [0.4.0] - 2019-12-17

### Changed

* return type of `Validator` return type updated from `bool` to `Optional[str]`
* `is_valid` function updated to `validate`, return type updated from `bool` to `Optional[str]`

### Fixed

* `BasicQuestion` constructor now respects the `validator` argument
  * If `validator` callable provided, question will be asked until validator returns `True`

## [0.3.0] - 2019-11-21

* `get_answers()` takes optional `answers` dict, appending new answers to this as opposed to new dictionary

## [0.2.0] - 2019-11-08

### Added

* `get_answers()` takes list of interactions and builds dict of answers, handling user I/O

## [0.1.0] - 2019-10-15

Initial Release

[pep-639]: https://peps.python.org/pep-0639/
[trusted-publishers]: https://docs.pypi.org/trusted-publishers/
[hatch]: https://hatch.pypa.io/latest/
