"""
Emails Resource
"""

from typing import Any, Dict, List, Optional, Union

from ..http import HttpClient, AsyncHttpClient


# Type alias for flexible recipient input
RecipientInput = Union[str, Dict[str, Any], List[Union[str, Dict[str, Any]]]]


def _normalize_recipients(
    recipients: RecipientInput,
) -> List[Dict[str, Any]]:
    """
    Normalize recipient input to list of {email, name} dicts.

    Accepts:
        - str: "john@example.com"
        - dict: {"email": "john@example.com", "name": "John"}
        - list: ["john@example.com", {"email": "jane@example.com", "name": "Jane"}]
    """
    if isinstance(recipients, str):
        return [{"email": recipients}]
    elif isinstance(recipients, dict):
        return [recipients]
    elif isinstance(recipients, list):
        result = []
        for r in recipients:
            if isinstance(r, str):
                result.append({"email": r})
            else:
                result.append(r)
        return result
    else:
        raise ValueError(f"Invalid recipient type: {type(recipients)}")


class EmailsResource:
    """Synchronous emails resource."""

    def __init__(self, http: HttpClient):
        self._http = http

    def send(
        self,
        template_id: str,
        to: RecipientInput,
        *,
        cc: Optional[RecipientInput] = None,
        bcc: Optional[RecipientInput] = None,
        version: Optional[str] = None,
        sender_email: Optional[str] = None,
        sender_id: Optional[str] = None,
        from_name: Optional[str] = None,
        reply_to: Optional[str] = None,
        variables: Optional[Dict[str, Any]] = None,
        priority: Optional[str] = None,
        scheduled_at: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        attachments: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Send an email using a template.

        Args:
            template_id: Template ID (UUID, shortId like etpl_xxx, or slug)
            to: Recipient(s) - string, dict with email/name, or list
            cc: CC recipient(s) - same format as 'to'
            bcc: BCC recipient(s) - same format as 'to'
            version: Template version ('published' or 'draft')
            sender_email: Verified sender email address
            sender_id: Sender ID (legacy - prefer sender_email)
            from_name: Custom sender name
            reply_to: Reply-to email override
            variables: Template variables
            priority: Email priority ('low', 'normal', 'high')
            scheduled_at: Schedule send time (ISO 8601)
            headers: Custom headers
            tags: Tags for tracking
            metadata: Metadata for tracking
            attachments: List of attachments

        Returns:
            Send result with email ID

        Example:
            >>> # Single recipient
            >>> result = client.emails.send(
            ...     template_id="welcome-email",
            ...     to="customer@example.com",
            ...     variables={"firstName": "John"}
            ... )

            >>> # Multiple recipients with cc/bcc
            >>> result = client.emails.send(
            ...     template_id="invoice-email",
            ...     to=[
            ...         {"email": "john@example.com", "name": "John Doe"},
            ...         "jane@example.com",
            ...     ],
            ...     cc="manager@example.com",
            ...     bcc=["audit@example.com"],
            ...     variables={"invoiceNumber": "INV-001"}
            ... )
        """
        body: Dict[str, Any] = {
            "templateId": template_id,
            "to": _normalize_recipients(to),
        }

        if cc is not None:
            body["cc"] = _normalize_recipients(cc)
        if bcc is not None:
            body["bcc"] = _normalize_recipients(bcc)
        if version:
            body["version"] = version
        if sender_email:
            body["senderEmail"] = sender_email
        if sender_id:
            body["senderId"] = sender_id
        if from_name:
            body["fromName"] = from_name
        if reply_to:
            body["replyTo"] = reply_to
        if variables:
            body["variables"] = variables
        if priority:
            body["priority"] = priority
        if scheduled_at:
            body["scheduledAt"] = scheduled_at
        if headers:
            body["headers"] = headers
        if tags:
            body["tags"] = tags
        if metadata:
            body["metadata"] = metadata
        if attachments:
            body["attachments"] = attachments

        response = self._http.post("/api/v1/emails/send", body)
        return response.get("data", response)

    def send_with_attachment(
        self,
        template_id: str,
        to: RecipientInput,
        attachment_template_id: str,
        attachment_type: str = "pdf",
        *,
        file_name: Optional[str] = None,
        attachment_variables: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Send an email with a generated attachment (PDF or Excel).

        Args:
            template_id: Email template ID
            to: Recipient(s) - string, dict, or list
            attachment_template_id: Template ID for generating the attachment
            attachment_type: Attachment type ('pdf' or 'excel')
            file_name: Custom file name (without extension)
            attachment_variables: Variables for the attachment template
            **kwargs: Other send options (cc, bcc, variables, etc.)

        Example:
            >>> # Send with PDF attachment
            >>> result = client.emails.send_with_attachment(
            ...     template_id="invoice-email",
            ...     to="customer@example.com",
            ...     attachment_template_id="invoice-pdf",
            ...     attachment_type="pdf",
            ...     file_name="Invoice-001",
            ...     variables={"invoiceNumber": "INV-001"}
            ... )

            >>> # Send with Excel attachment
            >>> result = client.emails.send_with_attachment(
            ...     template_id="report-email",
            ...     to="manager@example.com",
            ...     attachment_template_id="monthly-report-excel",
            ...     attachment_type="excel",
            ...     file_name="Report-Jan",
            ...     variables={"reportMonth": "January 2025"}
            ... )
        """
        attachment: Dict[str, Any] = {
            "type": attachment_type,
            "templateId": attachment_template_id,
        }
        if file_name:
            attachment["fileName"] = file_name
        if attachment_variables:
            attachment["variables"] = attachment_variables

        return self.send(
            template_id=template_id,
            to=to,
            attachments=[attachment],
            **kwargs,
        )

    def send_bulk(
        self,
        template_id: str,
        recipients: List[Dict[str, Any]],
        *,
        version: Optional[str] = None,
        base_variables: Optional[Dict[str, Any]] = None,
        attachments: Optional[List[Dict[str, Any]]] = None,
        sender_email: Optional[str] = None,
        sender_id: Optional[str] = None,
        from_name: Optional[str] = None,
        reply_to: Optional[str] = None,
        priority: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        batch_name: Optional[str] = None,
        dry_run: Optional[bool] = None,
        scheduled_at: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Send bulk emails to multiple recipients with personalization.

        Supports variable overrides at multiple levels:
        - base_variables: Shared across all recipients
        - recipients[].variables: Per-recipient overrides (merged with base_variables)
        - attachments[].base_variables: Shared for attachment generation
        - recipients[].attachment_overrides: Per-recipient attachment overrides

        Args:
            template_id: Template ID (UUID, shortId like etpl_xxx, or slug)
            recipients: List of recipients (max 1000) with:
                - email: Recipient email address
                - name: Recipient name (optional)
                - variables: Variables for this recipient (merged with base_variables)
                - attachment_overrides: Per-recipient attachment overrides (optional)
            version: Template version ('published' or 'draft')
            base_variables: Variables shared across all recipients
            attachments: Attachments for all recipients with:
                - filename: Can use variables like {{invoiceNumber}}.pdf
                - attachment_template_id: Template for generating attachment
                - base_variables: Shared variables for attachment
                - recipient_variable_fields: Which recipient fields to use
                - output_formats: ['pdf', 'excel']
            sender_email: Verified sender email address
            sender_id: Sender ID (legacy - prefer sender_email)
            from_name: Custom sender name
            reply_to: Reply-to email address
            priority: Email priority ('low', 'normal', 'high')
            headers: Custom headers
            tags: Tags for tracking
            metadata: Metadata for tracking
            batch_name: Batch name for tracking
            dry_run: Validate without sending (returns validation result)
            scheduled_at: Schedule send time (ISO 8601 format)

        Example:
            >>> # Simple bulk send
            >>> result = client.emails.send_bulk(
            ...     template_id="newsletter",
            ...     recipients=[
            ...         {"email": "user1@example.com", "variables": {"firstName": "Alice"}},
            ...         {"email": "user2@example.com", "variables": {"firstName": "Bob"}},
            ...     ],
            ...     base_variables={"companyName": "Acme", "year": "2025"},
            ...     tags=["newsletter", "monthly"],
            ... )

            >>> # Option 1: Personalized attachments using recipientVariableFields
            >>> result = client.emails.send_bulk(
            ...     template_id="invoice-email",
            ...     recipients=[
            ...         {"email": "c1@example.com", "variables": {"name": "Alice", "invoiceNumber": "INV-001"}},
            ...         {"email": "c2@example.com", "variables": {"name": "Bob", "invoiceNumber": "INV-002"}},
            ...     ],
            ...     attachments=[{
            ...         "filename": "invoice-{{invoiceNumber}}.pdf",
            ...         "attachmentTemplateId": "invoice-pdf",
            ...         "recipientVariableFields": ["name", "invoiceNumber"],  # Pull these from recipient
            ...         "outputFormats": ["pdf"],
            ...     }],
            ... )

            >>> # Option 2: Per-recipient attachment override using attachmentOverrides
            >>> result = client.emails.send_bulk(
            ...     template_id="report-email",
            ...     recipients=[
            ...         {
            ...             "email": "vip@example.com",
            ...             "variables": {"name": "VIP Customer"},
            ...             "attachmentOverrides": [{  # Override for this recipient
            ...                 "filename": "vip-report.pdf",
            ...                 "attachmentTemplateId": "vip-report-pdf",
            ...                 "outputFormats": ["pdf"],
            ...             }],
            ...         },
            ...         {"email": "regular@example.com", "variables": {"name": "Regular"}},  # Uses default
            ...     ],
            ...     attachments=[{"filename": "standard.pdf", "attachmentTemplateId": "standard-pdf"}],
            ... )
        """
        body: Dict[str, Any] = {
            "templateId": template_id,
            "recipients": recipients,
        }

        if version:
            body["version"] = version
        if base_variables:
            body["baseVariables"] = base_variables
        if attachments:
            body["attachments"] = attachments
        if sender_email:
            body["senderEmail"] = sender_email
        if sender_id:
            body["senderId"] = sender_id
        if from_name:
            body["fromName"] = from_name
        if reply_to:
            body["replyTo"] = reply_to
        if priority:
            body["priority"] = priority
        if headers:
            body["headers"] = headers
        if tags:
            body["tags"] = tags
        if metadata:
            body["metadata"] = metadata
        if batch_name:
            body["batchName"] = batch_name
        if dry_run is not None:
            body["dryRun"] = dry_run
        if scheduled_at:
            body["scheduledAt"] = scheduled_at

        response = self._http.post("/api/v1/emails/send/bulk", body)
        return response.get("data", response)

    def get(self, email_id: str) -> Dict[str, Any]:
        """Get an email by ID."""
        response = self._http.get(f"/api/v1/emails/{email_id}")
        return response.get("data", response)

    def list(
        self,
        *,
        recipient: Optional[str] = None,
        status: Optional[str] = None,
        template_id: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        limit: int = 20,
        page: int = 1,
    ) -> Dict[str, Any]:
        """
        List emails with optional filters.

        Returns dict with 'data' (list) and 'meta' (pagination).
        """
        params = {
            "recipient": recipient,
            "status": status,
            "templateId": template_id,
            "dateFrom": date_from,
            "dateTo": date_to,
            "limit": limit,
            "page": page,
        }
        return self._http.get("/api/v1/emails", params)


class AsyncEmailsResource:
    """Asynchronous emails resource."""

    def __init__(self, http: AsyncHttpClient):
        self._http = http

    async def send(
        self,
        template_id: str,
        to: RecipientInput,
        *,
        cc: Optional[RecipientInput] = None,
        bcc: Optional[RecipientInput] = None,
        version: Optional[str] = None,
        sender_email: Optional[str] = None,
        sender_id: Optional[str] = None,
        from_name: Optional[str] = None,
        reply_to: Optional[str] = None,
        variables: Optional[Dict[str, Any]] = None,
        priority: Optional[str] = None,
        scheduled_at: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        attachments: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Send an email using a template (async).

        See EmailsResource.send() for full documentation.
        """
        body: Dict[str, Any] = {
            "templateId": template_id,
            "to": _normalize_recipients(to),
        }

        if cc is not None:
            body["cc"] = _normalize_recipients(cc)
        if bcc is not None:
            body["bcc"] = _normalize_recipients(bcc)
        if version:
            body["version"] = version
        if sender_email:
            body["senderEmail"] = sender_email
        if sender_id:
            body["senderId"] = sender_id
        if from_name:
            body["fromName"] = from_name
        if reply_to:
            body["replyTo"] = reply_to
        if variables:
            body["variables"] = variables
        if priority:
            body["priority"] = priority
        if scheduled_at:
            body["scheduledAt"] = scheduled_at
        if headers:
            body["headers"] = headers
        if tags:
            body["tags"] = tags
        if metadata:
            body["metadata"] = metadata
        if attachments:
            body["attachments"] = attachments

        response = await self._http.post("/api/v1/emails/send", body)
        return response.get("data", response)

    async def send_with_attachment(
        self,
        template_id: str,
        to: RecipientInput,
        attachment_template_id: str,
        attachment_type: str = "pdf",
        *,
        file_name: Optional[str] = None,
        attachment_variables: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Send an email with a generated attachment (async).

        See EmailsResource.send_with_attachment() for full documentation.
        """
        attachment: Dict[str, Any] = {
            "type": attachment_type,
            "templateId": attachment_template_id,
        }
        if file_name:
            attachment["fileName"] = file_name
        if attachment_variables:
            attachment["variables"] = attachment_variables

        return await self.send(
            template_id=template_id,
            to=to,
            attachments=[attachment],
            **kwargs,
        )

    async def send_bulk(
        self,
        template_id: str,
        recipients: List[Dict[str, Any]],
        *,
        version: Optional[str] = None,
        base_variables: Optional[Dict[str, Any]] = None,
        attachments: Optional[List[Dict[str, Any]]] = None,
        sender_email: Optional[str] = None,
        sender_id: Optional[str] = None,
        from_name: Optional[str] = None,
        reply_to: Optional[str] = None,
        priority: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        batch_name: Optional[str] = None,
        dry_run: Optional[bool] = None,
        scheduled_at: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Send bulk emails (async).

        See EmailsResource.send_bulk() for full documentation.
        """
        body: Dict[str, Any] = {
            "templateId": template_id,
            "recipients": recipients,
        }

        if version:
            body["version"] = version
        if base_variables:
            body["baseVariables"] = base_variables
        if attachments:
            body["attachments"] = attachments
        if sender_email:
            body["senderEmail"] = sender_email
        if sender_id:
            body["senderId"] = sender_id
        if from_name:
            body["fromName"] = from_name
        if reply_to:
            body["replyTo"] = reply_to
        if priority:
            body["priority"] = priority
        if headers:
            body["headers"] = headers
        if tags:
            body["tags"] = tags
        if metadata:
            body["metadata"] = metadata
        if batch_name:
            body["batchName"] = batch_name
        if dry_run is not None:
            body["dryRun"] = dry_run
        if scheduled_at:
            body["scheduledAt"] = scheduled_at

        response = await self._http.post("/api/v1/emails/send/bulk", body)
        return response.get("data", response)

    async def get(self, email_id: str) -> Dict[str, Any]:
        """Get an email by ID (async)."""
        response = await self._http.get(f"/api/v1/emails/{email_id}")
        return response.get("data", response)

    async def list(
        self,
        *,
        recipient: Optional[str] = None,
        status: Optional[str] = None,
        template_id: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        limit: int = 20,
        page: int = 1,
    ) -> Dict[str, Any]:
        """List emails with optional filters (async)."""
        params = {
            "recipient": recipient,
            "status": status,
            "templateId": template_id,
            "dateFrom": date_from,
            "dateTo": date_to,
            "limit": limit,
            "page": page,
        }
        return await self._http.get("/api/v1/emails", params)
