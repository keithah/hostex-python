"""
Main Hostex API client.
"""

import time
from typing import Optional, Dict, Any, Union
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from .auth import BaseAuth, TokenAuth, OAuthAuth
from .exceptions import (
    HostexAPIError,
    AuthenticationError,
    ValidationError,
    NotFoundError,
    PermissionError,
    MethodNotAllowedError,
    UserAccountError,
    RateLimitError,
    ServerError,
    ConnectionError,
    TimeoutError,
    InvalidConfigError,
)
from .endpoints import (
    PropertiesEndpoint,
    RoomTypesEndpoint,
    ReservationsEndpoint,
    AvailabilitiesEndpoint,
    ListingsEndpoint,
    ConversationsEndpoint,
    ReviewsEndpoint,
    WebhooksEndpoint,
    CustomChannelsEndpoint,
    IncomeMethodsEndpoint,
)


class HostexClient:
    """Main Hostex API client."""
    
    def __init__(
        self,
        access_token: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        base_url: str = "https://api.hostex.io/v3",
        timeout: int = 30,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
        user_agent: str = "hostex-python/1.0.0",
    ) -> None:
        """
        Initialize the Hostex API client.
        
        Args:
            access_token: API access token for token-based auth
            client_id: OAuth client ID 
            client_secret: OAuth client secret
            redirect_uri: OAuth redirect URI
            base_url: API base URL
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
            backoff_factor: Backoff factor for retries
            user_agent: User agent string
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.user_agent = user_agent
        
        # Initialize authentication
        if access_token:
            self.auth = TokenAuth(access_token)
        elif client_id and client_secret:
            self.auth = OAuthAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                base_url=base_url,
            )
        else:
            raise InvalidConfigError(
                "Either access_token or (client_id and client_secret) must be provided"
            )
        
        # Set up HTTP session with retries
        self.session = requests.Session()
        
        # Configure retries
        retry_strategy = Retry(
            total=max_retries,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"],
            backoff_factor=backoff_factor,
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Initialize endpoints
        self.properties = PropertiesEndpoint(self)
        self.room_types = RoomTypesEndpoint(self)
        self.reservations = ReservationsEndpoint(self)
        self.availabilities = AvailabilitiesEndpoint(self)
        self.listings = ListingsEndpoint(self)
        self.conversations = ConversationsEndpoint(self)
        self.reviews = ReviewsEndpoint(self)
        self.webhooks = WebhooksEndpoint(self)
        self.custom_channels = CustomChannelsEndpoint(self)
        self.income_methods = IncomeMethodsEndpoint(self)
        
        # OAuth-specific properties
        if isinstance(self.auth, OAuthAuth):
            self.oauth = self.auth
    
    def set_access_token(self, access_token: str) -> None:
        """Set or update the access token."""
        if isinstance(self.auth, TokenAuth):
            self.auth.access_token = access_token
        elif isinstance(self.auth, OAuthAuth):
            self.auth.access_token = access_token
        else:
            raise InvalidConfigError("Cannot set access token for current auth type")
    
    def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        retries: int = 0,
        max_retries: int = 3,
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the Hostex API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (without base URL)
            params: Query parameters
            data: Form data
            json: JSON data
            headers: Additional headers
            timeout: Request timeout (uses default if not provided)
            retries: Current retry count (internal use)
            max_retries: Maximum retries for this request
        
        Returns:
            Parsed JSON response
        
        Raises:
            Various HostexAPIError subclasses based on response
        """
        url = urljoin(self.base_url + "/", endpoint.lstrip("/"))
        
        # Build headers
        request_headers = {
            "User-Agent": self.user_agent,
            "Content-Type": "application/json",
        }
        
        # Add authentication headers
        try:
            auth_headers = self.auth.get_headers()
            request_headers.update(auth_headers)
        except Exception as e:
            raise AuthenticationError(f"Authentication failed: {e}")
        
        # Add custom headers
        if headers:
            request_headers.update(headers)
        
        request_timeout = timeout or self.timeout
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                json=json,
                headers=request_headers,
                timeout=request_timeout,
            )
            
            # Parse response
            try:
                result = response.json()
            except ValueError:
                # Non-JSON response
                result = {"error_msg": response.text, "error_code": response.status_code}
            
            # Handle successful responses
            if response.status_code == 200 and result.get("error_code") == 200:
                return result
            
            # Handle API errors
            error_code = result.get("error_code", response.status_code)
            error_msg = result.get("error_msg", "Unknown error")
            request_id = result.get("request_id")
            
            # Create appropriate exception
            exception_class = self._get_exception_class(error_code)
            
            if error_code == 429:
                # Rate limit - extract retry-after if available
                retry_after = response.headers.get("Retry-After")
                if retry_after:
                    try:
                        retry_after = int(retry_after)
                    except ValueError:
                        retry_after = None
                
                # Retry with exponential backoff
                if retries < max_retries:
                    wait_time = retry_after or (2 ** retries)
                    time.sleep(wait_time)
                    return self.request(
                        method, endpoint, params, data, json, headers,
                        timeout, retries + 1, max_retries
                    )
                
                raise RateLimitError(
                    error_msg,
                    retry_after=retry_after,
                    request_id=request_id,
                    response_data=result,
                )
            
            raise exception_class(
                error_msg,
                error_code=error_code,
                request_id=request_id,
                response_data=result,
            )
            
        except requests.exceptions.Timeout:
            raise TimeoutError(f"Request timed out after {request_timeout} seconds")
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(f"Connection error: {e}")
        except requests.exceptions.RequestException as e:
            raise HostexAPIError(f"Request failed: {e}", error_code=0)
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """Make a GET request."""
        return self.request("GET", endpoint, params=params, **kwargs)
    
    def post(self, endpoint: str, json: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """Make a POST request."""
        return self.request("POST", endpoint, json=json, **kwargs)
    
    def patch(self, endpoint: str, json: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """Make a PATCH request."""
        return self.request("PATCH", endpoint, json=json, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make a DELETE request."""
        return self.request("DELETE", endpoint, **kwargs)
    
    @staticmethod
    def _get_exception_class(error_code: int) -> type:
        """Get appropriate exception class for error code."""
        error_map = {
            400: ValidationError,
            401: AuthenticationError,
            403: PermissionError,
            404: NotFoundError,
            405: MethodNotAllowedError,
            420: UserAccountError,
            429: RateLimitError,
        }
        
        if error_code in error_map:
            return error_map[error_code]
        elif 500 <= error_code < 600:
            return ServerError
        else:
            return HostexAPIError