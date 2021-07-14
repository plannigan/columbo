# Development Guide

Welcome! Thank you for wanting to make the project better. This section provides an overview of repository
structure and how to work with the code base.

Before you dive into this, it is best to read:

* The whole [Usage Guide][usage-guide]
* The [Code of Conduct][code of conduct]
* The [Contributing][contributing] guide

## Docker

The Columbo project uses Docker to ease setting up a consistent development environment. The Docker documentation has
details on how to [install docker][install-docker] on your computer.

Once that is configured, the test suite can be run locally:

```bash
docker-compose run --rm test
```

If you want to be able to execute code in the container:

```bash
docker-compose run --rm devbox
(your code here)
```

In the devbox environment you'll be able to enter a python shell and import `columbo` or any dependencies.

## Debugging

The docker container has [pdb++][pdbpp-home] install that can be used as a debugger. (However, you are welcome to set up
a different debugger if you would like.)

This allows you to easily create a breakpoint anywhere in the code.

```python
def my_function():
    breakpoint()
    ...
```

When your the code, you will drop into an interactive `pdb++` debugger.

See the documentation on [pdb][pdb-docs] and [pdb++][pdbpp-docs] for more information.

## Testing

You'll be unable to merge code unless the linting and tests pass. You can run these in your container via:

```bash
docker-compose run --rm test
```

This will run the same tests, linting, and code coverage that are run by the CI pipeline. The only difference is that,
when run locally, `black` and `isort` are configured to automatically correct issues they detect.

Generally we should endeavor to write tests for every feature. Every new feature branch should increase the test
coverage rather than decreasing it.

We use [pytest][pytest-docs] as our testing framework.

### Stages

To customize / override a specific testing stage, please read the documentation specific to that tool:

1. [PyTest][pytest-docs]
2. [MyPy][mypy-docs]
3. [Black][black-docs]
4. [Isort][isort-docs]
4. [Flake8][flake8-docs]
5. [Bandit][bandit-docs]

## Validate Examples Used in Documentation

In the `docs/examples/` directory of this repo, there are example Python scripts which we use in our documentation.
You can validate that the examples run properly using:

```bash
docker-compose run --rm validateDocExamples
```

If the script fails (exits with a non-zero status), it will output information about the file that we need to fix.

Note that this script will output some content in the shell every time it runs.
Just because the script outputs content to the shell does *not* mean it has failed;
as long as the script finishes successfully (exits with a zero status), there are no problems we need to address.

## Building the Library

`columbo` is [PEP 517][pep-517] compliant. [build][build] is used as the frontend tool for building the library.
Setuptools is used as the build backend. `setup.cfg` contains the library metadata. A `setup.py` is also included to
support an editable install.

### Requirements

* **requirements.txt** - Lists all direct dependencies (packages imported by the library).
* **requirements-test.txt** - Lists all direct dependencies needed for development. This primarily covers dependencies
  needed to run the test suite & lints.

## Publishing the Package

TODO: The project currently only has parts of this process implemented. The CI pipeline does not currently publish the
wheel and source distribution to [PyPI][pypi]. For now, this must be done manually.

Once the package is ready to be released, there are a few things that need to be done:

1. Start with a local clone of the repo on the default branch with a clean working tree.
2. Run the version bump script with the appropriate part name (`major`, `minor`, or `patch`).
    Example: `docker-compose run --rm bump minor`
    
    This wil create a new branch, updates all affected files with the new version, and commit the changes to the branch.

3. Push the new branch to create a new pull request.
4. Get the pull request approved.
5. Merge the pull request to the default branch.
6. Double check the default branch has all the code that should be included in the release.
7. Create a new GitHub release. The tag should be named `vX.Y.Z` to match the new version number.

This will trigger the CI system to build a wheel and a source distributions of the package and push them to
[PyPI][pypi].

## Continuous Integration Pipeline

TODO: Add CI documentation.

[usage-guide]: usage-guide/fundamentals.md
[code of conduct]: https://github.com/wayfair-incubator/columbo/blob/main/CODE_OF_CONDUCT.md
[contributing]: https://github.com/wayfair-incubator/columbo/blob/main/CONTRIBUTING.md
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
