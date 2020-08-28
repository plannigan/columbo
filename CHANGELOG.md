# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
