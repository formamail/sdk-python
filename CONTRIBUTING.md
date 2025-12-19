# Contributing to formamail (Python)

This guide covers how to develop, test, and publish the FormaMail Python SDK.

## Prerequisites

- Python 3.8 or later
- pip or poetry
- A FormaMail account with API key (for integration tests)

## Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/formamail/sdk-python.git
cd sdk-python
```

### 2. Create Virtual Environment

```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using conda
conda create -n formamail python=3.11
conda activate formamail
```

### 3. Install Dependencies

```bash
# Install package in editable mode with dev dependencies
pip install -e ".[dev]"
```

### 4. Set Up Environment Variables

Create a `.env` file for testing (never commit this):

```bash
# .env
FORMAMAIL_API_KEY=your_test_api_key
FORMAMAIL_BASE_URL=https://api.formamail.com  # or staging URL
FORMAMAIL_WEBHOOK_SECRET=your_webhook_secret
```

## Development Workflow

### Code Formatting

We use `ruff` for linting and formatting:

```bash
# Check for lint errors
ruff check .

# Auto-fix lint errors
ruff check --fix .

# Format code
ruff format .
```

### Type Checking

```bash
# Run mypy type checker
mypy formamail
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run a specific test file
pytest tests/test_emails.py

# Run a specific test
pytest tests/test_emails.py::test_send_email

# Run tests matching a pattern
pytest -k "webhook"
```

### Test Coverage

```bash
# Run tests with coverage
pytest --cov=formamail --cov-report=html

# View coverage report
open htmlcov/index.html
```

We aim for >80% test coverage.

### Writing Unit Tests

Tests are located in `tests/`. Example:

```python
# tests/test_emails.py
import pytest
from unittest.mock import Mock, patch
from formamail import Formamail

class TestEmailsResource:
    @pytest.fixture
    def client(self):
        return Formamail(api_key="test_key")

    @patch('formamail.http.HttpClient.request')
    def test_send_email(self, mock_request, client):
        mock_request.return_value = {"id": "email_123", "status": "queued"}

        result = client.emails.send(
            template_id="tmpl_123",
            to="test@example.com",
        )

        assert result["id"] == "email_123"
        mock_request.assert_called_once()
```

### Integration Tests

Integration tests make real API calls. Only run these against a test/staging environment.

```bash
# Run integration tests (requires FORMAMAIL_API_KEY)
pytest tests/integration/ -v
```

### Async Tests

For testing async functionality:

```python
# tests/test_async.py
import pytest
from formamail import AsyncFormamail

@pytest.mark.asyncio
async def test_async_send():
    async with AsyncFormamail(api_key="test_key") as client:
        # Test async operations
        pass
```

## Versioning

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (1.0.0 → 2.0.0): Breaking changes
- **MINOR** (1.0.0 → 1.1.0): New features, backward compatible
- **PATCH** (1.0.0 → 1.0.1): Bug fixes, backward compatible

### Version Location

Version is defined in `pyproject.toml`:

```toml
[project]
version = "1.0.0"
```

And in `formamail/__init__.py`:

```python
__version__ = "1.0.0"
```

**Always update both files!**

## Publishing to PyPI

### Prerequisites

1. You must have PyPI account with access to `formamail` package
2. You must have API token configured
3. Install build tools: `pip install build twine`

### Pre-publish Checklist

- [ ] All tests pass: `pytest`
- [ ] Lint passes: `ruff check .`
- [ ] Type check passes: `mypy formamail`
- [ ] Version is updated in `pyproject.toml` AND `formamail/__init__.py`
- [ ] CHANGELOG.md is updated
- [ ] Changes are committed and pushed

### Manual Publishing

```bash
# 1. Ensure you're on main branch with latest changes
git checkout main
git pull origin main

# 2. Run tests
pytest

# 3. Run lint and type check
ruff check .
mypy formamail

# 4. Update version in pyproject.toml and formamail/__init__.py
# Edit files manually

# 5. Clean previous builds
rm -rf dist/ build/ *.egg-info/

