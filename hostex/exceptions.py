"""
Custom exceptions for the Hostex API client.
"""

from typing import Optional, Dict, Any


class HostexError(Exception):
    """Base exception class for all Hostex-related errors."""
    
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class HostexAPIError(HostexError):
    """Raised when the Hostex API returns an error response."""
    
    def __init__(
        self, 
        message: str, 
        error_code: int, 
        request_id: Optional[str] = None,
        response_data: Optional[Dict[str, Any]] = None
    ) -> None:
        self.error_code = error_code
        self.request_id = request_id
        self.response_data = response_data or {}
        super().__init__(message)
    
    def __str__(self) -> str:
        return f"Hostex API Error {self.error_code}: {self.message}"


class AuthenticationError(HostexAPIError):
    """Raised when authentication fails (401 errors)."""
    
    def __init__(self, message: str = "Authentication failed", **kwargs) -> None:
        super().__init__(message, error_code=401, **kwargs)


class ValidationError(HostexAPIError):
    """Raised when request validation fails (400 errors)."""
    
    def __init__(self, message: str = "Request validation failed", **kwargs) -> None:
        super().__init__(message, error_code=400, **kwargs)


class NotFoundError(HostexAPIError):
    """Raised when a resource is not found (404 errors)."""
    
    def __init__(self, message: str = "Resource not found", **kwargs) -> None:
        super().__init__(message, error_code=404, **kwargs)


class PermissionError(HostexAPIError):
    """Raised when access is forbidden (403 errors)."""
    
    def __init__(self, message: str = "Access forbidden", **kwargs) -> None:
        super().__init__(message, error_code=403, **kwargs)


class MethodNotAllowedError(HostexAPIError):
    """Raised when HTTP method is not allowed (405 errors)."""
    
    def __init__(self, message: str = "Method not allowed", **kwargs) -> None:
        super().__init__(message, error_code=405, **kwargs)


class UserAccountError(HostexAPIError):
    """Raised when there's a user account issue (420 errors)."""
    
    def __init__(self, message: str = "User account issue", **kwargs) -> None:
        super().__init__(message, error_code=420, **kwargs)


class RateLimitError(HostexAPIError):
    """Raised when rate limit is exceeded (429 errors)."""
    
    def __init__(
        self, 
        message: str = "Rate limit exceeded", 
        retry_after: Optional[int] = None,
        **kwargs
    ) -> None:
        self.retry_after = retry_after
        super().__init__(message, error_code=429, **kwargs)
    
    def __str__(self) -> str:
        base_msg = super().__str__()
        if self.retry_after:
            return f"{base_msg} (retry after {self.retry_after} seconds)"
        return base_msg


class ServerError(HostexAPIError):
    """Raised when the server encounters an error (5xx errors)."""
    
    def __init__(
        self, 
        message: str = "Internal server error", 
        error_code: int = 500,
        **kwargs
    ) -> None:
        super().__init__(message, error_code=error_code, **kwargs)


class ConnectionError(HostexError):
    """Raised when there are connection issues with the API."""
    pass


class TimeoutError(HostexError):
    """Raised when requests timeout."""
    pass


class InvalidConfigError(HostexError):
    """Raised when client configuration is invalid."""
    pass