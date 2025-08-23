"""
Custom Channels endpoint implementation.
"""

from typing import Dict, Any

from .base import BaseEndpoint


class CustomChannelsEndpoint(BaseEndpoint):
    """Custom Channels API endpoint."""
    
    def list(self) -> Dict[str, Any]:
        """
        Query custom channels created from the Custom Options Page.
        
        Returns:
            API response with custom channels data
        """
        return self._get("custom_channels")