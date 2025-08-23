"""
Webhooks endpoint implementation.
"""

from typing import Dict, Any

from .base import BaseEndpoint


class WebhooksEndpoint(BaseEndpoint):
    """Webhooks API endpoint."""
    
    def list(self) -> Dict[str, Any]:
        """
        Query webhooks like the Webhooks Page.
        
        Returns:
            API response with webhooks data
        """
        return self._get("webhooks")
    
    def create(self, url: str) -> Dict[str, Any]:
        """
        Create a webhook.
        
        Args:
            url: The webhook URL endpoint
        
        Returns:
            API response confirming creation
        """
        if not url:
            raise ValueError("URL is required")
        
        # Basic URL validation
        if not (url.startswith("http://") or url.startswith("https://")):
            raise ValueError("URL must start with http:// or https://")
        
        data = {"url": url}
        return self._post("webhooks", json=data)
    
    def delete(self, webhook_id: int) -> Dict[str, Any]:
        """
        Delete a webhook.
        
        Note: You can only delete webhooks created by your own app if they are 
        manageable. Attempting to delete non-manageable webhooks from other apps 
        will result in a 403 error.
        
        Args:
            webhook_id: The webhook ID to delete
        
        Returns:
            API response confirming deletion
        """
        return self._delete(f"webhooks/{webhook_id}")