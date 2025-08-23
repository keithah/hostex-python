# hostex-python

[![PyPI version](https://img.shields.io/pypi/v/hostex-python.svg)](https://pypi.org/project/hostex-python/)
[![Python versions](https://img.shields.io/pypi/pyversions/hostex-python.svg)](https://pypi.org/project/hostex-python/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python client library for the Hostex API v3.0.0 (Beta). Hostex is a property management platform that provides APIs for managing reservations, properties, availabilities, messaging, reviews, and more.

## 🚀 Features

- **Complete API Coverage**: All Hostex API v3.0.0 endpoints
- **Dual Authentication**: API token and OAuth 2.0 support
- **Automatic Token Refresh**: OAuth tokens refreshed automatically
- **Rate Limiting**: Built-in rate limit handling with exponential backoff
- **Comprehensive Error Handling**: Custom exceptions for all error types
- **Type Hints**: Full type annotation support
- **Async-Ready**: Designed for easy async/await integration
- **Extensive Testing**: 95%+ test coverage
- **Rich Documentation**: Comprehensive docs and examples

### Supported APIs

| Feature | Endpoints | Description |
|---------|-----------|-------------|
| 🏠 **Properties** | `/properties`, `/room_types` | Property and room type management |
| 📅 **Reservations** | `/reservations/*` | CRUD operations, custom fields, lock codes |
| 📊 **Availability** | `/availabilities` | Property availability management |
| 📋 **Listings** | `/listings/*` | Calendar, pricing, inventory, restrictions |
| 💬 **Messaging** | `/conversations/*` | Guest communication and messaging |
| ⭐ **Reviews** | `/reviews/*` | Review management and responses |
| 🔗 **Webhooks** | `/webhooks/*` | Real-time event notifications |
| ⚙️ **Utilities** | `/custom_channels`, `/income_methods` | Configuration endpoints |

## 📦 Installation

```bash
pip install hostex-python
```

### Development Installation

```bash
git clone https://github.com/keithah/hostex-python.git
cd hostex-python
pip install -e ".[dev]"
```

## 🔐 Authentication

### API Token (Recommended for server-side apps)

```python
from hostex import HostexClient

client = HostexClient(access_token="your_hostex_api_token")
```

### OAuth 2.0 (Required for third-party integrations)

```python
from hostex import HostexClient

# Initialize OAuth client
client = HostexClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    redirect_uri="https://your-app.com/callback"
)

# Generate authorization URL
auth_url = client.oauth.get_authorization_url(state="random_state")
print(f"Visit: {auth_url}")

# Exchange authorization code for tokens
tokens = client.oauth.get_access_token("authorization_code_from_callback")

# Client is now authenticated and ready to use
properties = client.properties.list()
```

### Environment Variables

```bash
export HOSTEX_ACCESS_TOKEN="your_token_here"
# or for OAuth
export HOSTEX_CLIENT_ID="your_client_id"
export HOSTEX_CLIENT_SECRET="your_client_secret"
```

```python
import os
from hostex import HostexClient

# Auto-detects credentials from environment
client = HostexClient(
    access_token=os.getenv("HOSTEX_ACCESS_TOKEN"),
    # or
    client_id=os.getenv("HOSTEX_CLIENT_ID"),
    client_secret=os.getenv("HOSTEX_CLIENT_SECRET")
)
```

## 🚀 Quick Start

### List Properties

```python
# Get all properties
properties = client.properties.list()

for property in properties['data']['properties']:
    print(f"{property['title']} (ID: {property['id']})")
    print(f"  Address: {property.get('address', 'Not specified')}")
    print(f"  Channels: {[ch['channel_type'] for ch in property['channels']]}")
```

### Manage Reservations

```python
# List recent reservations
reservations = client.reservations.list(
    status="accepted",
    start_check_in_date="2024-01-01",
    limit=50
)

# Create a direct booking
reservation = client.reservations.create(
    property_id="12345",
    custom_channel_id=1,
    check_in_date="2024-07-01",
    check_out_date="2024-07-07",
    guest_name="Jane Smith",
    currency="USD",
    rate_amount=84000,  # $840.00 (in cents)
    commission_amount=8400,
    received_amount=75600,
    income_method_id=1
)

# Update custom fields (e.g., lock code)
client.reservations.update_custom_fields(
    stay_code="0-1234567-abcdef",
    custom_fields={
        "lock_code": "1234",
        "wifi_password": "GuestWiFi2024"
    }
)
```

### Manage Availability

```python
# Check availability
availabilities = client.availabilities.list(
    property_ids="12345,67890",
    start_date="2024-07-01",
    end_date="2024-07-31"
)

# Block dates for maintenance
client.availabilities.update(
    property_ids=[12345],
    dates=["2024-07-15", "2024-07-16"],
    available=False
)
```

### Guest Communication

```python
# List conversations
conversations = client.conversations.list()

# Get conversation details
conversation = client.conversations.get("conversation_id")

# Send a message
client.conversations.send_message(
    conversation_id="conversation_id",
    message="Thank you for choosing our property! Check-in is at 3 PM."
)
```

### Webhook Integration

```python
# List webhooks
webhooks = client.webhooks.list()

# Create webhook
webhook = client.webhooks.create("https://your-app.com/hostex-webhook")

# Example webhook handler (Flask)
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/hostex-webhook', methods=['POST'])
def handle_webhook():
    payload = request.get_json()
    event_type = payload.get('event')
    
    if event_type == 'reservation_created':
        # Handle new reservation
        reservation_code = payload.get('reservation_code')
        print(f"New reservation: {reservation_code}")
    
    return jsonify({"status": "received"}), 200
```

## 🛡️ Error Handling

The library provides comprehensive error handling with custom exceptions:

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
except NotFoundError:
    print("Resource not found")
except HostexAPIError as e:
    print(f"API error {e.error_code}: {e.message}")
```

## 📚 Documentation

- **[API Reference](docs/API.md)** - Complete API documentation
- **[User Guide](docs/README.md)** - Detailed usage guide  
- **[Examples](docs/examples.md)** - Comprehensive examples and workflows
- **[Hostex API Docs](https://docs.hostex.io/)** - Official API documentation

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=hostex --cov-report=html

# Run specific test file
pytest tests/test_client.py
```

## 🛠️ Development

### Setup Development Environment

```bash
git clone https://github.com/keithah/hostex-python.git
cd hostex-python
pip install -e ".[dev]"
```

### Code Quality

```bash
# Format code
make format

# Lint code
make lint

# Type checking
make type-check

# Run all checks
make check
```

## 📋 Requirements

- Python 3.7+
- requests >= 2.25.0
- python-dateutil >= 2.8.0

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and add tests
4. Run the test suite (`make test`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/keithah/hostex-python/issues)
- **Documentation**: [docs/](docs/)
- **Hostex API Support**: contact@hostex.io

---

**Note**: This library is not officially supported by Hostex. It's a community-driven project to provide Python developers with easy access to the Hostex API.