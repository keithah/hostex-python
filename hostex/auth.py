"""
Authentication handlers for the Hostex API client.
"""

import time
from typing import Optional, Dict, Any
from urllib.parse import urlencode

import requests

from .exceptions import (
    AuthenticationError,
    ValidationError,
    InvalidConfigError,
    HostexAPIError,
)


class BaseAuth:
    """Base authentication class."""
    
    def get_headers(self) -> Dict[str, str]:
        """Return headers required for authentication."""
        raise NotImplementedError


class TokenAuth(BaseAuth):
    """API token authentication."""
    
    def __init__(self, access_token: str) -> None:
        if not access_token:
            raise InvalidConfigError("Access token is required")
        self.access_token = access_token
    
    def get_headers(self) -> Dict[str, str]:
        """Return headers with API token."""
        return {
            "Hostex-Access-Token": self.access_token,
        }


class OAuthAuth(BaseAuth):
    """OAuth 2.0 authentication handler."""
    
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: Optional[str] = None,
        access_token: Optional[str] = None,
        refresh_token: Optional[str] = None,
        expires_at: Optional[float] = None,
        base_url: str = "https://api.hostex.io/v3",
    ) -> None:
        if not client_id or not client_secret:
            raise InvalidConfigError("Client ID and client secret are required")
        
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_at = expires_at
        self.base_url = base_url.rstrip("/")
    
    def get_headers(self) -> Dict[str, str]:
        """Return headers with access token if available."""
        if not self.access_token:
            raise AuthenticationError("No access token available. Please authenticate first.")
        
        # Check if token is expired and refresh if needed
        if self.is_token_expired() and self.refresh_token:
            try:
                self.refresh_access_token()
            except Exception as e:
                raise AuthenticationError(f"Failed to refresh access token: {e}")
        
        return {
            "Hostex-Access-Token": self.access_token,
        }
    
    def is_token_expired(self) -> bool:
        """Check if the access token is expired."""
        if not self.expires_at:
            return False
        
        # Add 60 second buffer to refresh before expiration
        return time.time() >= (self.expires_at - 60)
    
    def get_authorization_url(
        self, 
        state: Optional[str] = None,
        authorization_base_url: str = "https://hostex.io/app/authorization"
    ) -> str:
        """Generate the authorization URL for OAuth flow."""
        if not self.redirect_uri:
            raise InvalidConfigError("Redirect URI is required for authorization URL")
        
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
        }
        
        if state:
            params["state"] = state
        
        return f"{authorization_base_url}?{urlencode(params)}"
    
    def get_access_token(self, authorization_code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token."""
        return self._request_token({
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "authorization_code",
            "code": authorization_code,
        })
    
    def refresh_access_token(self) -> Dict[str, Any]:
        """Refresh the access token using refresh token."""
        if not self.refresh_token:
            raise AuthenticationError("No refresh token available")
        
        token_data = self._request_token({
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
        })
        
        # Update instance variables
        self.access_token = token_data["access_token"]
        if "refresh_token" in token_data:
            self.refresh_token = token_data["refresh_token"]
        if "expires_in" in token_data:
            self.expires_at = time.time() + token_data["expires_in"]
        
        return token_data
    
    def revoke_token(self, token: Optional[str] = None) -> Dict[str, Any]:
        """Revoke an access or refresh token."""
        token_to_revoke = token or self.access_token
        if not token_to_revoke:
            raise ValidationError("No token to revoke")
        
        url = f"{self.base_url}/oauth/revoke"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "token": token_to_revoke,
        }
        
        try:
            response = requests.post(
                url,
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=30,
            )
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("error_code") != 200:
                raise HostexAPIError(
                    result.get("error_msg", "Token revocation failed"),
                    error_code=result.get("error_code", 400),
                    request_id=result.get("request_id"),
                    response_data=result,
                )
            
            # Clear tokens if we revoked our own
            if token_to_revoke == self.access_token:
                self.access_token = None
                self.expires_at = None
            if token_to_revoke == self.refresh_token:
                self.refresh_token = None
            
            return result
            
        except requests.RequestException as e:
            raise AuthenticationError(f"Failed to revoke token: {e}")
    
    def _request_token(self, data: Dict[str, str]) -> Dict[str, Any]:
        """Make a token request to the OAuth endpoint."""
        url = f"{self.base_url}/oauth/authorizations"
        
        try:
            response = requests.post(
                url,
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=30,
            )
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("error_code") != 200:
                raise AuthenticationError(
                    result.get("error_msg", "Token request failed"),
                    error_code=result.get("error_code", 400),
                    request_id=result.get("request_id"),
                    response_data=result,
                )
            
            token_data = result.get("data", {})
            
            # Update instance variables
            if "access_token" in token_data:
                self.access_token = token_data["access_token"]
            if "refresh_token" in token_data:
                self.refresh_token = token_data["refresh_token"]
            if "expires_in" in token_data:
                self.expires_at = time.time() + token_data["expires_in"]
            
            return token_data
            
        except requests.RequestException as e:
            raise AuthenticationError(f"Failed to request token: {e}")
    
    def set_tokens(
        self,
        access_token: str,
        refresh_token: Optional[str] = None,
        expires_in: Optional[int] = None,
    ) -> None:
        """Set tokens manually."""
        self.access_token = access_token
        if refresh_token:
            self.refresh_token = refresh_token
        if expires_in:
            self.expires_at = time.time() + expires_in