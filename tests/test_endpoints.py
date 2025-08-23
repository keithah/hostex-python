"""
Tests for API endpoint classes.
"""

import pytest
import requests_mock
from hostex.endpoints import (
    PropertiesEndpoint,
    RoomTypesEndpoint,
    ReservationsEndpoint,
    AvailabilitiesEndpoint,
    ListingsEndpoint,
    ConversationsEndpoint,
    ReviewsEndpoint,
    WebhooksEndpoint,
)


class TestPropertiesEndpoint:
    """Test PropertiesEndpoint class."""
    
    def test_list_properties_default(self, mock_client, requests_mocker, sample_property, sample_api_response):
        """Test listing properties with default parameters."""
        response_data = sample_api_response.copy()
        response_data["data"] = {
            "properties": [sample_property],
            "total": 1
        }
        
        requests_mocker.get(
            "https://api.hostex.io/v3/properties",
            json=response_data
        )
        
        result = mock_client.properties.list()
        
        assert result["error_code"] == 200
        assert len(result["data"]["properties"]) == 1
        assert result["data"]["properties"][0]["id"] == 12345
        
        # Check default parameters
        request = requests_mocker.last_request
        assert request.qs == {"offset": ["0"], "limit": ["20"]}
    
    def test_list_properties_with_params(self, mock_client, requests_mocker, sample_api_response):
        """Test listing properties with custom parameters."""
        requests_mocker.get(
            "https://api.hostex.io/v3/properties",
            json=sample_api_response
        )
        
        mock_client.properties.list(offset=10, limit=50, id=12345)
        
        request = requests_mocker.last_request
        assert request.qs == {"offset": ["10"], "limit": ["50"], "id": ["12345"]}
    
    def test_list_properties_limit_validation(self, mock_client):
        """Test properties list limit validation."""
        with pytest.raises(ValueError, match="Limit cannot exceed 100"):
            mock_client.properties.list(limit=101)


class TestRoomTypesEndpoint:
    """Test RoomTypesEndpoint class."""
    
    def test_list_room_types(self, mock_client, requests_mocker, sample_api_response):
        """Test listing room types."""
        response_data = sample_api_response.copy()
        response_data["data"] = {
            "room_types": [
                {
                    "id": 1,
                    "title": "Standard Room",
                    "properties": [{"id": 12345, "title": "Test Property"}],
                    "channels": [{"channel_type": "airbnb", "listing_id": "abc123"}]
                }
            ],
            "total": 1
        }
        
        requests_mocker.get(
            "https://api.hostex.io/v3/room_types",
            json=response_data
        )
        
        result = mock_client.room_types.list()
        
        assert result["error_code"] == 200
        assert len(result["data"]["room_types"]) == 1
        assert result["data"]["room_types"][0]["title"] == "Standard Room"


