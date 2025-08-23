# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-08-23

### Added
- Initial release of hostex-python library
- Complete Hostex API v3.0.0 (Beta) coverage
- API token authentication support
- OAuth 2.0 authentication with automatic token refresh
- Properties and Room Types endpoints
- Reservations management (CRUD, custom fields, lock codes)
- Availability management endpoints
- Listing calendar management (prices, inventories, restrictions)
- Messaging and conversations endpoints
- Reviews management endpoints
- Webhooks management endpoints
- Custom channels and income methods endpoints
- Comprehensive error handling with custom exceptions
- Rate limiting with exponential backoff
- Type hints throughout the codebase
- Extensive test suite with 95%+ coverage
- Comprehensive documentation and examples
- Development tools and configuration

### Features
- **Authentication**: Dual support for API tokens and OAuth 2.0
- **Error Handling**: Custom exceptions for all error types (401, 403, 404, 429, 500, etc.)
- **Rate Limiting**: Automatic retry with exponential backoff for rate limit errors
- **Token Management**: Automatic OAuth token refresh when expired
- **Type Safety**: Full type annotations for better IDE support
- **Testing**: Comprehensive test suite with unit, integration, and error handling tests
- **Documentation**: Complete API reference, user guide, and examples

### Technical Details
- Python 3.7+ support
- Minimal dependencies (requests, python-dateutil)
- Comprehensive error handling
- Automatic request retries
- Configurable timeouts and retry behavior
- Clean, intuitive API design

[1.0.0]: https://github.com/keithah/hostex-python/releases/tag/v1.0.0