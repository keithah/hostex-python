"""
Conversations endpoint implementation.
"""

from typing import Dict, Any, Optional

from .base import BaseEndpoint


class ConversationsEndpoint(BaseEndpoint):
    """Conversations API endpoint."""
    
    def list(
        self,
        offset: int = 0,
        limit: int = 20,
    ) -> Dict[str, Any]:
        """
        Query conversations regarding guest inquiries.
        
        Args:
            offset: Starting index (default: 0)
            limit: Maximum results (max: 100, default: 20)
        
        Returns:
            API response with conversations data
        """
        if limit > 100:
            raise ValueError("Limit cannot exceed 100")
        
        params = {
            "offset": offset,
            "limit": limit,
        }
        
        return self._get("conversations", params=params)
    
    def get(self, conversation_id: str) -> Dict[str, Any]:
        """
        Get conversation details including messages.
        
        Args:
            conversation_id: The conversation ID
        
        Returns:
            API response with conversation details and messages
        """
        return self._get(f"conversations/{conversation_id}")
    
    def send_message(
        self,
        conversation_id: str,
        message: Optional[str] = None,
        jpeg_base64: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Send a text or image message to a guest.
        
        Args:
            conversation_id: The conversation ID
            message: Text content of the message
            jpeg_base64: Base64 encoded JPEG image
        
        Returns:
            API response confirming message sent
        """
        if not message and not jpeg_base64:
            raise ValueError("Either message text or jpeg_base64 image must be provided")
        
        data = {}
        if message:
            data["message"] = message
        if jpeg_base64:
            data["jpeg_base64"] = jpeg_base64
        
        return self._post(f"conversations/{conversation_id}", json=data)