class TestReservationsEndpoint:
    """Test ReservationsEndpoint class."""
    
    def test_list_reservations_default(self, mock_client, requests_mocker, sample_reservation, sample_api_response):
        """Test listing reservations with default parameters."""
        response_data = sample_api_response.copy()
        response_data["data"] = {
            "reservations": [sample_reservation]
        }
        
        requests_mocker.get(
            "https://api.hostex.io/v3/reservations",
            json=response_data
        )
        
        result = mock_client.reservations.list()
        
        assert result["error_code"] == 200
        assert len(result["data"]["reservations"]) == 1
        
        # Check default parameters
        request = requests_mocker.last_request
        expected_params = {"order_by": ["booked_at"], "offset": ["0"], "limit": ["20"]}
        assert request.qs == expected_params
    
    def test_list_reservations_with_filters(self, mock_client, requests_mocker, sample_api_response):
        """Test listing reservations with filters."""
        requests_mocker.get(
            "https://api.hostex.io/v3/reservations",
            json=sample_api_response
        )
        
        mock_client.reservations.list(
            reservation_code="0-1234567-abcdef",
            property_id=12345,
            status="accepted",
            start_check_in_date="2024-07-01",
            end_check_in_date="2024-07-31"
        )
        
        request = requests_mocker.last_request
        assert "reservation_code" in request.qs
        assert "property_id" in request.qs
        assert "status" in request.qs
    
    def test_list_reservations_invalid_status(self, mock_client):
        """Test listing reservations with invalid status."""
        with pytest.raises(ValueError, match="Invalid status"):
            mock_client.reservations.list(status="invalid_status")
    
    def test_create_reservation(self, mock_client, requests_mocker, sample_api_response):
        """Test creating a reservation."""
        requests_mocker.post(
            "https://api.hostex.io/v3/reservations",
            json=sample_api_response
        )
        
        result = mock_client.reservations.create(
            property_id="12345",
            custom_channel_id=1,
            check_in_date="2024-07-01",
            check_out_date="2024-07-07",
            guest_name="John Doe",
            currency="USD",
            rate_amount=50000,
            commission_amount=5000,
            received_amount=45000,
            income_method_id=1
        )
        
        assert result["error_code"] == 200
        
        request = requests_mocker.last_request
        request_data = request.json()
        assert request_data["property_id"] == "12345"
        assert request_data["guest_name"] == "John Doe"
        assert request_data["currency"] == "USD"
    
    def test_create_reservation_invalid_date(self, mock_client):
        """Test creating reservation with invalid date format."""
        with pytest.raises(ValueError, match="must be in YYYY-MM-DD format"):
            mock_client.reservations.create(
                property_id="12345",
                custom_channel_id=1,
                check_in_date="2024/07/01",  # Invalid format
                check_out_date="2024-07-07",
                guest_name="John Doe",
                currency="USD",
                rate_amount=50000,
                commission_amount=5000,
                received_amount=45000,
                income_method_id=1
            )
    
    def test_cancel_reservation(self, mock_client, requests_mocker, sample_api_response):
        """Test cancelling a reservation."""
        requests_mocker.delete(
            "https://api.hostex.io/v3/reservations/0-1234567-abcdef",
            json=sample_api_response
        )
        
        result = mock_client.reservations.cancel("0-1234567-abcdef")
        assert result["error_code"] == 200
    
    def test_update_lock_code(self, mock_client, requests_mocker, sample_api_response):
        """Test updating lock code."""
        requests_mocker.patch(
            "https://api.hostex.io/v3/reservations/0-1234567-abcdef/check_in_details",
            json=sample_api_response
        )
        
        result = mock_client.reservations.update_lock_code("0-1234567-abcdef", "1234")
        assert result["error_code"] == 200
        
        request = requests_mocker.last_request
        assert request.json()["lock_code"] == "1234"
    
    def test_get_custom_fields(self, mock_client, requests_mocker, sample_api_response):
        """Test getting custom fields."""
        response_data = sample_api_response.copy()
        response_data["data"] = {
            "custom_fields": {
                "lock_code": "1234",
                "wifi_password": "test123"
            }
        }
        
        requests_mocker.get(
            "https://api.hostex.io/v3/reservations/0-1234567-abcdef/custom_fields",
            json=response_data
        )
        
        result = mock_client.reservations.get_custom_fields("0-1234567-abcdef")
        assert result["data"]["custom_fields"]["lock_code"] == "1234"
    
    def test_update_custom_fields(self, mock_client, requests_mocker, sample_api_response):
        """Test updating custom fields."""
        requests_mocker.patch(
            "https://api.hostex.io/v3/reservations/0-1234567-abcdef/custom_fields",
            json=sample_api_response
        )
        
        custom_fields = {"lock_code": "5678", "delete_me": None}
        result = mock_client.reservations.update_custom_fields("0-1234567-abcdef", custom_fields)
        
        assert result["error_code"] == 200
        request = requests_mocker.last_request
        assert request.json()["custom_fields"] == custom_fields


