"""API client module to demonstrate mocking external dependencies."""

from typing import Dict, Any, Optional
import json


class APIClient:
    """Client for interacting with external APIs."""

    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """Initialize the API client.

        Args:
            base_url: Base URL for the API
            api_key: Optional API key for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self._session_active = False

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests.

        Returns:
            Dictionary of headers
        """
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def build_url(self, endpoint: str) -> str:
        """Build full URL from endpoint.

        Args:
            endpoint: API endpoint path

        Returns:
            Full URL
        """
        endpoint = endpoint.lstrip('/')
        return f"{self.base_url}/{endpoint}"

    def validate_response(self, response_data: Dict[str, Any]) -> bool:
        """Validate API response structure.

        Args:
            response_data: Response data to validate

        Returns:
            True if valid, False otherwise
        """
        if not isinstance(response_data, dict):
            return False

        # Check for common error indicators
        if "error" in response_data and response_data["error"]:
            return False

        return True

    def parse_json(self, json_string: str) -> Dict[str, Any]:
        """Parse JSON string to dictionary.

        Args:
            json_string: JSON string to parse

        Returns:
            Parsed dictionary

        Raises:
            ValueError: If JSON is invalid
        """
        try:
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")
