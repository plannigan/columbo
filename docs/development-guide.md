# Development Guide

Welcome! Thank you for wanting to make the project better. This section provides an overview of repository
structure and how to work with the code base.

Before you dive into this, it is best to read:

* The whole [Usage Guide][usage-guide]
* The [Code of Conduct][code of conduct]
* The [Contributing][contributing] guide

## Project & Environment management

The Columbo project uses [Hatch][hatch] to manage various aspects of the project's development life cycle. This
includes: 
* building the distributions
* controlling python environments
* executing common development tasks

`requirements-bootstrap.txt` can be used to install a version of `hatch` that is known to work with the project.

### Environments

There are three distinct environments that `hatch` manages:

* `default`:  Testing or linting the project code
* `docs`: Generating documentation for the project
* `bump`: Releasing a new version of the library


### Docker

For those that wan to work in an even more consistent development environment, there is a Dockerfile that defines an
images that is isolated from the host machine. The Docker documentation has details on how to
[install docker][install-docker] on your computer.

Once that is configured, you will be able to execute code in the container:

```bash
docker-compose run --rm devbox
(your code here)
```

The devbox container also utilizes `hatch` to manage the python environments. So you will be able to run the same
scripts detailed below.



the test suite can be run locally:

```bash
docker-compose run --rm test
```


## Testing

You'll be unable to merge code unless the linting and tests pass. Therefore it is important to execute that
functionality locally before pushing changes. This is so common, that it has a dedicated `hatch` scripts.

```bash
hatch run check
```

This will run the same tests, linting, and code coverage that are run by the CI pipeline. The only difference is that,
when run locally, `black` and `isort` are configured to automatically correct issues they detect.

!!! tip Implicit Validators
    Since this is so common, there is also a shorthand for running this in the container

    ```bash
    docker-compose run --rm check
    ```

### Writing Tests

Generally we should endeavor to write tests for every feature. Every new feature branch should increase the test
coverage rather than decreasing it.

We use [pytest][pytest-docs] as our testing framework.

### Linting Tools

To customize one of the linting tools, please read the documentation specific to that tool:

1. [MyPy][mypy-docs]
2. [Black][black-docs]
3. [Isort][isort-docs]
4. [Flake8][flake8-docs]
5. [Bandit][bandit-docs]

## Validate Examples Used in Documentation

In the `docs/examples/` directory of this repo, there are example Python scripts which we use in our documentation.
You can validate that the examples run properly using:

```bash
hatch run test-docs-examples
```

If the script fails (exits with a non-zero status), it will output information about the file that we need to fix.

Note that this script will output some content in the shell every time it runs. Just because the script outputs content
to the shell does **not** mean it has failed; as long as the script finishes successfully (exits with a zero status),
there are no problems we need to address.

## Building the Library

`columbo` is [PEP 517][pep-517] compliant. [build][build] is used as the frontend tool for building the library.
`hatching` is used as the build backend. The libray metadata is defined in `pyproject.toml`.

### Dependencies

* **Direct Library Dependencies** - These are packages imported by the library. They are specified under
    `project.dependencies` in `pyproject.toml`. These should be version ranges that specify the minimum and maximum
    version supported for each dependency. A conservative approach to maximum version is used that disallows the next
    major version so that an incompatible version of a direct dependency will not be considered valid. 
* **Direct Development Dependencies** - These all direct dependencies needed for development. This things like
    non-library dependencies imported by tests, linting tools, and documentation tools. They are specified in
    `pyproject.toml` under the specific `hatch` environment. 

## Publishing a New Version

Once the package is ready to be released, there are a few things that need to be done:

1. Start with a local clone of the repo on the default branch with a clean working tree.
2. Have an environment configured for Python 3.9 or later.
3. Perform the version bump part name (`major`, `minor`, or `patch`).

    Example: `hatch run bump:it by minor`
    
    This wil create a new branch, updates all affected files with the new version, commit the changes to the branch, and 
    push the branch.

4. Create a new pull request for the pushed branch.
5. Get the pull request approved.
6. Merge the pull request to the default branch.

Merging the pull request will trigger a GitHub Action that will create a new release. The creation of this new
release will trigger a GitHub Action that will to build a wheel & a source distributions of the package and push them to
[PyPI][pypi].

!!! warning
    The action that uploads the files to PyPI will not run until a repository maintainer acknowledges that the job is
    ready to run. This additional layer of manual action ensures that distribution are not unintentionally published. 

In addition to uploading the files to PyPI, the documentation website will be updated to include the new version. If the
new version is a full release, it will be made the new `latest` version.

## Continuous Integration Pipeline

The Continuous Integration (CI) Pipeline runs to confirm that the repository is in a good state. It will run when 
someone creates a pull request or when they push new commits to the branch for an existing pull request. The pipeline
runs multiple different jobs that helps verify the state of the code.

This same pipeline also runs on the default branch when a maintainer merges a pull request.

### Lints

The first set of jobs that run as part of the CI pipline are linters that perform static analysis on the code. This
includes: [MyPy][mypy-docs], [Black][black-docs], [Isort][isort-docs], [Flake8][flake8-docs], and [Bandit][bandit-docs].

### Tests

The next set of jobs run the unit tests using [PyTest][pytest-docs]. The pipeline runs the tests cases across each
supported version of Python to ensure compatibility.

For each run of the test cases, the job will record the test results and code coverage information. The pipeline uploads
the code coverage information to [CodeCov][codecov] to ensure that a pull request doesn't significantly reduce the total
code coverage percentage or introduce a large amount of code that is untested.

### Distribution Verification

The next set of jobs build the wheel distribution, installs in into a virtual environment, and then runs Python to
import the library version. This works as a smoke test to ensure that the library can be packaged correctly and used.
The pipeline runs the tests cases across each supported version of Python to ensure compatibility.

### Documentation

The remaining jobs are all related to documentation.

* A job runs each of the code examples that are used in the documentation to verify they produce the expected results.
* A job builds the documentation in strict mode so that it will fail if there are any errors. The job records the
    generated files so that the documentation website can be viewed in its rendered form.
* When the pipeline is running as a result of a maintainer merging a pull request to the default branch, a job runs that
    publishes the current state of the documentation to as the `dev` version. This will allow users to view the state of
    the documentation as it has changed since a maintainer published the `latest` version.


[usage-guide]: usage-guide/fundamentals.md
[code of conduct]: https://github.com/plannigan/columbo/blob/main/CODE_OF_CONDUCT.md
[contributing]: https://github.com/plannigan/columbo/blob/main/CONTRIBUTING.md
[hatch]: https://hatch.pypa.io/latest/
[install-docker]: https://docs.docker.com/install/
[pdbpp-home]: https://github.com/pdbpp/pdbpp
[pdb-docs]: https://docs.python.org/3/library/pdb.html
[pdbpp-docs]: https://github.com/pdbpp/pdbpp#usage
[pytest-docs]: https://docs.pytest.org/en/latest/
[mypy-docs]: https://mypy.readthedocs.io/en/stable/
[black-docs]: https://black.readthedocs.io/en/stable/
[isort-docs]: https://pycqa.github.io/isort/
[flake8-docs]: http://flake8.pycqa.org/en/stable/
[bandit-docs]: https://bandit.readthedocs.io/en/stable/
[sem-ver]: https://semver.org/
[pep-517]: https://www.python.org/dev/peps/pep-0517
[build]: https://pypa-build.readthedocs.io/
[pypi]: https://pypi.org/project/columbo/
[codecov]: https://about.codecov.io/
