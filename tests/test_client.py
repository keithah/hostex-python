"""
Tests for the main HostexClient class.
"""

import pytest
import requests_mock
from hostex import HostexClient
from hostex.exceptions import (
    InvalidConfigError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    NotFoundError,
    HostexAPIError,
)


class TestHostexClient:
    """Test the main HostexClient class."""
    
    def test_init_with_access_token(self):
        """Test client initialization with access token."""
        client = HostexClient(access_token="test_token")
        assert client.auth.access_token == "test_token"
        assert client.base_url == "https://api.hostex.io/v3"
        assert client.timeout == 30
    
    def test_init_with_oauth(self):
        """Test client initialization with OAuth."""
        client = HostexClient(
            client_id="test_id",
            client_secret="test_secret",
            redirect_uri="https://example.com/callback"
        )
        assert client.auth.client_id == "test_id"
        assert client.auth.client_secret == "test_secret"
        assert client.auth.redirect_uri == "https://example.com/callback"
    
    def test_init_without_auth(self):
        """Test client initialization without auth parameters."""
        with pytest.raises(InvalidConfigError):
            HostexClient()
    
    def test_init_with_custom_params(self):
        """Test client initialization with custom parameters."""
        client = HostexClient(
            access_token="test_token",
            base_url="https://custom.api.com",
            timeout=60,
            user_agent="MyApp/1.0"
        )
        assert client.base_url == "https://custom.api.com"
        assert client.timeout == 60
        assert client.user_agent == "MyApp/1.0"
    
    def test_set_access_token(self):
        """Test setting access token."""
        client = HostexClient(access_token="old_token")
        client.set_access_token("new_token")
        assert client.auth.access_token == "new_token"