class TestAvailabilitiesEndpoint:
    """Test AvailabilitiesEndpoint class."""
    
    def test_list_availabilities(self, mock_client, requests_mocker, sample_api_response):
        """Test listing availabilities."""
        response_data = sample_api_response.copy()
        response_data["data"] = {
            "listings": [
                {
                    "id": 12345,
                    "availabilities": [
                        {"date": "2024-07-01", "available": True, "remarks": ""},
                        {"date": "2024-07-02", "available": False, "remarks": "Maintenance"}
                    ]
                }
            ]
        }
        
        requests_mocker.get(
            "https://api.hostex.io/v3/availabilities",
            json=response_data
        )
        
        result = mock_client.availabilities.list(
            property_ids="12345,67890",
            start_date="2024-07-01",
            end_date="2024-07-31"
        )
        
        assert result["error_code"] == 200
        assert len(result["data"]["listings"][0]["availabilities"]) == 2
        
        request = requests_mocker.last_request
        assert request.qs["property_ids"] == ["12345,67890"]
        assert request.qs["start_date"] == ["2024-07-01"]
        assert request.qs["end_date"] == ["2024-07-31"]
    
    def test_list_availabilities_invalid_date(self, mock_client):
        """Test listing availabilities with invalid date format."""
        with pytest.raises(ValueError, match="must be in YYYY-MM-DD format"):
            mock_client.availabilities.list(
                property_ids="12345",
                start_date="2024/07/01",  # Invalid format
                end_date="2024-07-31"
            )
    
    def test_update_availabilities_with_date_range(self, mock_client, requests_mocker, sample_api_response):
        """Test updating availabilities with date range."""
        requests_mocker.post(
            "https://api.hostex.io/v3/availabilities",
            json=sample_api_response
        )
        
        result = mock_client.availabilities.update(
            property_ids=[12345, 67890],
            start_date="2024-07-01",
            end_date="2024-07-07",
            available=False
        )
        
        assert result["error_code"] == 200
        
        request = requests_mocker.last_request
        request_data = request.json()
        assert request_data["property_ids"] == [12345, 67890]
        assert request_data["available"] is False
        assert request_data["start_date"] == "2024-07-01"
        assert request_data["end_date"] == "2024-07-07"
    
    def test_update_availabilities_with_specific_dates(self, mock_client, requests_mocker, sample_api_response):
        """Test updating availabilities with specific dates."""
        requests_mocker.post(
            "https://api.hostex.io/v3/availabilities",
            json=sample_api_response
        )
        
        dates = ["2024-07-15", "2024-07-16", "2024-07-17"]
        result = mock_client.availabilities.update(
            property_ids=[12345],
            dates=dates,
            available=False
        )
        
        assert result["error_code"] == 200
        
        request = requests_mocker.last_request
        request_data = request.json()
        assert request_data["dates"] == dates
    
    def test_update_availabilities_missing_dates(self, mock_client):
        """Test updating availabilities without date parameters."""
        with pytest.raises(ValueError, match="Either .* or dates must be provided"):
            mock_client.availabilities.update(
                property_ids=[12345],
                available=True
                # Missing both date range and specific dates
            )


class TestListingsEndpoint:
    """Test ListingsEndpoint class."""
    
    def test_get_calendar(self, mock_client, requests_mocker, sample_api_response):
        """Test getting listing calendar."""
        response_data = sample_api_response.copy()
        response_data["data"] = {
            "listings": [
                {
                    "channel_type": "airbnb",
                    "listing_id": "12345678",
                    "calendar": [
                        {
                            "date": "2024-07-01",
                            "price": 150.0,
                            "inventory": 1,
                            "restrictions": {}
                        }
                    ]
                }
            ]
        }
        
        requests_mocker.post(
            "https://api.hostex.io/v3/listings/calendar",
            json=response_data
        )
        
        listings = [
            {"channel_type": "airbnb", "listing_id": "12345678"},
            {"channel_type": "booking.com", "listing_id": "hotel_123-rate_456"}
        ]
        
        result = mock_client.listings.get_calendar(
            start_date="2024-07-01",
            end_date="2024-07-31",
            listings=listings
        )
        
        assert result["error_code"] == 200
        assert len(result["data"]["listings"]) == 1
        
        request = requests_mocker.last_request
        request_data = request.json()
        assert request_data["listings"] == listings
    
    def test_get_calendar_invalid_listings(self, mock_client):
        """Test get calendar with invalid listings format."""
        with pytest.raises(ValueError, match="listings must be a non-empty list"):
            mock_client.listings.get_calendar(
                start_date="2024-07-01",
                end_date="2024-07-31",
                listings=[]
            )
        
        with pytest.raises(ValueError, match="Each listing must have"):
            mock_client.listings.get_calendar(
                start_date="2024-07-01",
                end_date="2024-07-31",
                listings=[{"channel_type": "airbnb"}]  # Missing listing_id
            )
    
    def test_update_inventories(self, mock_client, requests_mocker, sample_api_response):
        """Test updating inventories."""
        requests_mocker.post(
            "https://api.hostex.io/v3/listings/inventories",
            json=sample_api_response
        )
        
        inventories = [
            {"date": "2024-07-01", "inventory": 0},
            {"date": "2024-07-02", "inventory": 1}
        ]
        
        result = mock_client.listings.update_inventories(
            channel_type="airbnb",
            listing_id="12345678",
            inventories=inventories
        )
        
        assert result["error_code"] == 200
        
        request = requests_mocker.last_request
        request_data = request.json()
        assert request_data["inventories"] == inventories
    
    def test_update_prices(self, mock_client, requests_mocker, sample_api_response):
        """Test updating prices."""
        requests_mocker.post(
            "https://api.hostex.io/v3/listings/prices",
            json=sample_api_response
        )
        
        prices = [
            {"date": "2024-07-01", "price": 150.00},
            {"date": "2024-07-02", "price": 175.00}
        ]
        
        result = mock_client.listings.update_prices(
            channel_type="booking.com",
            listing_id="hotel_123-rate_456",
            prices=prices
        )
        
        assert result["error_code"] == 200
        
        request = requests_mocker.last_request
        request_data = request.json()
        assert request_data["prices"] == prices
    
    def test_update_restrictions(self, mock_client, requests_mocker, sample_api_response):
        """Test updating restrictions."""
        requests_mocker.post(
            "https://api.hostex.io/v3/listings/restrictions",
            json=sample_api_response
        )
        
        restrictions = [
            {"date": "2024-07-01", "min_stay": 3},
            {"date": "2024-07-02", "closed_to_arrival": True}
        ]
        
        result = mock_client.listings.update_restrictions(
            channel_type="vrbo",
            listing_id="vrbo_789",
            restrictions=restrictions
        )
        
        assert result["error_code"] == 200
        
        request = requests_mocker.last_request
        request_data = request.json()
        assert request_data["restrictions"] == restrictions


