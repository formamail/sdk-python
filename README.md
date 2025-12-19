# formamail

Official Python SDK for FormaMail - the email delivery platform with unified template design for emails and attachments.

## Installation

```bash
pip install formamail
```

## Quick Start

```python
from formamail import Formamail

client = Formamail(api_key="your_api_key")

# Send an email
result = client.emails.send(
    template_id="tmpl_welcome",
    to="customer@example.com",
    to_name="John Doe",
    variables={
        "firstName": "John",
        "accountId": "12345",
    },
)

print(f"Email sent: {result['id']}")
```

## Features

- **Sync and async clients** - Choose based on your application needs
- **Type hints** - Full type annotation support
- **Email sending** with template variables
- **PDF generation** - Attach auto-generated PDFs from templates
- **Excel generation** - Attach auto-generated Excel files from templates
- **Bulk sending** - Send to multiple recipients with personalization
- **Webhook verification** - Secure signature verification

## Usage Examples

### Send Email with PDF Attachment

```python
result = client.emails.send_with_pdf(
    template_id="tmpl_invoice_email",
    to="customer@example.com",
    pdf_template_id="tmpl_invoice_pdf",
    pdf_file_name="Invoice-001",
    variables={
        "invoiceNumber": "INV-001",
        "customerName": "John Doe",
        "total": 99.99,
    },
)
```

### Send Email with Excel Attachment

```python
result = client.emails.send_with_excel(
    template_id="tmpl_report_email",
    to="manager@example.com",
    excel_template_id="tmpl_monthly_report",
    excel_file_name="Monthly-Report-Jan",
    variables={
        "reportMonth": "January 2025",
    },
)
```

### Send Bulk Emails

```python
result = client.emails.send_bulk(
    template_id="tmpl_newsletter",
    recipients=[
        {"email": "user1@example.com", "name": "User 1", "variables": {"firstName": "User"}},
        {"email": "user2@example.com", "name": "User 2", "variables": {"firstName": "User"}},
    ],
    common_variables={
        "companyName": "Acme Corp",
    },
)

print(f"Batch ID: {result['batchId']}")
```

### List and Search Emails

```python
# List recent emails
emails = client.emails.list(limit=20)

# Search by recipient
emails = client.emails.list(recipient="customer@example.com")

# Filter by status
emails = client.emails.list(status="delivered")

# Get specific email
email = client.emails.get("email_abc123")
```

### Work with Templates

```python
# List all templates
templates = client.templates.list()

# List by type
email_templates = client.templates.list_email()
pdf_templates = client.templates.list_pdf()
excel_templates = client.templates.list_excel()

# Get template details
template = client.templates.get("tmpl_abc123")
```

### Manage Webhooks

```python
# Create a webhook subscription
webhook = client.webhooks.create(
    url="https://your-app.com/webhooks/formamail",
    events=["email.sent", "email.delivered", "email.bounced"],
    name="My Webhook",
)

# Save the secret for verification!
print(f"Webhook secret: {webhook['secret']}")

# List webhooks
webhooks = client.webhooks.list()

# Delete a webhook
client.webhooks.delete("wh_abc123")
```

### Verify Webhook Signatures

```python
from formamail import verify_webhook_signature, WebhookSignatureError

# Flask example
@app.route('/webhooks/formamail', methods=['POST'])
def handle_webhook():
    signature = request.headers.get('X-FormaMail-Signature')

    try:
        event = verify_webhook_signature(
            payload=request.data.decode('utf-8'),
            signature=signature,
            secret=os.environ['WEBHOOK_SECRET'],
        )

        # Process the verified event
        if event['type'] == 'email.sent':
            print(f"Email sent: {event['data']['emailId']}")
        elif event['type'] == 'email.bounced':
            print(f"Email bounced: {event['data']['emailId']}")

        return 'OK', 200
    except WebhookSignatureError as e:
        return f'Invalid signature: {e}', 400
```

## Async Client

For async applications, use `AsyncFormamail`:

```python
from formamail import AsyncFormamail
import asyncio

async def main():
    async with AsyncFormamail(api_key="your_api_key") as client:
        result = await client.emails.send(
            template_id="tmpl_welcome",
            to="customer@example.com",
            variables={"firstName": "John"},
        )
        print(f"Email sent: {result['id']}")

asyncio.run(main())
```

## Configuration

```python
client = Formamail(
    # Required: Your API key
    api_key="your_api_key",

    # Optional: Custom base URL (default: https://api.formamail.com)
    base_url="https://api.formamail.com",

    # Optional: Request timeout in seconds (default: 30)
    timeout=30.0,

    # Optional: Custom headers
    headers={"X-Custom-Header": "value"},
)
```

## Error Handling

```python
from formamail import Formamail, FormamailError

client = Formamail(api_key="your_api_key")

try:
    result = client.emails.send(
        template_id="invalid_template",
        to="customer@example.com",
    )
except FormamailError as e:
    print(f"API Error: {e.message}")
    print(f"Code: {e.code}")
    print(f"Status: {e.status_code}")
```

## Context Manager

Use the client as a context manager to ensure proper cleanup:

```python
with Formamail(api_key="your_api_key") as client:
    result = client.emails.send(
        template_id="tmpl_welcome",
        to="customer@example.com",
    )
```

## API Reference

### Client Methods

- `client.me()` - Get current authenticated user
- `client.verify_api_key()` - Verify API key is valid

### Emails Resource

- `client.emails.send(...)` - Send an email
- `client.emails.send_with_pdf(...)` - Send with PDF attachment
- `client.emails.send_with_excel(...)` - Send with Excel attachment
- `client.emails.send_bulk(...)` - Send bulk emails
- `client.emails.get(email_id)` - Get email by ID
- `client.emails.list(...)` - List/search emails

### Templates Resource

- `client.templates.get(template_id)` - Get template by ID
- `client.templates.list(...)` - List templates
- `client.templates.list_email()` - List email templates
- `client.templates.list_pdf()` - List PDF templates
- `client.templates.list_excel()` - List Excel templates

### Webhooks Resource

- `client.webhooks.create(...)` - Create webhook subscription
- `client.webhooks.get(webhook_id)` - Get webhook by ID
- `client.webhooks.list()` - List webhooks
- `client.webhooks.update(...)` - Update webhook
- `client.webhooks.delete(webhook_id)` - Delete webhook

### Utilities

- `verify_webhook_signature(...)` - Verify webhook signature

## Requirements

- Python 3.8+
- httpx 0.24+

## License

MIT

## Support

- Documentation: https://docs.formamail.com/sdk/python
- API Reference: https://docs.formamail.com/api
- Support: support@formamail.com
