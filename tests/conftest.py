"""
Test configuration and fixtures.
"""

import pytest
import requests_mock
from hostex import HostexClient


@pytest.fixture
def mock_client():
    """Create a mock Hostex client for testing."""
    return HostexClient(access_token="test_token_12345")


@pytest.fixture  
def oauth_client():
    """Create an OAuth Hostex client for testing."""
    return HostexClient(
        client_id="test_client_id",
        client_secret="test_client_secret",
        redirect_uri="https://example.com/callback"
    )


@pytest.fixture
def requests_mocker():
    """Provide requests mock."""
    with requests_mock.Mocker() as m:
        yield m


@pytest.fixture
def sample_property():
    """Sample property data for testing."""
    return {
        "id": 12345,
        "title": "Beautiful Test Apartment",
        "channels": [
            {
                "channel_type": "airbnb",
                "listing_id": "airbnb_123456"
            },
            {
                "channel_type": "booking.com", 
                "listing_id": "booking_654321"
            }
        ],
        "address": "123 Test Street, Test City",
        "longitude": "-122.4194",
        "latitude": "37.7749"
    }


@pytest.fixture
def sample_reservation():
    """Sample reservation data for testing."""
    return {
        "reservation_code": "0-1234567-abcdef",
        "stay_code": "0-1234567-abcdef",
        "channel_id": "test_channel_id",
        "property_id": 12345,
        "channel_type": "hostex_direct",
        "listing_id": "direct_listing_123",
        "check_in_date": "2024-07-01",
        "check_out_date": "2024-07-07",
        "number_of_guests": 2,
        "number_of_adults": 2,
        "number_of_children": 0,
        "number_of_infants": 0,
        "number_of_pets": 0,
        "status": "accepted",
        "guest_name": "John Test",
        "guest_phone": "+1234567890",
        "guest_email": "john@test.com",
        "cancelled_at": None,
        "booked_at": "2024-06-01T10:00:00+00:00",
        "created_at": "2024-06-01T10:00:00+00:00",
        "creator": "API Test",
        "rates": {},
        "check_in_details": {},
        "remarks": "Test reservation",
        "channel_remarks": "",
        "conversation_id": "conv_123456",
        "tags": ["test"],
        "custom_channel": None,
        "guests": [
            {
                "id": 1,
                "name": "John Test",
                "phone": "+1234567890",
                "email": "john@test.com",
                "id_type": "passport",
                "id_number": "TEST123456",
                "gender": "male",
                "country": "US",
                "is_booker": True,
                "custom_fields": None
            }
        ],
        "in_reservation_box": True
    }


@pytest.fixture
def sample_api_response():
    """Sample successful API response structure."""
    return {
        "request_id": "req_12345",
        "error_code": 200,
        "error_msg": "Success"
    }