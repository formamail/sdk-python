"""
HTTP Client for FormaMail SDK
"""

from typing import Any, Dict, Optional
import httpx

from .exceptions import FormamailError


class HttpClient:
    """Synchronous HTTP client."""

    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: float = 30.0,
        headers: Optional[Dict[str, str]] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self._headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "formamail-python/1.0.0",
            **(headers or {}),
        }
        self._client = httpx.Client(timeout=timeout)

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Handle API response and errors."""
        try:
            data = response.json()
        except Exception:
            data = {}

        if response.status_code >= 400:
            message = data.get("message", f"HTTP {response.status_code}")
            code = data.get("error", "ApiError")
            raise FormamailError(message, code, response.status_code)

        return data

    def get(
        self, path: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make GET request."""
        # Filter out None values from params
        if params:
            params = {k: v for k, v in params.items() if v is not None}

        response = self._client.get(
            f"{self.base_url}{path}",
            headers=self._headers,
            params=params,
        )
        return self._handle_response(response)

    def post(
        self, path: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make POST request."""
        response = self._client.post(
            f"{self.base_url}{path}",
            headers=self._headers,
            json=data,
        )
        return self._handle_response(response)

    def put(
        self, path: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make PUT request."""
        response = self._client.put(
            f"{self.base_url}{path}",
            headers=self._headers,
            json=data,
        )
        return self._handle_response(response)

    def delete(self, path: str) -> Dict[str, Any]:
        """Make DELETE request."""
        response = self._client.delete(
            f"{self.base_url}{path}",
            headers=self._headers,
        )
        return self._handle_response(response)

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()


class AsyncHttpClient:
    """Asynchronous HTTP client."""

    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: float = 30.0,
        headers: Optional[Dict[str, str]] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self._headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "formamail-python/1.0.0",
            **(headers or {}),
        }
        self._client = httpx.AsyncClient(timeout=timeout)

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Handle API response and errors."""
        try:
            data = response.json()
        except Exception:
            data = {}

        if response.status_code >= 400:
            message = data.get("message", f"HTTP {response.status_code}")
            code = data.get("error", "ApiError")
            raise FormamailError(message, code, response.status_code)

        return data

    async def get(
        self, path: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make GET request."""
        if params:
            params = {k: v for k, v in params.items() if v is not None}

        response = await self._client.get(
            f"{self.base_url}{path}",
            headers=self._headers,
            params=params,
        )
        return self._handle_response(response)

    async def post(
        self, path: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make POST request."""
        response = await self._client.post(
            f"{self.base_url}{path}",
            headers=self._headers,
            json=data,
        )
        return self._handle_response(response)

    async def put(
        self, path: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make PUT request."""
        response = await self._client.put(
            f"{self.base_url}{path}",
            headers=self._headers,
            json=data,
        )
        return self._handle_response(response)

    async def delete(self, path: str) -> Dict[str, Any]:
        """Make DELETE request."""
        response = await self._client.delete(
            f"{self.base_url}{path}",
            headers=self._headers,
        )
        return self._handle_response(response)

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()
