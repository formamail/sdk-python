"""
Webhooks Resource
"""

from typing import Any, Dict, List, Optional

from ..http import HttpClient, AsyncHttpClient


class WebhooksResource:
    """Synchronous webhooks resource."""

    def __init__(self, http: HttpClient):
        self._http = http

    def create(
        self,
        url: str,
        events: List[str],
        *,
        name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a webhook subscription.

        Args:
            url: Webhook endpoint URL
            events: List of event types to subscribe to
            name: Webhook name (optional)

        Returns:
            Webhook subscription with secret

        Example:
            >>> webhook = client.webhooks.create(
            ...     url="https://your-app.com/webhooks",
            ...     events=["email.sent", "email.delivered"],
            ...     name="My Webhook"
            ... )
            >>> print(f"Secret: {webhook['secret']}")
        """
        body: Dict[str, Any] = {
            "url": url,
            "events": events,
        }
        if name:
            body["name"] = name

        response = self._http.post("/api/v1/webhook-subscriptions", body)
        return response.get("data", response)

    def get(self, webhook_id: str) -> Dict[str, Any]:
        """Get a webhook subscription by ID."""
        response = self._http.get(f"/api/v1/webhook-subscriptions/{webhook_id}")
        return response.get("data", response)

    def list(self) -> Dict[str, Any]:
        """List all webhook subscriptions."""
        return self._http.get("/api/v1/webhook-subscriptions")

    def update(
        self,
        webhook_id: str,
        *,
        url: Optional[str] = None,
        events: Optional[List[str]] = None,
        name: Optional[str] = None,
        active: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Update a webhook subscription."""
        body: Dict[str, Any] = {}
        if url is not None:
            body["url"] = url
        if events is not None:
            body["events"] = events
        if name is not None:
            body["name"] = name
        if active is not None:
            body["active"] = active

        response = self._http.put(f"/api/v1/webhook-subscriptions/{webhook_id}", body)
        return response.get("data", response)

    def delete(self, webhook_id: str) -> None:
        """Delete a webhook subscription."""
        self._http.delete(f"/api/v1/webhook-subscriptions/{webhook_id}")


class AsyncWebhooksResource:
    """Asynchronous webhooks resource."""

    def __init__(self, http: AsyncHttpClient):
        self._http = http

    async def create(
        self,
        url: str,
        events: List[str],
        *,
        name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a webhook subscription (async)."""
        body: Dict[str, Any] = {
            "url": url,
            "events": events,
        }
        if name:
            body["name"] = name

        response = await self._http.post("/api/v1/webhook-subscriptions", body)
        return response.get("data", response)

    async def get(self, webhook_id: str) -> Dict[str, Any]:
        """Get a webhook subscription by ID (async)."""
        response = await self._http.get(f"/api/v1/webhook-subscriptions/{webhook_id}")
        return response.get("data", response)

    async def list(self) -> Dict[str, Any]:
        """List all webhook subscriptions (async)."""
        return await self._http.get("/api/v1/webhook-subscriptions")

    async def update(
        self,
        webhook_id: str,
        *,
        url: Optional[str] = None,
        events: Optional[List[str]] = None,
        name: Optional[str] = None,
        active: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Update a webhook subscription (async)."""
        body: Dict[str, Any] = {}
        if url is not None:
            body["url"] = url
        if events is not None:
            body["events"] = events
        if name is not None:
            body["name"] = name
        if active is not None:
            body["active"] = active

        response = await self._http.put(
            f"/api/v1/webhook-subscriptions/{webhook_id}", body
        )
        return response.get("data", response)

    async def delete(self, webhook_id: str) -> None:
        """Delete a webhook subscription (async)."""
        await self._http.delete(f"/api/v1/webhook-subscriptions/{webhook_id}")