# 6. Build the package
python -m build

# 7. Check the build
twine check dist/*

# 8. Upload to Test PyPI first (optional but recommended)
twine upload --repository testpypi dist/*

# 9. Test installation from Test PyPI
pip install --index-url https://test.pypi.org/simple/ formamail

# 10. Upload to PyPI
twine upload dist/*

# 11. Create git tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin main --tags

# 12. Verify on PyPI
open https://pypi.org/project/formamail/
```

### Automated Publishing (CI/CD)

We use GitHub Actions for automated publishing. When you push a version tag:

```yaml
# .github/workflows/publish.yml
name: Publish to PyPI

on:
  push:
    tags:
      - 'v*'

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install build twine
          pip install -e ".[dev]"

      - name: Run tests
        run: pytest

      - name: Build package
        run: python -m build

      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
        run: twine upload dist/*
```

### Setting Up PyPI Token for CI

1. Generate a PyPI API token:
   - Go to pypi.org → Account Settings → API tokens
   - Create token scoped to `formamail` package

2. Add to GitHub secrets:
   - Go to repo Settings → Secrets → Actions
   - Add `PYPI_TOKEN` with the token value

## Release Process

### 1. Create a Release Branch (for major/minor)

```bash
git checkout -b release/v1.2.0
```

### 2. Update Version

Edit `pyproject.toml`:
```toml
version = "1.2.0"
```

Edit `formamail/__init__.py`:
```python
__version__ = "1.2.0"
```

### 3. Update CHANGELOG.md

```markdown
## [1.2.0] - 2025-12-18

### Added
- New `send_with_excel()` method for Excel attachments
- Support for custom headers in client config
- Async client support with `AsyncFormamail`

### Fixed
- Webhook signature verification timing attack vulnerability

### Changed
- Improved error messages for validation errors
```

### 4. Commit and Tag

```bash
git add .
git commit -m "Release v1.2.0"
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin release/v1.2.0 --tags
```

### 5. Create Pull Request

Create a PR from `release/v1.2.0` to `main`.

### 6. Merge and Publish

After PR approval:
1. Merge to main
2. CI automatically publishes to PyPI

### 7. Create GitHub Release

1. Go to Releases → Draft a new release
2. Select the version tag
3. Copy CHANGELOG entry as release notes
4. Publish release

## Troubleshooting

### twine upload fails with 403

- Ensure your PyPI token is valid
- Ensure the token has scope for the `formamail` package
- Check if the version already exists on PyPI (versions cannot be overwritten)

### Build fails

- Clear build artifacts: `rm -rf dist/ build/ *.egg-info/`
- Reinstall dependencies: `pip install -e ".[dev]"`
- Check Python version: `python --version` (should be 3.8+)

### Tests fail in CI but pass locally

- Check for environment-dependent code
- Ensure all mocks are properly set up
- Check for timing-sensitive tests
- Verify Python version matches

### Import errors after install

- Ensure `__init__.py` exports are correct
- Check `pyproject.toml` package configuration
- Try reinstalling: `pip uninstall formamail && pip install -e .`

## Code Style

- Follow PEP 8 (enforced by ruff)
- Use type hints for all public APIs
- Document all public APIs with docstrings (Google style)
- Keep functions small and focused
- Write tests for all new features

### Docstring Example

```python
def send(
    self,
    template_id: str,
    to: str,
    *,
    to_name: str | None = None,
    variables: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Send an email using a template.

    Args:
        template_id: The ID of the template to use.
        to: The recipient's email address.
        to_name: The recipient's display name.
        variables: Template variables for personalization.

    Returns:
        A dictionary containing the email ID and status.

    Raises:
        FormamailError: If the API request fails.

    Example:
        >>> client.emails.send(
        ...     template_id="tmpl_welcome",
        ...     to="user@example.com",
        ...     variables={"firstName": "John"},
        ... )
        {'id': 'email_123', 'status': 'queued'}
    """
```

## Questions?

- Open an issue on GitHub
- Email: sdk-support@formamail.com
