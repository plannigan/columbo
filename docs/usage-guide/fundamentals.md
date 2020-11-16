# Usage Guide

This section provides detailed descriptions of all the ways `columbo` can be used. If you are new to `columbo`, the
[Getting Started][getting-started] page provides a gradual introduction of the basic functionality with examples.

## Static vs Dynamic Values

Before diving into the specifics about each `Interaction` type, it is important to understand how `columbo` supports
both static and dynamic values. A static value is a value that is known when creating an `Interaction` instance.
Frequently this will be a value like a string literal, but that is not a requirement.

In contrast, a dynamic value is one which depends on one or more answer provided by the user from a previous question.
This is supported by accepting a function that takes an `Answers` dictionary as an argument and returns a value with
the type of that static value would have. For example, the static value for `message` is `str`. Therefore, tye dynamic
value would be a function that accepts `Answers` and returns a string (`Callable[[Answers],str]`).

In most cases, any argument to an `Interaction`'s constructor can be dynamic. This guide will explicitly mention when
the constructor requires an argument to be a static value.

## Detailed Sections

* [Interactions][interactions]
* [Optional Questions & Branching][optional-questions]
* [Validators][validators]
* [Command Line Interface][command-line]

[getting-started]: ../getting-started.md
[interactions]: interactions.md
[optional-questions]: optional-questions-and-branching.md
[validators]: validators.md
[command-line]: command-line.md
