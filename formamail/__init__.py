"""
FormaMail Python SDK

Official SDK for the FormaMail email delivery platform.

Example:
    >>> from formamail import Formamail
    >>>
    >>> client = Formamail(api_key="your_api_key")
    >>>
    >>> # Send an email
    >>> result = client.emails.send(
    ...     template_id="tmpl_welcome",
    ...     to="customer@example.com",
    ...     variables={"firstName": "John"}
    ... )
    >>> print(f"Email sent: {result['id']}")
"""

from .client import Formamail, AsyncFormamail
from .exceptions import FormamailError, WebhookSignatureError
from .webhooks import verify_webhook_signature

__version__ = "1.0.0"
__all__ = [
    "Formamail",
    "AsyncFormamail",
    "FormamailError",
    "WebhookSignatureError",
    "verify_webhook_signature",
]
