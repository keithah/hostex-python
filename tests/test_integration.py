"""
Integration tests for the Hostex API client.
"""

import pytest
import requests_mock
from hostex import HostexClient


class TestIntegrationWorkflows:
    """Test complete workflows using multiple endpoints."""
    
    def test_property_management_workflow(self, mock_client, requests_mocker, sample_property, sample_api_response):
        """Test a complete property management workflow."""
        # Mock getting properties
        properties_response = sample_api_response.copy()
        properties_response["data"] = {
            "properties": [sample_property],
            "total": 1
        }
        requests_mocker.get(
            "https://api.hostex.io/v3/properties",
            json=properties_response
        )
        
        # Mock getting availabilities
        availability_response = sample_api_response.copy()
        availability_response["data"] = {
            "listings": [
                {
                    "id": 12345,
                    "availabilities": [
                        {"date": "2024-07-01", "available": True, "remarks": ""},
                        {"date": "2024-07-02", "available": True, "remarks": ""}
                    ]
                }
            ]
        }
        requests_mocker.get(
            "https://api.hostex.io/v3/availabilities",
            json=availability_response
        )
        
        # Mock updating availability
        requests_mocker.post(
            "https://api.hostex.io/v3/availabilities",
            json=sample_api_response
        )
        
        # Execute workflow
        # 1. Get properties
        properties = mock_client.properties.list(limit=10)
        assert len(properties["data"]["properties"]) == 1
        property_id = properties["data"]["properties"][0]["id"]
        
        # 2. Check current availability
        availabilities = mock_client.availabilities.list(
            property_ids=str(property_id),
            start_date="2024-07-01",
            end_date="2024-07-02"
        )
        assert len(availabilities["data"]["listings"]) == 1
        
        # 3. Update availability (block dates)
        update_result = mock_client.availabilities.update(
            property_ids=[property_id],
            dates=["2024-07-01", "2024-07-02"],
            available=False
        )
        assert update_result["error_code"] == 200
        
        # Verify all calls were made
        assert len(requests_mocker.request_history) == 3
    
    def test_reservation_workflow(self, mock_client, requests_mocker, sample_reservation, sample_api_response):
        """Test a complete reservation management workflow."""
        # Mock custom channels and income methods
        channels_response = sample_api_response.copy()
        channels_response["data"] = {
            "custom_channels": [
                {"id": 1, "name": "Direct Website"}
            ]
        }
        requests_mocker.get(
            "https://api.hostex.io/v3/custom_channels",
            json=channels_response
        )
        
        income_methods_response = sample_api_response.copy()
        income_methods_response["data"] = {
            "custom_channels": [  # Note: API returns "custom_channels" for income methods too
                {"id": 1, "name": "Bank Transfer"}
            ]
        }
        requests_mocker.get(
            "https://api.hostex.io/v3/income_methods",
            json=income_methods_response
        )
        
        # Mock creating reservation
        create_response = sample_api_response.copy()
        create_response["reservation_code"] = "0-1234567-abcdef"
        requests_mocker.post(
            "https://api.hostex.io/v3/reservations",
            json=create_response
        )
        
        # Mock querying created reservation
        reservations_response = sample_api_response.copy()
        reservations_response["data"] = {
            "reservations": [sample_reservation]
        }
        requests_mocker.get(
            "https://api.hostex.io/v3/reservations",
            json=reservations_response
        )
        
        # Mock updating custom fields
        requests_mocker.patch(
            "https://api.hostex.io/v3/reservations/0-1234567-abcdef/custom_fields",
            json=sample_api_response
        )
        
        # Execute workflow
        # 1. Get required data for reservation creation
        channels = mock_client.custom_channels.list()
        income_methods = mock_client.income_methods.list()
        
        channel_id = channels["data"]["custom_channels"][0]["id"]
        income_method_id = income_methods["data"]["custom_channels"][0]["id"]
        
        # 2. Create reservation
        reservation = mock_client.reservations.create(
            property_id="12345",
            custom_channel_id=channel_id,
            check_in_date="2024-07-01",
            check_out_date="2024-07-07",
            guest_name="John Doe",
            currency="USD",
            rate_amount=84000,  # $840
            commission_amount=8400,  # 10%
            received_amount=75600,
            income_method_id=income_method_id
        )
        
        # 3. Verify reservation was created
        reservations = mock_client.reservations.list(
            reservation_code="0-1234567-abcdef"
        )
        assert len(reservations["data"]["reservations"]) == 1
        
        # 4. Add custom fields (e.g., lock code)
        custom_fields_result = mock_client.reservations.update_custom_fields(
            stay_code="0-1234567-abcdef",
            custom_fields={
                "lock_code": "1234",
                "wifi_password": "GuestWiFi2024"
            }
        )
        assert custom_fields_result["error_code"] == 200
        
        # Verify all calls were made
        assert len(requests_mocker.request_history) == 5
    
    def test_messaging_workflow(self, mock_client, requests_mocker, sample_api_response):
        """Test a complete messaging workflow."""
        # Mock listing conversations
        conversations_response = sample_api_response.copy()
        conversations_response["data"] = {
            "conversations": [
                {
                    "id": "conv_123",
                    "channel_type": "airbnb",
                    "last_message_at": "2024-07-01T10:00:00+00:00",
                    "guest": {"name": "Jane Smith"},
                    "property_title": "Beautiful Apartment",
                    "check_in_date": "2024-07-15",
                    "check_out_date": "2024-07-20"
                }
            ]
        }
        requests_mocker.get(
            "https://api.hostex.io/v3/conversations",
            json=conversations_response
        )
        
        # Mock getting conversation details
        conversation_response = sample_api_response.copy()
        conversation_response["data"] = {
            "id": "conv_123",
            "channel_type": "airbnb",
            "guest": {"name": "Jane Smith", "email": "jane@example.com"},
            "activities": [],
            "note": "",
            "messages": [
                {
                    "id": "msg_456",
                    "sender_role": "guest",
                    "display_type": "text",
                    "content": "Hi, I have a question about check-in",
                    "attachment": None,
                    "created_at": "2024-07-01T10:00:00+00:00"
                }
            ]
        }
        requests_mocker.get(
            "https://api.hostex.io/v3/conversations/conv_123",
            json=conversation_response
        )
        
        # Mock sending message
        requests_mocker.post(
            "https://api.hostex.io/v3/conversations/conv_123",
            json=sample_api_response
        )
        
        # Execute workflow
        # 1. Get all conversations
        conversations = mock_client.conversations.list(limit=50)
        assert len(conversations["data"]["conversations"]) == 1
        
        # 2. Get details for first conversation
        conv_id = conversations["data"]["conversations"][0]["id"]
        conversation = mock_client.conversations.get(conv_id)
        assert conversation["data"]["id"] == "conv_123"
        assert len(conversation["data"]["messages"]) == 1
        
        # 3. Send a response
        response_result = mock_client.conversations.send_message(
            conversation_id=conv_id,
            message="Hello! Check-in is at 3 PM. The door code will be sent 24 hours before your arrival."
        )
        assert response_result["error_code"] == 200
        
        # Verify all calls were made
        assert len(requests_mocker.request_history) == 3
    
    def test_review_management_workflow(self, mock_client, requests_mocker, sample_api_response):
        """Test review management workflow."""
        # Mock getting reviews
        reviews_response = sample_api_response.copy()
        reviews_response["data"] = {
            "reviews": [
                {
                    "reservation_code": "0-1234567-abcdef",
                    "property_id": 12345,
                    "channel_type": "airbnb",
                    "listing_id": "airbnb_123",
                    "check_in_date": "2024-06-01",
                    "check_out_date": "2024-06-07",
                    "host_review": None,
                    "guest_review": {
                        "score": 5,
                        "content": "Amazing place! Highly recommend.",
                        "created_at": "2024-06-08T10:00:00+00:00"
                    },
                    "host_reply": None
                }
            ]
        }
        requests_mocker.get(
            "https://api.hostex.io/v3/reviews",
            json=reviews_response
        )
        
        # Mock creating host review
        requests_mocker.post(
            "https://api.hostex.io/v3/reviews/0-1234567-abcdef",
            json=sample_api_response
        )
        
        # Execute workflow
        # 1. Get reviews that need host response
        reviews = mock_client.reviews.list(
            start_check_out_date="2024-06-01",
            end_check_out_date="2024-06-30"
        )
        assert len(reviews["data"]["reviews"]) == 1
        
        # 2. Process reviews needing responses
        review = reviews["data"]["reviews"][0]
        reservation_code = review["reservation_code"]
        
        # Guest left a review but no host review yet
        if review["guest_review"] and not review["host_review"]:
            # Create host review of guest
            host_review_result = mock_client.reviews.create(
                reservation_code=reservation_code,
                host_review_score=5.0,
                host_review_content="Wonderful guest! Very clean and respectful."
            )
            assert host_review_result["error_code"] == 200
        
        # Guest left a review but no host reply yet
        if review["guest_review"] and not review["host_reply"]:
            # Reply to guest review
            reply_result = mock_client.reviews.create(
                reservation_code=reservation_code,
                host_reply_content="Thank you so much for the kind words! We're thrilled you enjoyed your stay."
            )
            assert reply_result["error_code"] == 200
        
        # Verify calls were made
        assert len(requests_mocker.request_history) == 3
    
    def test_webhook_setup_workflow(self, mock_client, requests_mocker, sample_api_response):
        """Test webhook setup workflow."""
        # Mock listing existing webhooks
        webhooks_response = sample_api_response.copy()
        webhooks_response["data"] = {
            "webhooks": [
                {
                    "id": 1,
                    "url": "https://old-app.com/webhook",
                    "manageable": False,  # Can't delete this one
                    "created_at": "2024-01-01T10:00:00+00:00"
                }
            ]
        }
        requests_mocker.get(
            "https://api.hostex.io/v3/webhooks",
            json=webhooks_response
        )
        
        # Mock creating new webhook
        create_webhook_response = sample_api_response.copy()
        create_webhook_response["webhook_id"] = 2
        requests_mocker.post(
            "https://api.hostex.io/v3/webhooks",
            json=create_webhook_response
        )
        
        # Execute workflow
        # 1. Check existing webhooks
        existing_webhooks = mock_client.webhooks.list()
        assert len(existing_webhooks["data"]["webhooks"]) == 1
        
        # 2. Create new webhook for our application
        new_webhook = mock_client.webhooks.create("https://my-app.com/hostex-webhook")
        assert new_webhook["error_code"] == 200
        
        # Verify calls were made
        assert len(requests_mocker.request_history) == 2