class TestConversationsEndpoint:
    """Test ConversationsEndpoint class."""
    
    def test_list_conversations(self, mock_client, requests_mocker, sample_api_response):
        """Test listing conversations."""
        response_data = sample_api_response.copy()
        response_data["data"] = {
            "conversations": [
                {
                    "id": "conv_123",
                    "channel_type": "airbnb",
                    "last_message_at": "2024-07-01T10:00:00+00:00",
                    "guest": {"name": "John Doe"}
                }
            ]
        }
        
        requests_mocker.get(
            "https://api.hostex.io/v3/conversations",
            json=response_data
        )
        
        result = mock_client.conversations.list(offset=10, limit=50)
        
        assert result["error_code"] == 200
        assert len(result["data"]["conversations"]) == 1
        
        request = requests_mocker.last_request
        assert request.qs == {"offset": ["10"], "limit": ["50"]}
    
    def test_get_conversation(self, mock_client, requests_mocker, sample_api_response):
        """Test getting conversation details."""
        response_data = sample_api_response.copy()
        response_data["data"] = {
            "id": "conv_123",
            "channel_type": "airbnb",
            "guest": {"name": "John Doe"},
            "messages": [
                {
                    "id": "msg_456",
                    "sender_role": "guest",
                    "content": "Hello, I have a question",
                    "created_at": "2024-07-01T10:00:00+00:00"
                }
            ]
        }
        
        requests_mocker.get(
            "https://api.hostex.io/v3/conversations/conv_123",
            json=response_data
        )
        
        result = mock_client.conversations.get("conv_123")
        
        assert result["error_code"] == 200
        assert result["data"]["id"] == "conv_123"
        assert len(result["data"]["messages"]) == 1
    
    def test_send_message_text(self, mock_client, requests_mocker, sample_api_response):
        """Test sending text message."""
        requests_mocker.post(
            "https://api.hostex.io/v3/conversations/conv_123",
            json=sample_api_response
        )
        
        result = mock_client.conversations.send_message(
            conversation_id="conv_123",
            message="Thank you for your inquiry!"
        )
        
        assert result["error_code"] == 200
        
        request = requests_mocker.last_request
        request_data = request.json()
        assert request_data["message"] == "Thank you for your inquiry!"
    
    def test_send_message_with_image(self, mock_client, requests_mocker, sample_api_response):
        """Test sending message with image."""
        requests_mocker.post(
            "https://api.hostex.io/v3/conversations/conv_123",
            json=sample_api_response
        )
        
        result = mock_client.conversations.send_message(
            conversation_id="conv_123",
            message="Here's a photo",
            jpeg_base64="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
        )
        
        assert result["error_code"] == 200
        
        request = requests_mocker.last_request
        request_data = request.json()
        assert "jpeg_base64" in request_data
    
    def test_send_message_without_content(self, mock_client):
        """Test sending message without content."""
        with pytest.raises(ValueError, match="Either message text or jpeg_base64"):
            mock_client.conversations.send_message(conversation_id="conv_123")


