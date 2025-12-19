"""
FormaMail SDK Type Definitions
"""

from typing import Any, Dict, List, Literal, Optional, TypedDict


# Email Types
class Attachment(TypedDict, total=False):
    type: Literal["pdf", "excel"]
    template_id: str
    file_name: Optional[str]
    variables: Optional[Dict[str, Any]]


class BulkRecipient(TypedDict, total=False):
    email: str
    name: Optional[str]
    variables: Optional[Dict[str, Any]]


class SendEmailOptions(TypedDict, total=False):
    template_id: str
    to: str
    to_name: Optional[str]
    subject: Optional[str]
    from_name: Optional[str]
    reply_to: Optional[str]
    variables: Optional[Dict[str, Any]]
    track_opens: Optional[bool]
    track_clicks: Optional[bool]
    attachments: Optional[List[Attachment]]


class SendBulkEmailOptions(TypedDict, total=False):
    template_id: str
    recipients: List[BulkRecipient]
    subject: Optional[str]
    from_name: Optional[str]
    reply_to: Optional[str]
    common_variables: Optional[Dict[str, Any]]
    track_opens: Optional[bool]
    track_clicks: Optional[bool]


EmailStatus = Literal["queued", "sent", "delivered", "opened", "clicked", "bounced", "failed"]

WebhookEventType = Literal[
    "email.sent",
    "email.delivered",
    "email.opened",
    "email.clicked",
    "email.bounced",
    "unsubscribe.created",
]


class CreateWebhookOptions(TypedDict, total=False):
    url: str
    events: List[WebhookEventType]
    name: Optional[str]


class ListEmailsOptions(TypedDict, total=False):
    recipient: Optional[str]
    status: Optional[EmailStatus]
    template_id: Optional[str]
    date_from: Optional[str]
    date_to: Optional[str]
    limit: Optional[int]
    page: Optional[int]


class ListTemplatesOptions(TypedDict, total=False):
    type: Optional[Literal["email", "pdf", "excel"]]
    limit: Optional[int]
    page: Optional[int]