class TestErrorRecoveryWorkflows:
    """Test error handling and recovery workflows."""
    
    def test_token_refresh_workflow(self, oauth_client, requests_mocker, sample_api_response):
        """Test automatic token refresh workflow."""
        # Set initial tokens that are expired
        oauth_client.auth.set_tokens(
            access_token="expired_token",
            refresh_token="valid_refresh_token",
            expires_in=-3600  # Expired 1 hour ago
        )
        
        # Mock token refresh
        refresh_response = sample_api_response.copy()
        refresh_response["data"] = {
            "access_token": "new_access_token",
            "refresh_token": "new_refresh_token",
            "expires_in": 7200
        }
        requests_mocker.post(
            "https://api.hostex.io/v3/oauth/authorizations",
            json=refresh_response
        )
        
        # Mock API call after token refresh
        requests_mocker.get(
            "https://api.hostex.io/v3/properties",
            json=sample_api_response
        )
        
        # Make API call - should trigger automatic token refresh
        result = oauth_client.properties.list()
        assert result["error_code"] == 200
        
        # Verify token was refreshed
        assert oauth_client.auth.access_token == "new_access_token"
        
        # Check that both refresh and API calls were made
        assert len(requests_mocker.request_history) == 2
        
        # First call should be token refresh
        refresh_request = requests_mocker.request_history[0]
        assert refresh_request.json()["grant_type"] == "refresh_token"
        
        # Second call should be the actual API request with new token
        api_request = requests_mocker.request_history[1]
        assert api_request.headers["Hostex-Access-Token"] == "new_access_token"
    
    def test_rate_limit_retry_workflow(self, mock_client, requests_mocker, sample_api_response):
        """Test rate limit handling with retries."""
        # First call returns rate limit, second succeeds
        requests_mocker.get(
            "https://api.hostex.io/v3/properties",
            [
                {
                    "json": {
                        "request_id": "req_123",
                        "error_code": 429,
                        "error_msg": "Rate limit exceeded"
                    },
                    "status_code": 429,
                    "headers": {"Retry-After": "1"}
                },
                {
                    "json": sample_api_response
                }
            ]
        )
        
        # Make API call - should retry automatically
        result = mock_client.properties.list()
        assert result["error_code"] == 200
        
        # Verify retry was attempted
        assert len(requests_mocker.request_history) == 2
    
    def test_batch_operations_with_partial_failures(self, mock_client, requests_mocker, sample_api_response):
        """Test batch operations handling partial failures."""
        property_ids = [12345, 67890, 11111]
        
        # Mock responses: first succeeds, second fails, third succeeds
        update_responses = [
            sample_api_response,  # Success
            {
                "request_id": "req_124", 
                "error_code": 400,
                "error_msg": "Invalid property ID"
            },  # Failure
            sample_api_response   # Success
        ]
        
        for i, property_id in enumerate(property_ids):
            requests_mocker.post(
                "https://api.hostex.io/v3/availabilities",
                json=update_responses[i % len(update_responses)]
            )
        
        # Simulate batch update with error handling
        results = []
        for property_id in property_ids:
            try:
                result = mock_client.availabilities.update(
                    property_ids=[property_id],
                    dates=["2024-07-15"],
                    available=False
                )
                results.append({"property_id": property_id, "success": True, "result": result})
            except Exception as e:
                results.append({"property_id": property_id, "success": False, "error": str(e)})
        
        # Verify results
        assert len(results) == 3
        assert results[0]["success"] is True
        assert results[1]["success"] is False
        assert results[2]["success"] is True
        
        # Verify all calls were made
        assert len(requests_mocker.request_history) == 3