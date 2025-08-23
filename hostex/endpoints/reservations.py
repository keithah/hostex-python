"""
Reservations endpoint implementation.
"""

from typing import Dict, Any, Optional, List, Union

from .base import BaseEndpoint


class ReservationsEndpoint(BaseEndpoint):
    """Reservations API endpoint."""
    
    def list(
        self,
        reservation_code: Optional[str] = None,
        property_id: Optional[int] = None,
        status: Optional[str] = None,
        start_check_in_date: Optional[str] = None,
        end_check_in_date: Optional[str] = None,
        start_check_out_date: Optional[str] = None,
        end_check_out_date: Optional[str] = None,
        order_by: str = "booked_at",
        offset: int = 0,
        limit: int = 20,
    ) -> Dict[str, Any]:
        """
        Query reservations.
        
        Args:
            reservation_code: Filter by reservation code
            property_id: Filter by property ID
            status: Filter by reservation status (wait_accept, wait_pay, accepted, cancelled, denied, timeout)
            start_check_in_date: Check-in date range start (YYYY-MM-DD)
            end_check_in_date: Check-in date range end (YYYY-MM-DD)
            start_check_out_date: Check-out date range start (YYYY-MM-DD)
            end_check_out_date: Check-out date range end (YYYY-MM-DD)
            order_by: Sort field (default: booked_at)
            offset: Starting index (default: 0)
            limit: Maximum results (max: 100, default: 20)
        
        Returns:
            API response with reservations data
        """
        if limit > 100:
            raise ValueError("Limit cannot exceed 100")
        
        valid_statuses = ["wait_accept", "wait_pay", "accepted", "cancelled", "denied", "timeout"]
        if status and status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        
        params = {
            "order_by": order_by,
            "offset": offset,
            "limit": limit,
        }
        
        # Add optional filters
        if reservation_code:
            params["reservation_code"] = reservation_code
        if property_id is not None:
            params["property_id"] = property_id
        if status:
            params["status"] = status
        if start_check_in_date:
            params["start_check_in_date"] = start_check_in_date
        if end_check_in_date:
            params["end_check_in_date"] = end_check_in_date
        if start_check_out_date:
            params["start_check_out_date"] = start_check_out_date
        if end_check_out_date:
            params["end_check_out_date"] = end_check_out_date
        
        return self._get("reservations", params=params)
    
    def create(
        self,
        property_id: str,
        custom_channel_id: int,
        check_in_date: str,
        check_out_date: str,
        guest_name: str,
        currency: str,
        rate_amount: int,
        commission_amount: int,
        received_amount: int,
        income_method_id: int,
        number_of_guests: Optional[int] = None,
        email: Optional[str] = None,
        mobile: Optional[str] = None,
        remarks: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a direct booking reservation.
        
        Args:
            property_id: Property ID for the reservation
            custom_channel_id: Custom channel ID
            check_in_date: Check-in date (YYYY-MM-DD)
            check_out_date: Check-out date (YYYY-MM-DD)
            guest_name: Primary guest name
            currency: Currency code (e.g., 'USD')
            rate_amount: Total rate amount (in cents/smallest unit)
            commission_amount: Commission amount (in cents/smallest unit)
            received_amount: Total received amount (in cents/smallest unit)
            income_method_id: Income method identifier
            number_of_guests: Total number of guests
            email: Primary guest email
            mobile: Primary guest mobile phone
            remarks: Additional remarks
        
        Returns:
            API response with created reservation data
        """
        # Validate dates format (basic check)
        import re
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(date_pattern, check_in_date):
            raise ValueError("check_in_date must be in YYYY-MM-DD format")
        if not re.match(date_pattern, check_out_date):
            raise ValueError("check_out_date must be in YYYY-MM-DD format")
        
        data = {
            "property_id": property_id,
            "custom_channel_id": custom_channel_id,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "guest_name": guest_name,
            "currency": currency,
            "rate_amount": rate_amount,
            "commission_amount": commission_amount,
            "received_amount": received_amount,
            "income_method_id": income_method_id,
        }
        
        # Add optional fields
        if number_of_guests is not None:
            data["number_of_guests"] = number_of_guests
        if email:
            data["email"] = email
        if mobile:
            data["mobile"] = mobile
        if remarks:
            data["remarks"] = remarks
        
        return self._post("reservations", json=data)
    
    def cancel(self, reservation_code: str) -> Dict[str, Any]:
        """
        Cancel a direct booking reservation.
        
        Note: This endpoint does not support cancellation of channel bookings.
        
        Args:
            reservation_code: The reservation code to cancel
        
        Returns:
            API response confirming cancellation
        """
        return self._delete(f"reservations/{reservation_code}")
    
    def update_lock_code(self, stay_code: str, lock_code: str) -> Dict[str, Any]:
        """
        Update lock code for a stay.
        
        Args:
            stay_code: The stay code
            lock_code: New lock code
        
        Returns:
            API response confirming update
        """
        data = {"lock_code": lock_code}
        return self._patch(f"reservations/{stay_code}/check_in_details", json=data)
    
    def get_custom_fields(self, stay_code: str) -> Dict[str, Any]:
        """
        Get custom fields for a stay.
        
        Args:
            stay_code: The stay code
        
        Returns:
            API response with custom fields data
        """
        return self._get(f"reservations/{stay_code}/custom_fields")
    
    def update_custom_fields(
        self, 
        stay_code: str, 
        custom_fields: Dict[str, Optional[str]]
    ) -> Dict[str, Any]:
        """
        Update custom fields for a stay.
        
        Args:
            stay_code: The stay code
            custom_fields: Custom fields dict. Set field to None to delete it.
        
        Returns:
            API response with updated custom fields
        """
        data = {"custom_fields": custom_fields}
        return self._patch(f"reservations/{stay_code}/custom_fields", json=data)