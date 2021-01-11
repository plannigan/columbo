from typing import Optional


class ColumboException(Exception):
    """Base exception for exceptions raised by Columbo"""


class DuplicateQuestionNameException(ColumboException):
    """Multiple questions use the same name."""


class CliException(ColumboException):
    """An error occurred while processing command line arguments."""

    @classmethod
    def invalid_value(
        cls, value: str, argument_name: str, error_message: Optional[str] = None
    ) -> "CliException":
        formatted_error_message = f": {error_message}" if error_message else ""
        return cls(
            f"'{value}' is not a valid value for '{argument_name}'{formatted_error_message}"
        )
