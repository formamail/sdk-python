"""
Emails Resource
"""

from typing import Any, Dict, List, Optional

from ..http import HttpClient, AsyncHttpClient


class EmailsResource:
    """Synchronous emails resource."""

    def __init__(self, http: HttpClient):
        self._http = http

    def send(
        self,
        template_id: str,
        to: str,
        *,
        to_name: Optional[str] = None,
        subject: Optional[str] = None,
        from_name: Optional[str] = None,
        reply_to: Optional[str] = None,
        variables: Optional[Dict[str, Any]] = None,
        track_opens: bool = True,
        track_clicks: bool = True,
        attachments: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Send an email using a template.

        Args:
            template_id: Template ID to use
            to: Recipient email address
            to_name: Recipient name (optional)
            subject: Subject line (overrides template)
            from_name: Sender name (optional)
            reply_to: Reply-to email (optional)
            variables: Template variables
            track_opens: Track email opens
            track_clicks: Track link clicks
            attachments: List of attachments

        Returns:
            Send result with email ID

        Example:
            >>> result = client.emails.send(
            ...     template_id="tmpl_welcome",
            ...     to="customer@example.com",
            ...     variables={"firstName": "John"}
            ... )
        """
        body: Dict[str, Any] = {
            "templateId": template_id,
            "to": to,
            "trackOpens": track_opens,
            "trackClicks": track_clicks,
        }

        if to_name:
            body["toName"] = to_name
        if subject:
            body["subject"] = subject
        if from_name:
            body["fromName"] = from_name
        if reply_to:
            body["replyTo"] = reply_to
        if variables:
            body["variables"] = variables
        if attachments:
            body["attachments"] = attachments

        response = self._http.post("/api/v1/emails/send", body)
        return response.get("data", response)

    def send_with_pdf(
        self,
        template_id: str,
        to: str,
        pdf_template_id: str,
        *,
        pdf_file_name: Optional[str] = None,
        pdf_variables: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Send an email with a generated PDF attachment.

        Args:
            template_id: Email template ID
            to: Recipient email
            pdf_template_id: PDF template ID
            pdf_file_name: Custom PDF file name
            pdf_variables: Variables for PDF template
            **kwargs: Other send options

        Example:
            >>> result = client.emails.send_with_pdf(
            ...     template_id="tmpl_invoice_email",
            ...     to="customer@example.com",
            ...     pdf_template_id="tmpl_invoice_pdf",
            ...     pdf_file_name="Invoice-001",
            ...     variables={"invoiceNumber": "INV-001"}
            ... )
        """
        attachment: Dict[str, Any] = {
            "type": "pdf",
            "templateId": pdf_template_id,
        }
        if pdf_file_name:
            attachment["fileName"] = pdf_file_name
        if pdf_variables:
            attachment["variables"] = pdf_variables

        return self.send(
            template_id=template_id,
            to=to,
            attachments=[attachment],
            **kwargs,
        )

    def send_with_excel(
        self,
        template_id: str,
        to: str,
        excel_template_id: str,
        *,
        excel_file_name: Optional[str] = None,
        excel_variables: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Send an email with a generated Excel attachment.

        Args:
            template_id: Email template ID
            to: Recipient email
            excel_template_id: Excel template ID
            excel_file_name: Custom Excel file name
            excel_variables: Variables for Excel template
            **kwargs: Other send options
        """
        attachment: Dict[str, Any] = {
            "type": "excel",
            "templateId": excel_template_id,
        }
        if excel_file_name:
            attachment["fileName"] = excel_file_name
        if excel_variables:
            attachment["variables"] = excel_variables

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
        subject: Optional[str] = None,
        from_name: Optional[str] = None,
        reply_to: Optional[str] = None,
        common_variables: Optional[Dict[str, Any]] = None,
        track_opens: bool = True,
        track_clicks: bool = True,
    ) -> Dict[str, Any]:
        """
        Send bulk emails to multiple recipients.

        Args:
            template_id: Template ID
            recipients: List of recipients with email, name, variables
            subject: Subject line
            from_name: Sender name
            reply_to: Reply-to email
            common_variables: Variables for all recipients
            track_opens: Track email opens
            track_clicks: Track link clicks

        Example:
            >>> result = client.emails.send_bulk(
            ...     template_id="tmpl_newsletter",
            ...     recipients=[
            ...         {"email": "user1@example.com", "name": "User 1"},
            ...         {"email": "user2@example.com", "name": "User 2"},
            ...     ],
            ...     common_variables={"companyName": "Acme"}
            ... )
        """
        body: Dict[str, Any] = {
            "templateId": template_id,
            "recipients": recipients,
            "trackOpens": track_opens,
            "trackClicks": track_clicks,
        }

        if subject:
            body["subject"] = subject
        if from_name:
            body["fromName"] = from_name
        if reply_to:
            body["replyTo"] = reply_to
        if common_variables:
            body["commonVariables"] = common_variables

        response = self._http.post("/api/v1/emails/send-bulk", body)
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
        to: str,
        *,
        to_name: Optional[str] = None,
        subject: Optional[str] = None,
        from_name: Optional[str] = None,
        reply_to: Optional[str] = None,
        variables: Optional[Dict[str, Any]] = None,
        track_opens: bool = True,
        track_clicks: bool = True,
        attachments: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """Send an email using a template (async)."""
        body: Dict[str, Any] = {
            "templateId": template_id,
            "to": to,
            "trackOpens": track_opens,
            "trackClicks": track_clicks,
        }

        if to_name:
            body["toName"] = to_name
        if subject:
            body["subject"] = subject
        if from_name:
            body["fromName"] = from_name
        if reply_to:
            body["replyTo"] = reply_to
        if variables:
            body["variables"] = variables
        if attachments:
            body["attachments"] = attachments

        response = await self._http.post("/api/v1/emails/send", body)
        return response.get("data", response)

    async def send_with_pdf(
        self,
        template_id: str,
        to: str,
        pdf_template_id: str,
        *,
        pdf_file_name: Optional[str] = None,
        pdf_variables: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Send an email with a generated PDF attachment (async)."""
        attachment: Dict[str, Any] = {
            "type": "pdf",
            "templateId": pdf_template_id,
        }
        if pdf_file_name:
            attachment["fileName"] = pdf_file_name
        if pdf_variables:
            attachment["variables"] = pdf_variables

        return await self.send(
            template_id=template_id,
            to=to,
            attachments=[attachment],
            **kwargs,
        )

    async def send_with_excel(
        self,
        template_id: str,
        to: str,
        excel_template_id: str,
        *,
        excel_file_name: Optional[str] = None,
        excel_variables: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Send an email with a generated Excel attachment (async)."""
        attachment: Dict[str, Any] = {
            "type": "excel",
            "templateId": excel_template_id,
        }
        if excel_file_name:
            attachment["fileName"] = excel_file_name
        if excel_variables:
            attachment["variables"] = excel_variables

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
        subject: Optional[str] = None,
        from_name: Optional[str] = None,
        reply_to: Optional[str] = None,
        common_variables: Optional[Dict[str, Any]] = None,
        track_opens: bool = True,
        track_clicks: bool = True,
    ) -> Dict[str, Any]:
        """Send bulk emails (async)."""
        body: Dict[str, Any] = {
            "templateId": template_id,
            "recipients": recipients,
            "trackOpens": track_opens,
            "trackClicks": track_clicks,
        }

        if subject:
            body["subject"] = subject
        if from_name:
            body["fromName"] = from_name
        if reply_to:
            body["replyTo"] = reply_to
        if common_variables:
            body["commonVariables"] = common_variables

        response = await self._http.post("/api/v1/emails/send-bulk", body)
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
