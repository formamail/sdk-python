"""
FormaMail SDK Type Definitions
"""

from typing import Any, Dict, List, Literal, Optional, TypedDict, Union


# Email Types
class EmailRecipient(TypedDict, total=False):
    """Email recipient with optional name."""

    email: str
    name: Optional[str]


# Flexible recipient input: string, dict, or list of either
RecipientInput = Union[str, EmailRecipient, List[Union[str, EmailRecipient]]]


class Attachment(TypedDict, total=False):
    """Email attachment configuration."""

    type: Literal["pdf", "excel"]
    template_id: str
    file_name: Optional[str]
    variables: Optional[Dict[str, Any]]


class BulkAttachment(TypedDict, total=False):
    """Attachment configuration for bulk emails."""

    filename: str
    content_type: Optional[str]
    content: Optional[str]  # Base64 encoded
    url: Optional[str]
    attachment_template_id: Optional[str]
    base_variables: Optional[Dict[str, Any]]
    recipient_variable_fields: Optional[List[str]]
    output_formats: Optional[List[str]]
    required: Optional[bool]


class BulkRecipient(TypedDict, total=False):
    """Bulk email recipient with per-recipient variables."""

    email: str
    name: Optional[str]
    variables: Dict[str, Any]  # Required - variables for this recipient
    attachment_overrides: Optional[List[BulkAttachment]]


class SendEmailOptions(TypedDict, total=False):
    """Options for sending an email."""

    template_id: str
    to: RecipientInput
    cc: Optional[RecipientInput]
    bcc: Optional[RecipientInput]
    version: Optional[Literal["published", "draft"]]
    sender_email: Optional[str]
    sender_id: Optional[str]
    from_name: Optional[str]
    reply_to: Optional[str]
    variables: Optional[Dict[str, Any]]
    priority: Optional[Literal["low", "normal", "high"]]
    scheduled_at: Optional[str]
    headers: Optional[Dict[str, str]]
    tags: Optional[List[str]]
    metadata: Optional[Dict[str, Any]]
    attachments: Optional[List[Attachment]]


class SendBulkEmailOptions(TypedDict, total=False):
    """Options for sending bulk emails with personalization."""

    template_id: str
    version: Optional[Literal["published", "draft"]]
    recipients: List[BulkRecipient]
    base_variables: Optional[Dict[str, Any]]
    attachments: Optional[List[BulkAttachment]]
    sender_email: Optional[str]
    sender_id: Optional[str]
    from_name: Optional[str]
    reply_to: Optional[str]
    priority: Optional[Literal["low", "normal", "high"]]
    headers: Optional[Dict[str, str]]
    tags: Optional[List[str]]
    metadata: Optional[Dict[str, Any]]
    batch_name: Optional[str]
    dry_run: Optional[bool]
    scheduled_at: Optional[str]


class SendBulkEmailResponse(TypedDict, total=False):
    """Response from sending bulk emails."""

    batch_id: str
    status: str
    total_emails: int
    message: str
    created_at: str
    estimated_completion_at: Optional[str]
    scheduled_at: Optional[str]


EmailStatus = Literal[
    "pending",
    "queued",
    "processing",
    "sent",
    "delivered",
    "failed",
    "bounced",
    "complained",
    "rejected",
    "scheduled",
]


class BlockedRecipient(TypedDict, total=False):
    """Details about a blocked recipient."""

    email: str
    reason: str
    source: Optional[str]


class SendEmailResponse(TypedDict, total=False):
    """Response from sending an email."""

    id: str
    status: EmailStatus
    message: str
    provider_message_id: Optional[str]
    scheduled_at: Optional[str]
    created_at: str
    warning: Optional[str]
    blocked_recipients: Optional[List[BlockedRecipient]]


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
