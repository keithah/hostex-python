"""
Tests for utility endpoints.
"""

import pytest
import requests_mock


class TestCustomChannelsEndpoint:
    """Test CustomChannelsEndpoint class."""
    
    def test_list_custom_channels(self, mock_client, requests_mocker, sample_api_response):
        """Test listing custom channels."""
        response_data = sample_api_response.copy()
        response_data["data"] = {
            "custom_channels": [
                {"id": 1, "name": "Direct Website"},
                {"id": 2, "name": "Phone Bookings"},
                {"id": 3, "name": "Email Inquiries"}
            ]
        }
        
        requests_mocker.get(
            "https://api.hostex.io/v3/custom_channels",
            json=response_data
        )
        
        result = mock_client.custom_channels.list()
        
        assert result["error_code"] == 200
        assert len(result["data"]["custom_channels"]) == 3
        assert result["data"]["custom_channels"][0]["name"] == "Direct Website"
        assert result["data"]["custom_channels"][1]["name"] == "Phone Bookings"
        
        # Verify request was made correctly
        request = requests_mocker.last_request
        assert request.method == "GET"
        assert request.path == "/v3/custom_channels"


class TestIncomeMethodsEndpoint:
    """Test IncomeMethodsEndpoint class."""
    
    def test_list_income_methods(self, mock_client, requests_mocker, sample_api_response):
        """Test listing income methods."""
        response_data = sample_api_response.copy()
        response_data["data"] = {
            "custom_channels": [  # Note: API returns "custom_channels" key for income methods
                {"id": 1, "name": "Bank Transfer"},
                {"id": 2, "name": "Credit Card"},
                {"id": 3, "name": "Cash"},
                {"id": 4, "name": "PayPal"}
            ]
        }
        
        requests_mocker.get(
            "https://api.hostex.io/v3/income_methods",
            json=response_data
        )
        
        result = mock_client.income_methods.list()
        
        assert result["error_code"] == 200
        assert len(result["data"]["custom_channels"]) == 4
        assert result["data"]["custom_channels"][0]["name"] == "Bank Transfer"
        assert result["data"]["custom_channels"][1]["name"] == "Credit Card"
        assert result["data"]["custom_channels"][2]["name"] == "Cash"
        assert result["data"]["custom_channels"][3]["name"] == "PayPal"
        
        # Verify request was made correctly
        request = requests_mocker.last_request
        assert request.method == "GET"
        assert request.path == "/v3/income_methods"


class TestEndpointMethodsExist:
    """Test that all expected endpoint methods exist."""
    
    def test_properties_endpoint_methods(self, mock_client):
        """Test PropertiesEndpoint has expected methods."""
        assert hasattr(mock_client.properties, 'list')
        assert callable(mock_client.properties.list)
    
    def test_room_types_endpoint_methods(self, mock_client):
        """Test RoomTypesEndpoint has expected methods."""
        assert hasattr(mock_client.room_types, 'list')
        assert callable(mock_client.room_types.list)
    
    def test_reservations_endpoint_methods(self, mock_client):
        """Test ReservationsEndpoint has expected methods."""
        expected_methods = ['list', 'create', 'cancel', 'update_lock_code', 'get_custom_fields', 'update_custom_fields']
        for method in expected_methods:
            assert hasattr(mock_client.reservations, method)
            assert callable(getattr(mock_client.reservations, method))
    
    def test_availabilities_endpoint_methods(self, mock_client):
        """Test AvailabilitiesEndpoint has expected methods."""
        expected_methods = ['list', 'update']
        for method in expected_methods:
            assert hasattr(mock_client.availabilities, method)
            assert callable(getattr(mock_client.availabilities, method))
    
    def test_listings_endpoint_methods(self, mock_client):
        """Test ListingsEndpoint has expected methods."""
        expected_methods = ['get_calendar', 'update_inventories', 'update_prices', 'update_restrictions']
        for method in expected_methods:
            assert hasattr(mock_client.listings, method)
            assert callable(getattr(mock_client.listings, method))
    
    def test_conversations_endpoint_methods(self, mock_client):
        """Test ConversationsEndpoint has expected methods."""
        expected_methods = ['list', 'get', 'send_message']
        for method in expected_methods:
            assert hasattr(mock_client.conversations, method)
            assert callable(getattr(mock_client.conversations, method))
    
    def test_reviews_endpoint_methods(self, mock_client):
        """Test ReviewsEndpoint has expected methods."""
        expected_methods = ['list', 'create']
        for method in expected_methods:
            assert hasattr(mock_client.reviews, method)
            assert callable(getattr(mock_client.reviews, method))
    
    def test_webhooks_endpoint_methods(self, mock_client):
        """Test WebhooksEndpoint has expected methods."""
        expected_methods = ['list', 'create', 'delete']
        for method in expected_methods:
            assert hasattr(mock_client.webhooks, method)
            assert callable(getattr(mock_client.webhooks, method))
    
    def test_custom_channels_endpoint_methods(self, mock_client):
        """Test CustomChannelsEndpoint has expected methods."""
        assert hasattr(mock_client.custom_channels, 'list')
        assert callable(mock_client.custom_channels.list)
    
    def test_income_methods_endpoint_methods(self, mock_client):
        """Test IncomeMethodsEndpoint has expected methods."""
        assert hasattr(mock_client.income_methods, 'list')
        assert callable(mock_client.income_methods.list)