# Contributing to hostex-python

First off, thank you for considering contributing to hostex-python! It's people like you that make this library better for everyone.

## Code of Conduct

This project and everyone participating in it is governed by our commitment to creating a welcoming and inclusive environment. Please be respectful and constructive in all interactions.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list to see if the problem has already been reported. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed and what behavior you expected**
- **Include details about your configuration and environment**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the enhancement**
- **Explain why this enhancement would be useful**

### Pull Requests

1. Fork the repository
2. Create a new branch from `main` for your feature or bug fix
3. Make your changes
4. Add tests for your changes
5. Run the test suite and ensure all tests pass
6. Update documentation as needed
7. Submit a pull request

## Development Setup

### Prerequisites

- Python 3.7 or higher
- Git

### Setting Up Your Development Environment

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/hostex-python.git
   cd hostex-python
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Set up pre-commit hooks** (recommended)
   ```bash
   pre-commit install
   ```

### Running Tests

Run the full test suite:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=hostex --cov-report=html
```

Run specific test files:
```bash
pytest tests/test_client.py
pytest tests/test_endpoints.py
```

Run tests with different verbosity:
```bash
pytest -v  # Verbose
pytest -s  # Don't capture output
```

### Code Quality

We use several tools to maintain code quality:

**Format code with Black:**
```bash
black hostex tests
# or
make format
```

**Lint code with flake8:**
```bash
flake8 hostex tests
# or
make lint
```

**Type check with mypy:**
```bash
mypy hostex
# or
make type-check
```

**Run all quality checks:**
```bash
make check
```

### Documentation

Documentation is located in the `docs/` directory. When making changes:

1. Update relevant documentation files
2. Ensure examples are working and up-to-date
3. Update the API reference if adding new features
4. Update the changelog for notable changes

## Coding Standards

### Python Style

- Follow PEP 8 style guide
- Use Black for code formatting
- Maximum line length is 88 characters (Black default)
- Use type hints for all public functions and methods
- Write docstrings for all public classes and methods

### Code Organization

- Keep functions and methods focused and small
- Use descriptive variable and function names
- Add type hints to improve code clarity
- Write comprehensive tests for new functionality
- Follow existing patterns in the codebase

### Testing

- Write tests for all new functionality
- Maintain or improve test coverage
- Use descriptive test names that explain what is being tested
- Test both success and error cases
- Use mocks for external API calls

### Example Test Structure

```python
class TestNewFeature:
    """Test the new feature functionality."""
    
    def test_feature_success_case(self, mock_client, requests_mocker):
        """Test that feature works correctly with valid input."""
        # Setup
        # Execute
        # Assert
    
    def test_feature_error_case(self, mock_client):
        """Test that feature handles errors correctly."""
        # Test error conditions
```

### Commit Messages

- Use clear and meaningful commit messages
- Start with a capital letter
- Use the imperative mood ("Add feature" not "Added feature")
- Keep the first line under 50 characters
- Reference issues and pull requests when applicable

Examples:
```
Add support for custom field updates
Fix rate limiting retry logic
Update documentation for OAuth flow
```

## API Guidelines

When adding new API endpoints or functionality:

1. **Follow existing patterns** - Look at similar endpoints for consistency
2. **Add comprehensive error handling** - Handle all expected error cases
3. **Include input validation** - Validate parameters before making API calls
4. **Add rate limiting support** - Ensure new endpoints respect rate limits
5. **Write thorough tests** - Test success cases, error cases, and edge cases
6. **Update documentation** - Add examples and update API reference

### New Endpoint Checklist

- [ ] Endpoint implementation in appropriate module
- [ ] Input validation and type hints
- [ ] Error handling for all expected error codes
- [ ] Comprehensive tests (success, errors, edge cases)
- [ ] Documentation updates
- [ ] Example usage in docs/examples.md

## Release Process

Releases are handled by maintainers. The process includes:

1. Update version in `setup.py` and `hostex/__init__.py`
2. Update `CHANGELOG.md` with new version details
3. Create release tag
4. Build and publish to PyPI
5. Create GitHub release with release notes

## Questions?

If you have questions about contributing, please:

1. Check the existing documentation
2. Search existing issues
3. Create a new issue with the "question" label
4. Reach out to maintainers

Thank you for contributing to hostex-python! 🚀