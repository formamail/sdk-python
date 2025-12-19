"""
FormaMail SDK Client
"""

from typing import Any, Dict, Optional

from .http import HttpClient, AsyncHttpClient
from .resources.emails import EmailsResource, AsyncEmailsResource
from .resources.templates import TemplatesResource, AsyncTemplatesResource
from .resources.webhooks import WebhooksResource, AsyncWebhooksResource


DEFAULT_BASE_URL = "https://api.formamail.com"
DEFAULT_TIMEOUT = 30.0


class Formamail:
    """
    Synchronous FormaMail client.

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

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        headers: Optional[Dict[str, str]] = None,
    ):
        """
        Create a new FormaMail client.

        Args:
            api_key: Your FormaMail API key
            base_url: API base URL (default: https://api.formamail.com)
            timeout: Request timeout in seconds (default: 30)
            headers: Additional headers to include in requests
        """
        if not api_key:
            raise ValueError("api_key is required")

        self._http = HttpClient(
            base_url=base_url,
            api_key=api_key,
            timeout=timeout,
            headers=headers,
        )

        self.emails = EmailsResource(self._http)
        self.templates = TemplatesResource(self._http)
        self.webhooks = WebhooksResource(self._http)

    def me(self) -> Dict[str, Any]:
        """Get the current authenticated user."""
        response = self._http.get("/api/v1/me")
        return response.get("data", response)

    def verify_api_key(self) -> bool:
        """Verify the API key is valid."""
        try:
            self.me()
            return True
        except Exception:
            return False

    def close(self) -> None:
        """Close the HTTP client."""
        self._http.close()

    def __enter__(self) -> "Formamail":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


class AsyncFormamail:
    """
    Asynchronous FormaMail client.

    Example:
        >>> from formamail import AsyncFormamail
        >>> import asyncio
        >>>
        >>> async def main():
        ...     async with AsyncFormamail(api_key="your_api_key") as client:
        ...         result = await client.emails.send(
        ...             template_id="tmpl_welcome",
        ...             to="customer@example.com",
        ...             variables={"firstName": "John"}
        ...         )
        ...         print(f"Email sent: {result['id']}")
        >>>
        >>> asyncio.run(main())
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        headers: Optional[Dict[str, str]] = None,
    ):
        """
        Create a new async FormaMail client.

        Args:
            api_key: Your FormaMail API key
            base_url: API base URL (default: https://api.formamail.com)
            timeout: Request timeout in seconds (default: 30)
            headers: Additional headers to include in requests
        """
        if not api_key:
            raise ValueError("api_key is required")

        self._http = AsyncHttpClient(
            base_url=base_url,
            api_key=api_key,
            timeout=timeout,
            headers=headers,
        )

        self.emails = AsyncEmailsResource(self._http)
        self.templates = AsyncTemplatesResource(self._http)
        self.webhooks = AsyncWebhooksResource(self._http)

    async def me(self) -> Dict[str, Any]:
        """Get the current authenticated user (async)."""
        response = await self._http.get("/api/v1/me")
        return response.get("data", response)

    async def verify_api_key(self) -> bool:
        """Verify the API key is valid (async)."""
        try:
            await self.me()
            return True
        except Exception:
            return False

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._http.close()

    async def __aenter__(self) -> "AsyncFormamail":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()
