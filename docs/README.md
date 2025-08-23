# hostex-python

A Python client library for the Hostex API v3.0.0 (Beta).

## Overview

Hostex is a property management platform that provides APIs for managing reservations, properties, availabilities, messaging, reviews, and more. This Python library provides a convenient interface to interact with the Hostex API.

## Features

- **Authentication**: Support for both API token and OAuth authentication
- **Properties**: Query properties and room types
- **Reservations**: Create, query, update, and cancel reservations
- **Availabilities**: Query and update property availabilities
- **Listing Management**: Update calendars, prices, inventories, and restrictions
- **Messaging**: Query conversations and send messages to guests
- **Reviews**: Query and create reviews and replies
- **Webhooks**: Manage webhook subscriptions
- **Custom Fields**: Manage custom fields for reservations
- **Rate Limiting**: Automatic handling of API rate limits
- **Error Handling**: Comprehensive error handling with custom exceptions

## Installation

```bash
pip install hostex-python
```

## Quick Start

### API Token Authentication

```python
from hostex import HostexClient

# Initialize client with API token
client = HostexClient(access_token="your_access_token_here")

# Query properties
properties = client.properties.list(limit=10)
print(f"Found {properties['total']} properties")

# Query reservations
reservations = client.reservations.list(
    start_check_in_date="2024-01-01",
    end_check_in_date="2024-01-31"
)
```

### OAuth Authentication

```python
from hostex import HostexClient

# Initialize client for OAuth
client = HostexClient(
    client_id="your_client_id",
    client_secret="your_client_secret"
)

# Exchange authorization code for tokens
tokens = client.oauth.get_access_token(
    authorization_code="auth_code_from_redirect"
)

# Use the access token
client.set_access_token(tokens['access_token'])
```

## Library Structure

The library is organized into the following modules:

- `hostex.client` - Main client class
- `hostex.auth` - Authentication handlers
- `hostex.endpoints` - API endpoint implementations
- `hostex.models` - Data models and response objects
- `hostex.exceptions` - Custom exception classes
- `hostex.utils` - Utility functions

### Endpoint Modules

- `properties` - Properties and room types
- `reservations` - Reservation management
- `availabilities` - Property availability
- `listings` - Listing calendar management
- `conversations` - Messaging
- `reviews` - Reviews and replies
- `webhooks` - Webhook management
- `oauth` - OAuth authentication

## Usage Examples

### Working with Properties

```python
# List all properties
properties = client.properties.list()

# Get specific property
property_detail = client.properties.list(id=12345)

# Query room types
room_types = client.room_types.list()
```

### Managing Reservations

```python
# Create a new reservation
reservation = client.reservations.create(
    property_id="12345",
    custom_channel_id=1,
    check_in_date="2024-06-01",
    check_out_date="2024-06-07",
    guest_name="John Doe",
    currency="USD",
    rate_amount=50000,  # $500.00 in cents
    commission_amount=5000,
    received_amount=45000,
    income_method_id=1
)

# Query reservations
reservations = client.reservations.list(
    status="accepted",
    start_check_in_date="2024-01-01"
)

# Cancel a reservation
client.reservations.cancel("reservation_code_here")

# Update lock code
client.reservations.update_lock_code(
    stay_code="stay_code_here",
    lock_code="1234"
)
```

### Managing Availabilities

```python
# Query property availabilities
availabilities = client.availabilities.list(
    property_ids="12345,67890",
    start_date="2024-06-01",
    end_date="2024-06-30"
)

# Update property availability
client.availabilities.update(
    property_ids=[12345, 67890],
    start_date="2024-06-01",
    end_date="2024-06-07",
    available=False
)
```

### Working with Conversations

```python
# List conversations
conversations = client.conversations.list()

# Get conversation details
conversation = client.conversations.get("conversation_id")

# Send a message
client.conversations.send_message(
    conversation_id="conversation_id",
    message="Thank you for your booking!"
)
```

### Managing Reviews

```python
# Query reviews
reviews = client.reviews.list(
    property_id=12345,
    start_check_out_date="2024-01-01"
)

# Create a review
client.reviews.create(
    reservation_code="reservation_code",
    host_review_score=5.0,
    host_review_content="Great guest!"
)
```

### Webhook Management

```python
# List webhooks
webhooks = client.webhooks.list()

# Create a webhook
webhook = client.webhooks.create(
    url="https://your-server.com/webhook"
)

# Delete a webhook
client.webhooks.delete(webhook_id=123)
```

## Error Handling

The library provides custom exceptions for different error conditions:

```python
from hostex.exceptions import (
    HostexAPIError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    NotFoundError
)

try:
    reservations = client.reservations.list()
except AuthenticationError:
    print("Invalid API token or expired session")
except RateLimitError as e:
    print(f"Rate limit exceeded. Retry after {e.retry_after} seconds")
except ValidationError as e:
    print(f"Validation error: {e.message}")
except HostexAPIError as e:
    print(f"API error {e.error_code}: {e.message}")
```

## Rate Limiting

The library automatically handles rate limiting by:
- Adding delays between requests when approaching limits
- Implementing exponential backoff for 429 responses
- Providing rate limit information in error messages

## Configuration

You can configure the client behavior:

```python
client = HostexClient(
    access_token="your_token",
    base_url="https://api.hostex.io/v3",  # Custom base URL
    timeout=30,  # Request timeout in seconds
    max_retries=3,  # Maximum retry attempts
    user_agent="MyApp/1.0"  # Custom User-Agent
)
```

## Development

### Setup Development Environment

```bash
git clone https://github.com/example/hostex-python.git
cd hostex-python
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/
pytest tests/ --cov=hostex --cov-report=html
```

### Code Formatting

```bash
black hostex/
flake8 hostex/
mypy hostex/
```

## API Reference

For detailed API documentation, see [docs/API.md](docs/API.md).

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- GitHub Issues: https://github.com/example/hostex-python/issues
- Hostex API Documentation: https://docs.hostex.io/
- Hostex Support: contact@hostex.io