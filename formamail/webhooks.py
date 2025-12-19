"""
Webhook Signature Verification
"""

import hashlib
import hmac
import json
import time
from typing import Any, Dict

from .exceptions import WebhookSignatureError


def verify_webhook_signature(
    payload: str,
    signature: str,
    secret: str,
    *,
    tolerance: int = 300,
) -> Dict[str, Any]:
    """
    Verify a webhook signature and return the parsed event.

    Args:
        payload: Raw request body as string
        signature: Value of X-FormaMail-Signature header
        secret: Webhook secret from your subscription
        tolerance: Maximum age of webhook in seconds (default: 300)

    Returns:
        Parsed webhook event

    Raises:
        WebhookSignatureError: If signature is invalid

    Example:
        >>> from formamail import verify_webhook_signature
        >>>
        >>> # In your webhook handler (Flask example)
        >>> @app.route('/webhooks/formamail', methods=['POST'])
        >>> def handle_webhook():
        ...     signature = request.headers.get('X-FormaMail-Signature')
        ...     try:
        ...         event = verify_webhook_signature(
        ...             payload=request.data.decode('utf-8'),
        ...             signature=signature,
        ...             secret=os.environ['WEBHOOK_SECRET'],
        ...         )
        ...         print(f"Received event: {event['type']}")
        ...         return 'OK', 200
        ...     except WebhookSignatureError as e:
        ...         return f'Invalid signature: {e}', 400
    """
    # Parse signature header
    parts = dict(p.split("=", 1) for p in signature.split(",") if "=" in p)

    if "t" not in parts or "v1" not in parts:
        raise WebhookSignatureError("Invalid signature header format")

    try:
        timestamp = int(parts["t"])
    except ValueError:
        raise WebhookSignatureError("Invalid timestamp in signature")

    expected_sig = parts["v1"]

    # Check timestamp
    now = int(time.time())
    if abs(now - timestamp) > tolerance:
        raise WebhookSignatureError("Webhook timestamp outside tolerance window")

    # Compute expected signature
    signed_payload = f"{timestamp}.{payload}"
    computed_sig = hmac.new(
        secret.encode("utf-8"),
        signed_payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    # Compare signatures (timing-safe)
    if not hmac.compare_digest(computed_sig, expected_sig):
        raise WebhookSignatureError("Invalid signature")

    # Parse payload
    try:
        return json.loads(payload)
    except json.JSONDecodeError:
        raise WebhookSignatureError("Invalid webhook payload")
