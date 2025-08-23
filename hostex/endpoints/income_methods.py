"""
Income Methods endpoint implementation.
"""

from typing import Dict, Any

from .base import BaseEndpoint


class IncomeMethodsEndpoint(BaseEndpoint):
    """Income Methods API endpoint."""
    
    def list(self) -> Dict[str, Any]:
        """
        Query income methods created from the Custom Options Page.
        
        Returns:
            API response with income methods data
        """
        return self._get("income_methods")