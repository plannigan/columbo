# type: ignore
import ast
import re

import setuptools

_version_re = re.compile(r"__version__\s+=\s+(.*)")
with open("columbo/__init__.py", "rb") as f:
    _match = _version_re.search(f.read().decode("utf-8"))
    if _match is None:
        print("No version found")
        raise SystemExit(1)
    version = str(ast.literal_eval(_match.group(1)))


setuptools.setup(
    name="columbo",
    version=version,
    url="https://github.com/wayfair-incubator/columbo",
    author="Patrick Lannigan",
    author_email="plannigan@wayfair.com",
    description="Specify a dynamic set of questions to ask a user and get their answers.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]
    ),
    package_data={"columbo": ["py.typed"]},
    python_requires=">=3.6",
    install_requires=["prompt-toolkit~=3.0"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
