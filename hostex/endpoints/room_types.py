"""
Room Types endpoint implementation.
"""

from typing import Dict, Any

from .base import BaseEndpoint


class RoomTypesEndpoint(BaseEndpoint):
    """Room Types API endpoint."""
    
    def list(
        self,
        offset: int = 0,
        limit: int = 20,
    ) -> Dict[str, Any]:
        """
        Query room types.
        
        Args:
            offset: Starting point for results (default: 0)
            limit: Maximum number of results (max: 100, default: 20)
        
        Returns:
            API response with room types data
        """
        if limit > 100:
            raise ValueError("Limit cannot exceed 100")
        
        params = {
            "offset": offset,
            "limit": limit,
        }
        
        return self._get("room_types", params=params)