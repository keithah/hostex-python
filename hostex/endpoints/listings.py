"""
Listings endpoint implementation.
"""

from typing import Dict, Any, List

from .base import BaseEndpoint


class ListingsEndpoint(BaseEndpoint):
    """Listings API endpoint."""
    
    def get_calendar(
        self,
        start_date: str,
        end_date: str,
        listings: List[Dict[str, str]],
    ) -> Dict[str, Any]:
        """
        Query listing calendars for multiple listings.
        
        Args:
            start_date: Start date (YYYY-MM-DD, within 1 year from now)
            end_date: End date (YYYY-MM-DD, within 3 years from now)
            listings: List of listing objects with 'channel_type' and 'listing_id'
        
        Returns:
            API response with calendar data
        """
        # Validate date format (basic check)
        import re
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(date_pattern, start_date):
            raise ValueError("start_date must be in YYYY-MM-DD format")
        if not re.match(date_pattern, end_date):
            raise ValueError("end_date must be in YYYY-MM-DD format")
        
        # Validate listings format
        if not listings or not isinstance(listings, list):
            raise ValueError("listings must be a non-empty list")
        
        for listing in listings:
            if not isinstance(listing, dict):
                raise ValueError("Each listing must be a dictionary")
            if "channel_type" not in listing or "listing_id" not in listing:
                raise ValueError("Each listing must have 'channel_type' and 'listing_id'")
        
        data = {
            "start_date": start_date,
            "end_date": end_date,
            "listings": listings,
        }
        
        return self._post("listings/calendar", json=data)
    
    def update_inventories(
        self,
        channel_type: str,
        listing_id: str,
        inventories: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Update inventories of channel listings.
        
        Note: A successful response indicates that an asynchronous task has been 
        initiated; it does NOT ensure that channel inventories have been modified 
        successfully. This endpoint only modifies listing inventory and does NOT 
        affect property availability.
        
        Args:
            channel_type: The channel type (e.g., 'airbnb', 'booking.com')
            listing_id: The channel listing ID
            inventories: List of inventory update objects
        
        Returns:
            API response confirming submission
        """
        if not inventories or not isinstance(inventories, list):
            raise ValueError("inventories must be a non-empty list")
        
        data = {
            "channel_type": channel_type,
            "listing_id": listing_id,
            "inventories": inventories,
        }
        
        return self._post("listings/inventories", json=data)
    
    def update_prices(
        self,
        channel_type: str,
        listing_id: str,
        prices: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Update prices of channel listings.
        
        Note: A successful response indicates that an asynchronous task has been 
        initiated; it does NOT ensure that channel prices have been modified 
        successfully.
        
        Args:
            channel_type: The channel type (e.g., 'airbnb', 'booking.com')
            listing_id: The channel listing ID
            prices: List of price update objects
        
        Returns:
            API response confirming submission
        """
        if not prices or not isinstance(prices, list):
            raise ValueError("prices must be a non-empty list")
        
        data = {
            "channel_type": channel_type,
            "listing_id": listing_id,
            "prices": prices,
        }
        
        return self._post("listings/prices", json=data)
    
    def update_restrictions(
        self,
        channel_type: str,
        listing_id: str,
        restrictions: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Update restrictions of channel listings.
        
        Note: A successful response indicates that an asynchronous task has been 
        initiated; it does NOT ensure that channel restrictions have been modified 
        successfully.
        
        Args:
            channel_type: The channel type (e.g., 'airbnb', 'booking.com')
            listing_id: The channel listing ID
            restrictions: List of restriction update objects
        
        Returns:
            API response confirming submission
        """
        if not restrictions or not isinstance(restrictions, list):
            raise ValueError("restrictions must be a non-empty list")
        
        data = {
            "channel_type": channel_type,
            "listing_id": listing_id,
            "restrictions": restrictions,
        }
        
        return self._post("listings/restrictions", json=data)