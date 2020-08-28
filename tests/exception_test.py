import pytest

from columbo._exception import (
    CliException,
    ColumboException,
    DuplicateQuestionNameException,
)


@pytest.mark.parametrize(
    "exception",
    [CliException("test-value", "--test-argument"), DuplicateQuestionNameException],
)
def test_all_custom_exception__inherits_from_custom_base(exception):
    with pytest.raises(ColumboException):
        raise exception
