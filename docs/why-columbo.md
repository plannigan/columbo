# Why Columbo?

`columbo` started as an internal library used at [Wayfair][wayfair] by the Python Platforms team. It is now an
interdependently maintained open source project with the hope that it will provide benefit from the greater Python
community.

## What problem did Columbo initially solve?

One of the primary resources the Python Platforms team provided to Wayfair engineers was a set of project templates. This
allowed an engineering team to hit the ground running when starting a new HTTP application or Python package. The templates
contained best-practice patterns and allow developers to initialize and deploy a new application to production in minutes.

The project templates used [Cookiecutter][cookiecutter] in order to generate the files that will be used in the new
project. While Cookiecutter makes many things easy for maintainers of a template, the terminal user interface it
provides has a few issues:

* The text Cookiecutter presents to the user is also the name used to access the value within the template. This can
    make it hard for a user to know exactly what information the template is asking for.
* Cookiecutter always prompts the user for a value for every item defined by the template. Our templates have optional
    features that need additional information when used. When a user chooses not to use a given feature, they are still
    prompted to provide a value for the items that will not be used when generating files.
* Cookiecutter does not support validating given values when the user prompting the user to provide input. If a
    template requires the value for the first item to be a number, the user will be prompted for values for the
    remaining items. When the validation error occurs, the user always needs to start again from scratch.

Cookiecutter can be executed programmatically by passing in a dictionary of values. This allows `columbo` to handle the
user prompts resolving the issues we experienced, while still using Cookiecutter under the covers. With this pattern,
all project templates managed by language platform teams at Wayfair benefited from the user experience of working with
Cookiecutter templates.

## Alternatives

`columbo` is not the only library that exists which provides a way to codify prompting a user for answers to a set of
questions. This section compares `columbo` with some libraries which were created to achieve this task.

### PyInquirer

[PyInquirer][pyinquirer] was a major inspiration in the development of `columbo`. `PyInquirer` supports optional questions
and validation in similar way to how `columbo` supports those features.

`PyInquirer` has some features that `columbo` does not. It has some additional interaction types like selecting multiple
options from a list and using an external editor to provide a long form response. It also exposes more rendering options
of [prompt-toolkit][prompt-toolkit], which is used internally by both libraries.

`columbo` has some features that PyInquirer does not. `PyInquirer` does not support dynamic values as arguments used to
construct a question. Additionally, PyInquirer does not provide an option to parse command line arguments as answers to
a set of questions.

The primary reason why we chose to create `columbo` instead of using `PyInquirer` was that the project was still using
version 1 of `prompt-toolkit` while the maintainers of that library were preparing to release version 3[^1].
Additionally, the library uses an un-typed dictionary to describe each question, which can make it easier to make
configuration mistakes.

### python-inquirer

[python-inquirer][python-inquirer] is similar to `columbo` in that they both support dynamic values, validation and
optional questions. They also both use classes to represent interactions.

`python-inquirer` has some features that `columbo` does not. It has some additional interaction types like selecting
multiple options from a list and using an external editor to provide a long form response. It also exposes more
rendering options of [blessed][blessed].

`columbo` has some features that `python-inquirer` does not. `python-inquirer` does not provide an option to parse
command line arguments as answers to a set of questions or have interactions that do not store an answer. Additionally,
`colombo`'s API is fully type annotated, while `python-inquirer`'s API is not.

### questionary

[questionary][questionary] is similar to `columbo` in that they both support validation, optional questions, and use
classes to represent interactions[^2]. The API's for both libraries are fully type annotated.

`questionary` has some features that `columbo` does not. It has some additional interaction types like supporting tab
completion for some answers. It also exposes more rendering options of [prompt-toolkit][prompt-toolkit], which is used
internally by both libraries. `questionary` can also ask questions asynchronously.

`columbo` has some features that `questionary` does not. `questionary` does not support dynamic values as arguments used
to construct a question or provide an option to parse command line arguments as answers to a set of questions.


[^1]:
    At the time of writing this document (February 2021), the PyInquirer repo has been updated to use version 3 of
    prompt-toolkit, but a new release has not been published to PyPi.
[^2]:
    Dynamic optional questions requires questions to be [specified using a dictionary][questionary-dynamic-optional]
    instead of the class representation.

[wayfair]: https://www.wayfair.com/
[cookiecutter]: https://cookiecutter.readthedocs.io/
[pyinquirer]: https://github.com/CITGuru/PyInquirer
[prompt-toolkit]: https://python-prompt-toolkit.readthedocs.io/
[python-inquirer]: https://magmax.org/python-inquirer/
[blessed]: https://blessed.readthedocs.io/
[questionary]: https://questionary.readthedocs.io/
[questionary-dynamic-optional]: https://questionary.readthedocs.io/en/stable/pages/advanced.html#create-questions-from-dictionaries
