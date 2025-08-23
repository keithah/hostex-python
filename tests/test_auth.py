"""
Tests for authentication classes.
"""

import pytest
import requests_mock
import time
from hostex.auth import TokenAuth, OAuthAuth
from hostex.exceptions import (
    InvalidConfigError,
    AuthenticationError,
    ValidationError,
)


class TestTokenAuth:
    """Test TokenAuth class."""
    
    def test_init_with_token(self):
        """Test TokenAuth initialization with valid token."""
        auth = TokenAuth("test_token_123")
        assert auth.access_token == "test_token_123"
    
    def test_init_without_token(self):
        """Test TokenAuth initialization without token."""
        with pytest.raises(InvalidConfigError):
            TokenAuth("")
        
        with pytest.raises(InvalidConfigError):
            TokenAuth(None)
    
    def test_get_headers(self):
        """Test getting authentication headers."""
        auth = TokenAuth("test_token_123")
        headers = auth.get_headers()
        assert headers["Hostex-Access-Token"] == "test_token_123"


class TestOAuthAuth:
    """Test OAuthAuth class."""
    
    def test_init_with_required_params(self):
        """Test OAuthAuth initialization with required parameters."""
        auth = OAuthAuth(
            client_id="test_id",
            client_secret="test_secret"
        )
        assert auth.client_id == "test_id"
        assert auth.client_secret == "test_secret"
    
    def test_init_without_required_params(self):
        """Test OAuthAuth initialization without required parameters."""
        with pytest.raises(InvalidConfigError):
            OAuthAuth(client_id="", client_secret="test_secret")
        
        with pytest.raises(InvalidConfigError):
            OAuthAuth(client_id="test_id", client_secret="")
    
    def test_init_with_all_params(self):
        """Test OAuthAuth initialization with all parameters."""
        auth = OAuthAuth(
            client_id="test_id",
            client_secret="test_secret",
            redirect_uri="https://example.com/callback",
            access_token="access_123",
            refresh_token="refresh_123",
            expires_at=time.time() + 3600
        )
        assert auth.redirect_uri == "https://example.com/callback"
        assert auth.access_token == "access_123"
        assert auth.refresh_token == "refresh_123"
    
    def test_get_headers_without_token(self):
        """Test getting headers without access token."""
        auth = OAuthAuth(
            client_id="test_id",
            client_secret="test_secret"
        )
        
        with pytest.raises(AuthenticationError):
            auth.get_headers()
    
    def test_get_headers_with_token(self):
        """Test getting headers with access token."""
        auth = OAuthAuth(
            client_id="test_id",
            client_secret="test_secret",
            access_token="access_123"
        )
        
        headers = auth.get_headers()
        assert headers["Hostex-Access-Token"] == "access_123"
    
    def test_is_token_expired(self):
        """Test token expiration checking."""
        auth = OAuthAuth(
            client_id="test_id",
            client_secret="test_secret"
        )
        
        # No expiration time set
        assert not auth.is_token_expired()
        
        # Token expires in future
        auth.expires_at = time.time() + 3600
        assert not auth.is_token_expired()
        
        # Token expired
        auth.expires_at = time.time() - 3600
        assert auth.is_token_expired()
        
        # Token expires very soon (within buffer)
        auth.expires_at = time.time() + 30
        assert auth.is_token_expired()
    
    def test_get_authorization_url(self):
        """Test authorization URL generation."""
        auth = OAuthAuth(
            client_id="test_id",
            client_secret="test_secret",
            redirect_uri="https://example.com/callback"
        )
        
        url = auth.get_authorization_url()
        assert url.startswith("https://hostex.io/app/authorization?")
        assert "client_id=test_id" in url
        assert "redirect_uri=https%3A//example.com/callback" in url
    
    def test_get_authorization_url_with_state(self):
        """Test authorization URL generation with state."""
        auth = OAuthAuth(
            client_id="test_id",
            client_secret="test_secret",
            redirect_uri="https://example.com/callback"
        )
        
        url = auth.get_authorization_url(state="random_state_123")
        assert "state=random_state_123" in url
    
    def test_get_authorization_url_without_redirect_uri(self):
        """Test authorization URL generation without redirect URI."""
        auth = OAuthAuth(
            client_id="test_id",
            client_secret="test_secret"
        )
        
        with pytest.raises(InvalidConfigError):
            auth.get_authorization_url()
    
    def test_get_access_token(self):
        """Test getting access token with authorization code."""
        auth = OAuthAuth(
            client_id="test_id",
            client_secret="test_secret"
        )
        
        with requests_mock.Mocker() as m:
            m.post(
                "https://api.hostex.io/v3/oauth/authorizations",
                json={
                    "request_id": "req_123",
                    "error_code": 200,
                    "error_msg": "Success",
                    "data": {
                        "access_token": "new_access_token",
                        "refresh_token": "new_refresh_token",
                        "expires_in": 3600
                    }
                }
            )
            
            token_data = auth.get_access_token("auth_code_123")
            
            assert token_data["access_token"] == "new_access_token"
            assert token_data["refresh_token"] == "new_refresh_token"
            assert auth.access_token == "new_access_token"
            assert auth.refresh_token == "new_refresh_token"
            
            # Check request was made correctly
            request = m.last_request
            request_data = request.json()
            assert request_data["client_id"] == "test_id"
            assert request_data["client_secret"] == "test_secret"
            assert request_data["grant_type"] == "authorization_code"
            assert request_data["code"] == "auth_code_123"
    
    def test_refresh_access_token(self):
        """Test refreshing access token."""
        auth = OAuthAuth(
            client_id="test_id",
            client_secret="test_secret",
            refresh_token="refresh_123"
        )
        
        with requests_mock.Mocker() as m:
            m.post(
                "https://api.hostex.io/v3/oauth/authorizations",
                json={
                    "request_id": "req_123",
                    "error_code": 200,
                    "error_msg": "Success",
                    "data": {
                        "access_token": "refreshed_access_token",
                        "refresh_token": "new_refresh_token",
                        "expires_in": 3600
                    }
                }
            )
            
            token_data = auth.refresh_access_token()
            
            assert token_data["access_token"] == "refreshed_access_token"
            assert auth.access_token == "refreshed_access_token"
            
            # Check request was made correctly
            request = m.last_request
            request_data = request.json()
            assert request_data["grant_type"] == "refresh_token"
            assert request_data["refresh_token"] == "refresh_123"
    
    def test_refresh_access_token_without_refresh_token(self):
        """Test refreshing access token without refresh token."""
        auth = OAuthAuth(
            client_id="test_id",
            client_secret="test_secret"
        )
        
        with pytest.raises(AuthenticationError):
            auth.refresh_access_token()
    
    def test_revoke_token(self):
        """Test revoking a token."""
        auth = OAuthAuth(
            client_id="test_id",
            client_secret="test_secret",
            access_token="token_to_revoke"
        )
        
        with requests_mock.Mocker() as m:
            m.post(
                "https://api.hostex.io/v3/oauth/revoke",
                json={
                    "request_id": "req_123",
                    "error_code": 200,
                    "error_msg": "Success"
                }
            )
            
            result = auth.revoke_token()
            
            assert result["error_code"] == 200
            assert auth.access_token is None  # Token should be cleared
            
            # Check request was made correctly
            request = m.last_request
            request_data = request.json()
            assert request_data["client_id"] == "test_id"
            assert request_data["client_secret"] == "test_secret"
            assert request_data["token"] == "token_to_revoke"
    
    def test_revoke_specific_token(self):
        """Test revoking a specific token."""
        auth = OAuthAuth(
            client_id="test_id",
            client_secret="test_secret",
            access_token="current_token",
            refresh_token="refresh_token"
        )
        
        with requests_mock.Mocker() as m:
            m.post(
                "https://api.hostex.io/v3/oauth/revoke",
                json={
                    "request_id": "req_123",
                    "error_code": 200,
                    "error_msg": "Success"
                }
            )
            
            auth.revoke_token("refresh_token")
            
            # Access token should still be there, refresh token cleared
            assert auth.access_token == "current_token"
            assert auth.refresh_token is None
    
    def test_set_tokens(self):
        """Test setting tokens manually."""
        auth = OAuthAuth(
            client_id="test_id",
            client_secret="test_secret"
        )
        
        auth.set_tokens(
            access_token="manual_access_token",
            refresh_token="manual_refresh_token",
            expires_in=7200
        )
        
        assert auth.access_token == "manual_access_token"
        assert auth.refresh_token == "manual_refresh_token"
        assert auth.expires_at > time.time()  # Should be set to future time
    
    def test_token_error_response(self):
        """Test handling error responses from token endpoints."""
        auth = OAuthAuth(
            client_id="test_id",
            client_secret="test_secret"
        )
        
        with requests_mock.Mocker() as m:
            m.post(
                "https://api.hostex.io/v3/oauth/authorizations",
                json={
                    "request_id": "req_123",
                    "error_code": 400,
                    "error_msg": "Invalid authorization code"
                }
            )
            
            with pytest.raises(AuthenticationError) as exc_info:
                auth.get_access_token("invalid_code")
            
            assert exc_info.value.error_code == 400
            assert "Invalid authorization code" in str(exc_info.value)