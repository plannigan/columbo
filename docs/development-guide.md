# Development Guide

Welcome! Thanks for wanting to make the project better. This section provides an overview of the
project structure and how to work with the code base.

Before diving into this, it is best to read:

* The whole [Usage Guide][usage-guide]
* The [Code of Conduct][code-of-conduct]

## How to Contribute

There are lots of ways to contribute to the project.

* [Report a bug][bug]
* [Request a new feature][feature]
* Create a pull request that updates the code
* Create a pull request that updates the documentation
* Sponsor development of the project
    <iframe
     src="https://github.com/sponsors/plannigan/button"
     title="Sponsor plannigan"
     height="32" width="114" style="border: 0; border-radius: 6px; margin-bottom: -11px;">
    </iframe>

### Creating a Pull Request

Before creating a pull request, please first discuss the intended change by creating a new issue or
commenting on an existing issue.

#### Code Contributions

Code contributions should include test for the change. For a bug fix, there should be a new test
case that demonstrates the issue that was reported (which the contribution addresses). For a new
feature, new test cases should cover the new code, while also and checking for edge cases.
Generally, the goal is that each change should increase the code coverage rather than decreasing
it. ([more details][testing])

Pull requests will need to pass all tests and linting checks that are part of the [CI pipeline][ci]
before they can be merged.

Significant changes should update the [documentation][documentation] with details about how to use
the provided functionality.

Changes that affect users of `columbo` must include an entry the [CHANGELOG][changelog] under
the `[Unrelease]` header. Once a new release is ready to be published, a version number will be
assigned in place of this header ([more details][releasing]). If a logical change is broken into
multiple pull requests, each pull request does not need to add a new entry. For significant changes
that affect the development of the project, as apposed to users of `columbo`, the `Internal`
section can be used.

## Project & Environment management

The `columbo` project uses [Hatch][hatch] to manage various aspects of the project's development life cycle. This
includes:

* building the distributions
* controlling python environments
* executing common development tasks

`requirements-bootstrap.txt` can be used to install a version of `hatch` that is known to work with the project.

### Dependencies

* **Direct Library Dependencies** - These are packages imported by the library. They are specified under
    `project.dependencies` in `pyproject.toml`. These should be version ranges that specify the minimum and maximum
    version supported for each dependency. A conservative approach to maximum version is used that disallows the next
    major version so that an incompatible version of a direct dependency will not be considered valid. 
* **Direct Development Dependencies** - These all direct dependencies needed for development. This things like
    non-library dependencies imported by tests, linting tools, and documentation tools. They are specified in
    `pyproject.toml` under the specific `hatch` environment. 

### Environments

There are three distinct environments that `hatch` manages:

* `default`:  Testing or linting the project code
* `docs`: Generating documentation for the project
* `bump`: Releasing a new version of the library

### Docker

For those that want to work in an even more consistent development environment, there is a Dockerfile that defines an
images that is isolated from the host machine. The Docker documentation has details on how to
[install docker][install-docker] on the computer being used.

Once that is configured, it is possible to execute code in the container:

```bash
docker compose run --rm devbox
(custom code here)
```

The devbox container also utilizes `hatch` to manage the python environments. So the scripts detailed below can be used
from within the container.

## Testing

Code contributions won't be merged unless the linting and tests pass. Therefore, it is important to execute that
functionality locally before pushing changes. This is so common, that it has a dedicated `hatch` script.

```bash
hatch run check
```

This will run the same tests, linting, and code coverage that are run by the CI pipeline. The only difference is that,
when run locally, `black` and `isort` are configured to automatically correct issues they detect.

!!! tip
    Since this is so common, there is also a shorthand for running this in the container

    ```bash
    docker compose run --rm check
    ```

### Writing Tests

Generally contributors should endeavor to write tests for every feature. Every new feature branch should increase the
test coverage rather than decreasing it.

The project uses [pytest][pytest-docs] as the testing framework.

#### Testing Fixtures

In addition to the fixtures provided by `pytest`, the project also utilizes a plugin that
provide a fixture that integrates into `pytest`.

* [pytest-mock][pytest-mock] - Exposes [unitest.mock][unittest-mock].

### Linting Tools

To customize one of the linting tools, please read the documentation specific to that tool:

* [MyPy][mypy-docs]
* [Black][black-docs]
* [Isort][isort-docs]
* [Flake8][flake8-docs]
* [Bandit][bandit-docs]

## Documentation

The project uses [mkdocs][mkdocs] as static site generator. The [mkdocs-material][mkdocs-material]
theme is used to control the look and feel of the website. [mike][mike] is used to manage
documentation for each version of `hyper-bump-it`.

The documentation can be built locally. The following command will build the documentation and
start a local server to view the rendered documentation.

```bash
hatch run docs:serve
```

### Validate Examples Used in Documentation

In the `docs/examples/` directory of this repo, there are example Python scripts which are used in the documentation.
The below command can be used to validate that the examples run properly:

