"""
Tests for custom exception classes.
"""

import pytest
from hostex.exceptions import (
    HostexError,
    HostexAPIError,
    AuthenticationError,
    ValidationError,
    NotFoundError,
    PermissionError,
    MethodNotAllowedError,
    UserAccountError,
    RateLimitError,
    ServerError,
    ConnectionError,
    TimeoutError,
    InvalidConfigError,
)


class TestBaseExceptions:
    """Test base exception classes."""
    
    def test_hostex_error(self):
        """Test base HostexError exception."""
        error = HostexError("Base error message")
        assert str(error) == "Base error message"
        assert error.message == "Base error message"
    
    def test_hostex_api_error(self):
        """Test HostexAPIError exception."""
        error = HostexAPIError(
            message="API error",
            error_code=400,
            request_id="req_123",
            response_data={"test": "data"}
        )
        
        assert error.error_code == 400
        assert error.request_id == "req_123"
        assert error.response_data == {"test": "data"}
        assert str(error) == "Hostex API Error 400: API error"
    
    def test_hostex_api_error_minimal(self):
        """Test HostexAPIError with minimal parameters."""
        error = HostexAPIError("Simple error", 500)
        assert error.error_code == 500
        assert error.request_id is None
        assert error.response_data == {}


class TestSpecificExceptions:
    """Test specific exception classes."""
    
    def test_authentication_error(self):
        """Test AuthenticationError."""
        error = AuthenticationError()
        assert error.error_code == 401
        assert "Authentication failed" in str(error)
        
        # With custom message
        error = AuthenticationError("Invalid token")
        assert "Invalid token" in str(error)
    
    def test_validation_error(self):
        """Test ValidationError."""
        error = ValidationError()
        assert error.error_code == 400
        assert "Request validation failed" in str(error)
        
        # With custom message
        error = ValidationError("Missing required field")
        assert "Missing required field" in str(error)
    
    def test_not_found_error(self):
        """Test NotFoundError."""
        error = NotFoundError()
        assert error.error_code == 404
        assert "Resource not found" in str(error)
    
    def test_permission_error(self):
        """Test PermissionError."""
        error = PermissionError()
        assert error.error_code == 403
        assert "Access forbidden" in str(error)
    
    def test_method_not_allowed_error(self):
        """Test MethodNotAllowedError."""
        error = MethodNotAllowedError()
        assert error.error_code == 405
        assert "Method not allowed" in str(error)
    
    def test_user_account_error(self):
        """Test UserAccountError.""" 
        error = UserAccountError()
        assert error.error_code == 420
        assert "User account issue" in str(error)
    
    def test_rate_limit_error(self):
        """Test RateLimitError."""
        error = RateLimitError()
        assert error.error_code == 429
        assert "Rate limit exceeded" in str(error)
        assert error.retry_after is None
        
        # With retry_after
        error = RateLimitError("Rate limited", retry_after=60)
        assert error.retry_after == 60
        assert "retry after 60 seconds" in str(error)
    
    def test_server_error(self):
        """Test ServerError."""
        error = ServerError()
        assert error.error_code == 500
        assert "Internal server error" in str(error)
        
        # With custom error code
        error = ServerError("Service unavailable", error_code=503)
        assert error.error_code == 503


class TestUtilityExceptions:
    """Test utility exception classes."""
    
    def test_connection_error(self):
        """Test ConnectionError."""
        error = ConnectionError("Connection failed")
        assert str(error) == "Connection failed"
        assert isinstance(error, HostexError)
    
    def test_timeout_error(self):
        """Test TimeoutError."""
        error = TimeoutError("Request timeout")
        assert str(error) == "Request timeout"
        assert isinstance(error, HostexError)
    
    def test_invalid_config_error(self):
        """Test InvalidConfigError."""
        error = InvalidConfigError("Invalid configuration")
        assert str(error) == "Invalid configuration"
        assert isinstance(error, HostexError)


class TestExceptionInheritance:
    """Test exception inheritance hierarchy."""
    
    def test_inheritance_hierarchy(self):
        """Test that exceptions inherit from correct base classes."""
        # All API errors should inherit from HostexAPIError
        api_exceptions = [
            AuthenticationError,
            ValidationError,
            NotFoundError,
            PermissionError,
            MethodNotAllowedError,
            UserAccountError,
            RateLimitError,
            ServerError,
        ]
        
        for exc_class in api_exceptions:
            error = exc_class()
            assert isinstance(error, HostexAPIError)
            assert isinstance(error, HostexError)
            assert isinstance(error, Exception)
        
        # Utility exceptions should inherit from HostexError directly
        utility_exceptions = [ConnectionError, TimeoutError, InvalidConfigError]
        
        for exc_class in utility_exceptions:
            error = exc_class("test message")
            assert isinstance(error, HostexError)
            assert isinstance(error, Exception)
            assert not isinstance(error, HostexAPIError)
    
    def test_exception_with_kwargs(self):
        """Test exceptions with additional kwargs."""
        error = ValidationError(
            "Validation failed",
            request_id="req_456",
            response_data={"field": "value"}
        )
        
        assert error.request_id == "req_456"
        assert error.response_data == {"field": "value"}
        assert error.error_code == 400