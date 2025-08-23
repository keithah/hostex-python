"""
Base endpoint class.
"""

from typing import TYPE_CHECKING, Dict, Any, Optional

if TYPE_CHECKING:
    from ..client import HostexClient


class BaseEndpoint:
    """Base class for API endpoints."""
    
    def __init__(self, client: "HostexClient") -> None:
        self.client = client
    
    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request."""
        return self.client.get(endpoint, params=params)
    
    def _post(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a POST request."""
        return self.client.post(endpoint, json=json)
    
    def _patch(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a PATCH request."""
        return self.client.patch(endpoint, json=json)
    
    def _delete(self, endpoint: str) -> Dict[str, Any]:
        """Make a DELETE request."""
        return self.client.delete(endpoint)