"""
FormaMail SDK Resources
"""

from .emails import EmailsResource, AsyncEmailsResource
from .templates import TemplatesResource, AsyncTemplatesResource
from .webhooks import WebhooksResource, AsyncWebhooksResource

__all__ = [
    "EmailsResource",
    "AsyncEmailsResource",
    "TemplatesResource",
    "AsyncTemplatesResource",
    "WebhooksResource",
    "AsyncWebhooksResource",
]
