"""
Properties endpoint implementation.
"""

from typing import Dict, Any, Optional

from .base import BaseEndpoint


class PropertiesEndpoint(BaseEndpoint):
    """Properties API endpoint."""
    
    def list(
        self,
        offset: int = 0,
        limit: int = 20,
        id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Query properties.
        
        Args:
            offset: Starting point for results (default: 0)
            limit: Maximum number of results (max: 100, default: 20)
            id: Filter by specific property ID
        
        Returns:
            API response with properties data
        """
        if limit > 100:
            raise ValueError("Limit cannot exceed 100")
        
        params = {
            "offset": offset,
            "limit": limit,
        }
        
        if id is not None:
            params["id"] = id
        
        return self._get("properties", params=params)