class TestReviewsEndpoint:
    """Test ReviewsEndpoint class."""
    
    def test_list_reviews(self, mock_client, requests_mocker, sample_api_response):
        """Test listing reviews."""
        response_data = sample_api_response.copy()
        response_data["data"] = {
            "reviews": [
                {
                    "reservation_code": "0-1234567-abcdef",
                    "property_id": 12345,
                    "channel_type": "airbnb",
                    "host_review": {"score": 5, "content": "Great guest!"},
                    "guest_review": {"score": 4, "content": "Nice place"}
                }
            ]
        }
        
        requests_mocker.get(
            "https://api.hostex.io/v3/reviews",
            json=response_data
        )
        
        result = mock_client.reviews.list(
            property_id=12345,
            start_check_out_date="2024-01-01",
            end_check_out_date="2024-07-31"
        )
        
        assert result["error_code"] == 200
        assert len(result["data"]["reviews"]) == 1
        
        request = requests_mocker.last_request
        assert "property_id" in request.qs
        assert "start_check_out_date" in request.qs
    
    def test_create_review(self, mock_client, requests_mocker, sample_api_response):
        """Test creating a review."""
        requests_mocker.post(
            "https://api.hostex.io/v3/reviews/0-1234567-abcdef",
            json=sample_api_response
        )
        
        result = mock_client.reviews.create(
            reservation_code="0-1234567-abcdef",
            host_review_score=5.0,
            host_review_content="Excellent guest!"
        )
        
        assert result["error_code"] == 200
        
        request = requests_mocker.last_request
        request_data = request.json()
        assert request_data["host_review_score"] == 5.0
        assert request_data["host_review_content"] == "Excellent guest!"
    
    def test_create_reply(self, mock_client, requests_mocker, sample_api_response):
        """Test creating a reply to review."""
        requests_mocker.post(
            "https://api.hostex.io/v3/reviews/0-1234567-abcdef",
            json=sample_api_response
        )
        
        result = mock_client.reviews.create(
            reservation_code="0-1234567-abcdef",
            host_reply_content="Thank you for the wonderful review!"
        )
        
        assert result["error_code"] == 200
        
        request = requests_mocker.last_request
        request_data = request.json()
        assert request_data["host_reply_content"] == "Thank you for the wonderful review!"
    
    def test_create_review_invalid_score(self, mock_client):
        """Test creating review with invalid score."""
        with pytest.raises(ValueError, match="must be between 0 and 5"):
            mock_client.reviews.create(
                reservation_code="0-1234567-abcdef",
                host_review_score=6.0  # Invalid score
            )
    
    def test_create_review_no_content(self, mock_client):
        """Test creating review without any content."""
        with pytest.raises(ValueError, match="At least one of"):
            mock_client.reviews.create(reservation_code="0-1234567-abcdef")


class TestWebhooksEndpoint:
    """Test WebhooksEndpoint class."""
    
    def test_list_webhooks(self, mock_client, requests_mocker, sample_api_response):
        """Test listing webhooks."""
        response_data = sample_api_response.copy()
        response_data["data"] = {
            "webhooks": [
                {
                    "id": 1,
                    "url": "https://example.com/webhook",
                    "manageable": True,
                    "created_at": "2024-07-01T10:00:00+00:00"
                }
            ]
        }
        
        requests_mocker.get(
            "https://api.hostex.io/v3/webhooks",
            json=response_data
        )
        
        result = mock_client.webhooks.list()
        
        assert result["error_code"] == 200
        assert len(result["data"]["webhooks"]) == 1
    
    def test_create_webhook(self, mock_client, requests_mocker, sample_api_response):
        """Test creating a webhook."""
        requests_mocker.post(
            "https://api.hostex.io/v3/webhooks",
            json=sample_api_response
        )
        
        result = mock_client.webhooks.create("https://example.com/webhook")
        
        assert result["error_code"] == 200
        
        request = requests_mocker.last_request
        request_data = request.json()
        assert request_data["url"] == "https://example.com/webhook"
    
    def test_create_webhook_invalid_url(self, mock_client):
        """Test creating webhook with invalid URL."""
        with pytest.raises(ValueError, match="URL must start with http"):
            mock_client.webhooks.create("invalid-url")
        
        with pytest.raises(ValueError, match="URL is required"):
            mock_client.webhooks.create("")
    
    def test_delete_webhook(self, mock_client, requests_mocker, sample_api_response):
        """Test deleting a webhook."""
        requests_mocker.delete(
            "https://api.hostex.io/v3/webhooks/123",
            json=sample_api_response
        )
        
        result = mock_client.webhooks.delete(123)
        assert result["error_code"] == 200