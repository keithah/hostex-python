"""
Availabilities endpoint implementation.
"""

from typing import Dict, Any, List, Union, Optional

from .base import BaseEndpoint


class AvailabilitiesEndpoint(BaseEndpoint):
    """Availabilities API endpoint."""
    
    def list(
        self,
        property_ids: str,
        start_date: str,
        end_date: str,
    ) -> Dict[str, Any]:
        """
        Query property availabilities.
        
        Args:
            property_ids: Comma-separated property IDs (max 100)
            start_date: Start date (YYYY-MM-DD, within 1 year from now)
            end_date: End date (YYYY-MM-DD, within 3 years from now)
        
        Returns:
            API response with availabilities data
        """
        # Validate date format (basic check)
        import re
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(date_pattern, start_date):
            raise ValueError("start_date must be in YYYY-MM-DD format")
        if not re.match(date_pattern, end_date):
            raise ValueError("end_date must be in YYYY-MM-DD format")
        
        # Validate property_ids count
        property_id_list = [pid.strip() for pid in property_ids.split(",") if pid.strip()]
        if len(property_id_list) > 100:
            raise ValueError("Cannot query more than 100 properties at once")
        
        params = {
            "property_ids": property_ids,
            "start_date": start_date,
            "end_date": end_date,
        }
        
        return self._get("availabilities", params=params)
    
    def update(
        self,
        property_ids: List[int],
        available: bool,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        dates: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Update property availabilities.
        
        Note: A successful response indicates that an asynchronous task has been 
        initiated to handle the submission; it does NOT ensure that channel 
        inventories have been modified successfully.
        
        Args:
            property_ids: List of property IDs to update
            available: Availability status (True for available, False for unavailable)
            start_date: Update start date (YYYY-MM-DD). If omitted, dates becomes mandatory.
            end_date: Update end date (YYYY-MM-DD). If omitted, dates becomes mandatory.
            dates: List of specific dates (YYYY-MM-DD). If start_date and end_date 
                   are specified, this will be ignored.
        
        Returns:
            API response confirming submission
        """
        if not start_date and not end_date and not dates:
            raise ValueError("Either (start_date and end_date) or dates must be provided")
        
        if start_date and end_date and dates:
            # API docs state that dates will be ignored if start/end dates are provided
            pass
        
        # Validate date formats
        import re
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        
        if start_date and not re.match(date_pattern, start_date):
            raise ValueError("start_date must be in YYYY-MM-DD format")
        if end_date and not re.match(date_pattern, end_date):
            raise ValueError("end_date must be in YYYY-MM-DD format")
        
        if dates:
            for date in dates:
                if not re.match(date_pattern, date):
                    raise ValueError(f"Date '{date}' must be in YYYY-MM-DD format")
        
        data = {
            "property_ids": property_ids,
            "available": available,
        }
        
        if start_date:
            data["start_date"] = start_date
        if end_date:
            data["end_date"] = end_date
        if dates:
            data["dates"] = dates
        
        return self._post("availabilities", json=data)