```bash
hatch run test-docs-examples
```

If the script fails (exits with a non-zero status), it will output information about the file that we need to fix.

!!! warning
    This script will output some content in the shell every time it runs. Just because the script outputs content
    to the shell does **not** mean it has failed; as long as the script finishes successfully (exits with a zero status),
    there are no problems that need to address.

## Building the Library

`columbo` is [PEP 517][pep-517] compliant. [build][build] is used as the frontend tool for building the published
distributions of the library.
`hatching` is used as the build backend. The libray metadata is defined in `pyproject.toml`.

## Publishing a New Version

Once the package is ready to be released, there are a few things that need to be done:

1. Start with a local clone of the repo on the default branch with a clean working tree.
2. Perform the version bump part name (`major`, `minor`, or `patch`).

    Example: `hatch run bump:it by minor`
    
    This wil create a new branch, updates all affected files with the new version, commit the changes to the branch, and 
    push the branch.

3. Create a new pull request for the pushed branch.
4. Get the pull request approved.
5. Merge the pull request to the default branch.

Merging the pull request will trigger a GitHub Action that will create a new GitHub release. The creation of this new
release will trigger a GitHub Action that will to build a wheel & a source distributions of the package and push them to
[PyPI][pypi].

!!! warning
    The action that uploads the files to PyPI will not run until a repository maintainer acknowledges that the job is
    ready to run. This additional layer of manual action ensures that distribution are not unintentionally published. 

In addition to uploading the files to PyPI, the documentation website will be updated to include the new version. If the
new version is a full release, it will be made the new `latest` version.

## Continuous Integration Pipeline

The Continuous Integration (CI) Pipeline runs to confirm that the repository is in a good state. It
will run when:

* a pull request is created
* new commits are pushed to the branch for an existing pull request
* a maintainer merges a pull request to the default branch

Pull requests will need to pass all tests and linting checks that are part of the CI pipeline
before they can be merged.

### Lints

The first set of jobs that run as part of the CI pipline are linters that perform static analysis on the code
([more details][linting]).

### Tests

The next set of jobs run the unit tests ([more details][testing]). The pipeline runs the tests cases across each
supported version of Python to ensure compatibility.

For each run of the test cases, the job will record the test results and code coverage information. The pipeline uploads
the code coverage information to [CodeCov][codecov] to ensure that a pull request doesn't significantly reduce the total
code coverage percentage or introduce a large amount of code that is untested.

### Distribution Verification

The next set of jobs perform a basic smoke test to ensure that the library can be packaged correctly and used. The
sdist and wheel distributions are built and installs in into a virtual environment. Python is then run to
import the library version. This is done across each supported version of Python to ensure compatibility.


### Documentation Building

When running as part of a pull request, the documentation is build in strict mode so that it will
fail if there are any errors. The job bundles the generated files into an artifact so that the
documentation website can be viewed in its rendered form.

When the pipeline is running as a result of a maintainer merging a pull request to the default
branch, a job runs that publishes the current state of the documentation to as the `dev` version.
This will allow users to view the "in development" state of the documentation with any changed that
have been made since a maintainer published the `latest` version.

### Renovate Configuration Lint

[Renovate][renovate] is used to automate the process of keeping project dependencies up to date.
A small job that confirms that the configuration is valid.

[usage-guide]: usage-guide/fundamentals.md
[code-of-conduct]: https://github.com/plannigan/columbo/blob/main/CODE_OF_CONDUCT.md
[bug]: https://github.com/plannigan/columbo/issues/new?labels=bug&template=bug_report.md
[feature]: https://github.com/plannigan/columbo/issues/new?labels=enhancement&template=feature_request.md
[testing]: #testing
[ci]: #continuous-integration-pipeline
[documentation]: #documentation
[changelog]: changelog.md
[releasing]: #publishing-a-new-version
[hatch]: https://hatch.pypa.io/latest/
[install-docker]: https://docs.docker.com/install/
[pytest-docs]: https://docs.pytest.org/en/latest/
[pytest-mock]: https://pytest-mock.readthedocs.io
[unittest-mock]: https://docs.python.org/3/library/unittest.mock.html
[mypy-docs]: https://mypy.readthedocs.io/en/stable/
[black-docs]: https://black.readthedocs.io/en/stable/
[isort-docs]: https://pycqa.github.io/isort/
[flake8-docs]: http://flake8.pycqa.org/en/stable/
[bandit-docs]: https://bandit.readthedocs.io/en/latest/
[mkdocs]: https://www.mkdocs.org/
[mkdocs-material]: https://squidfunk.github.io/mkdocs-material/
[mike]: https://github.com/jimporter/mike
[pep-517]: https://www.python.org/dev/peps/pep-0517
[build]: https://pypa-build.readthedocs.io/
[pypi]: https://pypi.org/project/columbo/
[linting]: #linting-tools
[codecov]: https://app.codecov.io/gh/plannigan/hyper-bump-it
[renovate]: https://docs.renovatebot.com/
