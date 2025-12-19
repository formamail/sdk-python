"""Tests for FormaMail client."""

import pytest
from formamail import Formamail, AsyncFormamail


class TestFormamail:
    """Tests for synchronous Formamail client."""

    def test_requires_api_key(self) -> None:
        """Should raise ValueError if api_key is not provided."""
        with pytest.raises(ValueError, match="api_key is required"):
            Formamail(api_key="")

    def test_creates_client_with_api_key(self) -> None:
        """Should create client with valid api_key."""
        client = Formamail(api_key="test_api_key")
        assert client is not None
        assert client.emails is not None
        assert client.templates is not None
        assert client.webhooks is not None

    def test_accepts_custom_base_url(self) -> None:
        """Should accept custom base_url."""
        client = Formamail(
            api_key="test_api_key",
            base_url="https://custom.api.com",
        )
        assert client is not None

    def test_accepts_custom_timeout(self) -> None:
        """Should accept custom timeout."""
        client = Formamail(
            api_key="test_api_key",
            timeout=60.0,
        )
        assert client is not None

    def test_accepts_custom_headers(self) -> None:
        """Should accept custom headers."""
        client = Formamail(
            api_key="test_api_key",
            headers={"X-Custom-Header": "value"},
        )
        assert client is not None

    def test_context_manager(self) -> None:
        """Should work as context manager."""
        with Formamail(api_key="test_api_key") as client:
            assert client is not None


class TestAsyncFormamail:
    """Tests for asynchronous Formamail client."""

    def test_requires_api_key(self) -> None:
        """Should raise ValueError if api_key is not provided."""
        with pytest.raises(ValueError, match="api_key is required"):
            AsyncFormamail(api_key="")

    def test_creates_client_with_api_key(self) -> None:
        """Should create async client with valid api_key."""
        client = AsyncFormamail(api_key="test_api_key")
        assert client is not None
        assert client.emails is not None
        assert client.templates is not None
        assert client.webhooks is not None

    def test_accepts_custom_base_url(self) -> None:
        """Should accept custom base_url."""
        client = AsyncFormamail(
            api_key="test_api_key",
            base_url="https://custom.api.com",
        )
        assert client is not None
