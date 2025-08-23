"""
Hostex Python API Client

A Python client library for the Hostex API v3.0.0 (Beta).
Provides comprehensive access to property management, reservations,
availability, messaging, reviews, and more.
"""

from .client import HostexClient
from .exceptions import (
    HostexError,
    HostexAPIError,
    AuthenticationError,
    ValidationError,
    NotFoundError,
    RateLimitError,
    ServerError,
)

__version__ = "1.0.0"
__author__ = "Keith"
__email__ = "keith@example.com"

__all__ = [
    "HostexClient",
    "HostexError",
    "HostexAPIError", 
    "AuthenticationError",
    "ValidationError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
]