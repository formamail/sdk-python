"""
Templates Resource
"""

from typing import Any, Dict, Optional

from ..http import HttpClient, AsyncHttpClient


class TemplatesResource:
    """Synchronous templates resource."""

    def __init__(self, http: HttpClient):
        self._http = http

    def get(self, template_id: str) -> Dict[str, Any]:
        """Get a template by ID."""
        response = self._http.get(f"/api/v1/templates/{template_id}")
        return response.get("data", response)

    def list(
        self,
        *,
        type: Optional[str] = None,
        limit: int = 20,
        page: int = 1,
    ) -> Dict[str, Any]:
        """
        List templates with optional filters.

        Args:
            type: Filter by type (email, pdf, excel)
            limit: Results per page
            page: Page number

        Returns:
            Dict with 'data' and 'meta'
        """
        params = {
            "type": type,
            "limit": limit,
            "page": page,
        }
        return self._http.get("/api/v1/templates", params)

    def list_email(self, *, limit: int = 20, page: int = 1) -> Dict[str, Any]:
        """List email templates."""
        return self.list(type="email", limit=limit, page=page)

    def list_pdf(self, *, limit: int = 20, page: int = 1) -> Dict[str, Any]:
        """List PDF templates."""
        return self.list(type="pdf", limit=limit, page=page)

    def list_excel(self, *, limit: int = 20, page: int = 1) -> Dict[str, Any]:
        """List Excel templates."""
        return self.list(type="excel", limit=limit, page=page)


class AsyncTemplatesResource:
    """Asynchronous templates resource."""

    def __init__(self, http: AsyncHttpClient):
        self._http = http

    async def get(self, template_id: str) -> Dict[str, Any]:
        """Get a template by ID (async)."""
        response = await self._http.get(f"/api/v1/templates/{template_id}")
        return response.get("data", response)

    async def list(
        self,
        *,
        type: Optional[str] = None,
        limit: int = 20,
        page: int = 1,
    ) -> Dict[str, Any]:
        """List templates (async)."""
        params = {
            "type": type,
            "limit": limit,
            "page": page,
        }
        return await self._http.get("/api/v1/templates", params)

    async def list_email(self, *, limit: int = 20, page: int = 1) -> Dict[str, Any]:
        """List email templates (async)."""
        return await self.list(type="email", limit=limit, page=page)

    async def list_pdf(self, *, limit: int = 20, page: int = 1) -> Dict[str, Any]:
        """List PDF templates (async)."""
        return await self.list(type="pdf", limit=limit, page=page)

    async def list_excel(self, *, limit: int = 20, page: int = 1) -> Dict[str, Any]:
        """List Excel templates (async)."""
        return await self.list(type="excel", limit=limit, page=page)