class TestClientRequests:
    """Test client HTTP request methods."""
    
    def test_successful_request(self, mock_client, requests_mocker):
        """Test successful API request."""
        requests_mocker.get(
            "https://api.hostex.io/v3/test",
            json={
                "request_id": "req_123",
                "error_code": 200,
                "error_msg": "Success",
                "data": {"test": "value"}
            }
        )
        
        response = mock_client.get("test")
        assert response["error_code"] == 200
        assert response["data"]["test"] == "value"
    
    def test_authentication_error(self, mock_client, requests_mocker):
        """Test authentication error handling."""
        requests_mocker.get(
            "https://api.hostex.io/v3/test",
            json={
                "request_id": "req_123",
                "error_code": 401,
                "error_msg": "Unauthorized"
            }
        )
        
        with pytest.raises(AuthenticationError) as exc_info:
            mock_client.get("test")
        assert exc_info.value.error_code == 401
    
    def test_validation_error(self, mock_client, requests_mocker):
        """Test validation error handling."""
        requests_mocker.post(
            "https://api.hostex.io/v3/test",
            json={
                "request_id": "req_123",
                "error_code": 400,
                "error_msg": "Validation failed"
            }
        )
        
        with pytest.raises(ValidationError) as exc_info:
            mock_client.post("test", json={"invalid": "data"})
        assert exc_info.value.error_code == 400
    
    def test_not_found_error(self, mock_client, requests_mocker):
        """Test not found error handling."""
        requests_mocker.get(
            "https://api.hostex.io/v3/test/nonexistent",
            json={
                "request_id": "req_123",
                "error_code": 404,
                "error_msg": "Resource not found"
            }
        )
        
        with pytest.raises(NotFoundError) as exc_info:
            mock_client.get("test/nonexistent")
        assert exc_info.value.error_code == 404
    
    def test_rate_limit_error_with_retry(self, mock_client, requests_mocker):
        """Test rate limit error with automatic retry."""
        # First call returns rate limit error
        requests_mocker.get(
            "https://api.hostex.io/v3/test",
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
                    "json": {
                        "request_id": "req_124", 
                        "error_code": 200,
                        "error_msg": "Success",
                        "data": {"test": "value"}
                    }
                }
            ]
        )
        
        response = mock_client.get("test")
        assert response["error_code"] == 200
        assert len(requests_mocker.request_history) == 2
    
    def test_rate_limit_error_max_retries(self, mock_client, requests_mocker):
        """Test rate limit error exceeding max retries."""
        requests_mocker.get(
            "https://api.hostex.io/v3/test",
            json={
                "request_id": "req_123",
                "error_code": 429,
                "error_msg": "Rate limit exceeded"
            },
            status_code=429,
            headers={"Retry-After": "1"}
        )
        
        with pytest.raises(RateLimitError) as exc_info:
            mock_client.get("test", max_retries=2)
        assert exc_info.value.error_code == 429
        assert exc_info.value.retry_after == 1
    
    def test_server_error(self, mock_client, requests_mocker):
        """Test server error handling."""
        requests_mocker.get(
            "https://api.hostex.io/v3/test",
            json={
                "request_id": "req_123",
                "error_code": 500,
                "error_msg": "Internal server error"
            },
            status_code=500
        )
        
        with pytest.raises(HostexAPIError) as exc_info:
            mock_client.get("test")
        assert exc_info.value.error_code == 500
    
    def test_request_headers(self, mock_client, requests_mocker):
        """Test that proper headers are sent."""
        requests_mocker.get(
            "https://api.hostex.io/v3/test",
            json={
                "request_id": "req_123",
                "error_code": 200,
                "error_msg": "Success"
            }
        )
        
        mock_client.get("test")
        
        request = requests_mocker.last_request
        assert request.headers["Hostex-Access-Token"] == "test_token_12345"
        assert request.headers["User-Agent"] == "hostex-python/1.0.0"
        assert request.headers["Content-Type"] == "application/json"
    
    def test_custom_headers(self, mock_client, requests_mocker):
        """Test custom headers are included."""
        requests_mocker.get(
            "https://api.hostex.io/v3/test",
            json={
                "request_id": "req_123",
                "error_code": 200,
                "error_msg": "Success"
            }
        )
        
        custom_headers = {"X-Custom-Header": "test-value"}
        mock_client.get("test", headers=custom_headers)
        
        request = requests_mocker.last_request
        assert request.headers["X-Custom-Header"] == "test-value"
    
    def test_get_method(self, mock_client, requests_mocker):
        """Test GET method wrapper."""
        requests_mocker.get(
            "https://api.hostex.io/v3/test",
            json={
                "request_id": "req_123",
                "error_code": 200,
                "error_msg": "Success"
            }
        )
        
        params = {"param1": "value1"}
        mock_client.get("test", params=params)
        
        request = requests_mocker.last_request
        assert request.method == "GET"
        assert request.qs == {"param1": ["value1"]}
    
    def test_post_method(self, mock_client, requests_mocker):
        """Test POST method wrapper."""
        requests_mocker.post(
            "https://api.hostex.io/v3/test",
            json={
                "request_id": "req_123",
                "error_code": 200,
                "error_msg": "Success"
            }
        )
        
        data = {"field1": "value1"}
        mock_client.post("test", json=data)
        
        request = requests_mocker.last_request
        assert request.method == "POST"
        assert request.json() == data
    
    def test_patch_method(self, mock_client, requests_mocker):
        """Test PATCH method wrapper."""
        requests_mocker.patch(
            "https://api.hostex.io/v3/test",
            json={
                "request_id": "req_123",
                "error_code": 200,
                "error_msg": "Success"
            }
        )
        
        data = {"field1": "updated_value"}
        mock_client.patch("test", json=data)
        
        request = requests_mocker.last_request
        assert request.method == "PATCH"
        assert request.json() == data
    
    def test_delete_method(self, mock_client, requests_mocker):
        """Test DELETE method wrapper."""
        requests_mocker.delete(
            "https://api.hostex.io/v3/test/123",
            json={
                "request_id": "req_123",
                "error_code": 200,
                "error_msg": "Success"
            }
        )
        
        mock_client.delete("test/123")
        
        request = requests_mocker.last_request
        assert request.method == "DELETE"


class TestEndpointInitialization:
    """Test that all endpoint classes are properly initialized."""
    
    def test_endpoints_initialized(self, mock_client):
        """Test that all endpoint objects are created."""
        assert mock_client.properties is not None
        assert mock_client.room_types is not None
        assert mock_client.reservations is not None
        assert mock_client.availabilities is not None
        assert mock_client.listings is not None
        assert mock_client.conversations is not None
        assert mock_client.reviews is not None
        assert mock_client.webhooks is not None
        assert mock_client.custom_channels is not None
        assert mock_client.income_methods is not None
    
    def test_oauth_property_for_oauth_client(self, oauth_client):
        """Test that OAuth client has oauth property."""
        assert oauth_client.oauth is not None
        assert oauth_client.oauth == oauth_client.auth