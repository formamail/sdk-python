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
    template_id="welcome-email",  # Can be UUID, shortId (etpl_xxx), or slug
    to="customer@example.com",
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

### Multiple Recipients with CC/BCC

The `to`, `cc`, and `bcc` parameters accept flexible input formats:

```python
# Simple string (single recipient)
client.emails.send(
    template_id="welcome-email",
    to="john@example.com",
    variables={"name": "John"},
)

# Dict with name
client.emails.send(
    template_id="welcome-email",
    to={"email": "john@example.com", "name": "John Doe"},
    variables={"name": "John"},
)

# List of recipients (mixed formats)
client.emails.send(
    template_id="team-update",
    to=[
        {"email": "john@example.com", "name": "John Doe"},
        "jane@example.com",  # Name is optional
        {"email": "bob@example.com", "name": "Bob Smith"},
    ],
    variables={"teamName": "Engineering"},
)

# With CC and BCC
client.emails.send(
    template_id="invoice-email",
    to={"email": "customer@example.com", "name": "Customer"},
    cc="accounts@customer.com",  # CC the customer's accounts team
    bcc=[
        "audit@yourcompany.com",  # Internal audit copy
        {"email": "manager@yourcompany.com", "name": "Sales Manager"},
    ],
    variables={"invoiceNumber": "INV-001"},
)
```

### Send Email with Attachment (PDF or Excel)

```python
# Send with PDF attachment
result = client.emails.send_with_attachment(
    template_id="invoice-email",
    to="customer@example.com",
    attachment_template_id="invoice-pdf",
    attachment_type="pdf",
    file_name="Invoice-001",
    variables={
        "invoiceNumber": "INV-001",
        "customerName": "John Doe",
    },
)

# Send with Excel attachment
result = client.emails.send_with_attachment(
    template_id="report-email",
    to="manager@example.com",
    attachment_template_id="monthly-report-excel",
    attachment_type="excel",
    file_name="Monthly-Report-Jan",
    variables={
        "reportMonth": "January 2025",
    },
)
```

### Send Bulk Emails

```python
# Simple bulk send
result = client.emails.send_bulk(
    template_id="newsletter",
    recipients=[
        {"email": "user1@example.com", "name": "User 1", "variables": {"firstName": "Alice"}},
        {"email": "user2@example.com", "name": "User 2", "variables": {"firstName": "Bob"}},
    ],
    base_variables={"companyName": "Acme Corp"},  # Shared across all
    tags=["newsletter", "monthly"],
)

print(f"Batch ID: {result['batchId']}")
```

### Bulk Send with Personalized Attachments

There are two ways to personalize attachments in bulk sends:

**Option 1: Using `recipientVariableFields`** - Specify which recipient variable fields to use for attachments

```python
invoice_result = client.emails.send_bulk(
    template_id="invoice-email",
    recipients=[
        {"email": "c1@example.com", "variables": {"name": "Alice", "invoiceNumber": "INV-001", "amount": 100}},
        {"email": "c2@example.com", "variables": {"name": "Bob", "invoiceNumber": "INV-002", "amount": 200}},
    ],
    base_variables={"companyName": "Acme Corp"},
    attachments=[{
        "filename": "invoice-{{invoiceNumber}}.pdf",
        "attachmentTemplateId": "invoice-pdf",
        "baseVariables": {"currency": "USD"},
        # These fields are pulled from each recipient's variables
        "recipientVariableFields": ["name", "invoiceNumber", "amount"],
        "outputFormats": ["pdf"],
    }],
    batch_name="January Invoices",
)
```

**Option 2: Using `attachmentOverrides`** - Override attachments per recipient for complete control

```python
custom_result = client.emails.send_bulk(
    template_id="report-email",
    recipients=[
        {
            "email": "c1@example.com",
            "variables": {"name": "Alice"},
            # Completely override attachments for this recipient
            "attachmentOverrides": [{
                "filename": "custom-report-alice.pdf",
                "attachmentTemplateId": "vip-report-pdf",
                "baseVariables": {"reportType": "VIP", "discount": 20},
                "outputFormats": ["pdf"],
            }],
        },
        {
            "email": "c2@example.com",
            "variables": {"name": "Bob"},
            # This recipient uses the default attachments (no override)
        },
    ],
    base_variables={"companyName": "Acme Corp"},
    attachments=[{
        "filename": "standard-report.pdf",
        "attachmentTemplateId": "standard-report-pdf",
        "outputFormats": ["pdf"],
    }],
)
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
- `client.emails.send_with_attachment(...)` - Send with PDF or Excel attachment
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
