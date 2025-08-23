"""
Reviews endpoint implementation.
"""

from typing import Dict, Any, Optional

from .base import BaseEndpoint


class ReviewsEndpoint(BaseEndpoint):
    """Reviews API endpoint."""
    
    def list(
        self,
        reservation_code: Optional[str] = None,
        property_id: Optional[int] = None,
        review_status: str = "reviewed",
        start_check_out_date: Optional[str] = None,
        end_check_out_date: Optional[str] = None,
        offset: int = 0,
        limit: int = 20,
    ) -> Dict[str, Any]:
        """
        Query reviews like the Reviews Page.
        
        Args:
            reservation_code: Filter by reservation code
            property_id: Filter by property ID
            review_status: Filter by review status (default: 'reviewed')
            start_check_out_date: Check-out date range start (default: 180 days ago)
            end_check_out_date: Check-out date range end (default: today)
            offset: Starting index (default: 0)
            limit: Maximum results (max: 100, default: 20)
        
        Returns:
            API response with reviews data
        """
        if limit > 100:
            raise ValueError("Limit cannot exceed 100")
        
        # Validate dates if provided
        if start_check_out_date or end_check_out_date:
            import re
            date_pattern = r'^\d{4}-\d{2}-\d{2}$'
            if start_check_out_date and not re.match(date_pattern, start_check_out_date):
                raise ValueError("start_check_out_date must be in YYYY-MM-DD format")
            if end_check_out_date and not re.match(date_pattern, end_check_out_date):
                raise ValueError("end_check_out_date must be in YYYY-MM-DD format")
        
        params = {
            "review_status": review_status,
            "offset": offset,
            "limit": limit,
        }
        
        # Add optional filters
        if reservation_code:
            params["reservation_code"] = reservation_code
        if property_id is not None:
            params["property_id"] = property_id
        if start_check_out_date:
            params["start_check_out_date"] = start_check_out_date
        if end_check_out_date:
            params["end_check_out_date"] = end_check_out_date
        
        return self._get("reviews", params=params)
    
    def create(
        self,
        reservation_code: str,
        host_review_score: Optional[float] = None,
        host_review_content: Optional[str] = None,
        host_reply_content: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create review or reply for a reservation.
        
        Args:
            reservation_code: The reservation code
            host_review_score: Rating score (0-5)
            host_review_content: Review comment from host
            host_reply_content: Host reply to guest review
        
        Returns:
            API response confirming submission
        """
        if not any([host_review_score is not None, host_review_content, host_reply_content]):
            raise ValueError("At least one of host_review_score, host_review_content, or host_reply_content must be provided")
        
        # Validate score range
        if host_review_score is not None:
            if not (0 <= host_review_score <= 5):
                raise ValueError("host_review_score must be between 0 and 5")
        
        data = {}
        if host_review_score is not None:
            data["host_review_score"] = host_review_score
        if host_review_content:
            data["host_review_content"] = host_review_content
        if host_reply_content:
            data["host_reply_content"] = host_reply_content
        
        return self._post(f"reviews/{reservation_code}", json=data)