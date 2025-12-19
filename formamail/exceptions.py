"""
FormaMail SDK Exceptions
"""


class FormamailError(Exception):
    """Base exception for FormaMail SDK errors."""

    def __init__(self, message: str, code: str = "UnknownError", status_code: int = 0):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)

    def __repr__(self) -> str:
        return f"FormamailError(message={self.message!r}, code={self.code!r}, status_code={self.status_code})"


class WebhookSignatureError(Exception):
    """Exception raised when webhook signature verification fails."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
