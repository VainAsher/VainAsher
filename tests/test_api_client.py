"""Tests for API client module demonstrating mocking patterns."""

import pytest
from src.vainasher.api_client import APIClient


class TestAPIClientInitialization:
    """Test APIClient initialization."""

    def test_init_with_api_key(self):
        """Test initialization with API key."""
        client = APIClient("https://api.example.com", api_key="secret123")
        assert client.base_url == "https://api.example.com"
        assert client.api_key == "secret123"

    def test_init_without_api_key(self):
        """Test initialization without API key."""
        client = APIClient("https://api.example.com")
        assert client.base_url == "https://api.example.com"
        assert client.api_key is None

    def test_init_strips_trailing_slash(self):
        """Test that trailing slash is removed from base URL."""
        client = APIClient("https://api.example.com/")
        assert client.base_url == "https://api.example.com"


class TestGetHeaders:
    """Test header generation."""

    def test_headers_without_api_key(self):
        """Test headers when no API key is provided."""
        client = APIClient("https://api.example.com")
        headers = client._get_headers()

        assert headers["Content-Type"] == "application/json"
        assert "Authorization" not in headers

    def test_headers_with_api_key(self):
        """Test headers when API key is provided."""
        client = APIClient("https://api.example.com", api_key="secret123")
        headers = client._get_headers()

        assert headers["Content-Type"] == "application/json"
        assert headers["Authorization"] == "Bearer secret123"


class TestBuildUrl:
    """Test URL building."""

    def test_build_url_with_simple_endpoint(self):
        """Test building URL with simple endpoint."""
        client = APIClient("https://api.example.com")
        url = client.build_url("users")
        assert url == "https://api.example.com/users"

    def test_build_url_with_leading_slash(self):
        """Test building URL when endpoint has leading slash."""
        client = APIClient("https://api.example.com")
        url = client.build_url("/users")
        assert url == "https://api.example.com/users"

    def test_build_url_with_nested_endpoint(self):
        """Test building URL with nested endpoint."""
        client = APIClient("https://api.example.com")
        url = client.build_url("users/123/posts")
        assert url == "https://api.example.com/users/123/posts"


class TestValidateResponse:
    """Test response validation."""

    def test_validate_response_valid_data(self):
        """Test validation with valid response."""
        client = APIClient("https://api.example.com")
        response = {"status": "success", "data": {"id": 1}}

        assert client.validate_response(response) is True

    def test_validate_response_with_error(self):
        """Test validation with error in response."""
        client = APIClient("https://api.example.com")
        response = {"error": True, "message": "Something went wrong"}

        assert client.validate_response(response) is False

    def test_validate_response_with_false_error(self):
        """Test validation when error key is False."""
        client = APIClient("https://api.example.com")
        response = {"error": False, "data": {"id": 1}}

        # Error is present but False, so should return False
        assert client.validate_response(response) is False

    def test_validate_response_non_dict(self):
        """Test validation with non-dictionary response."""
        client = APIClient("https://api.example.com")

        assert client.validate_response("not a dict") is False
        assert client.validate_response([1, 2, 3]) is False
        assert client.validate_response(None) is False


class TestParseJson:
    """Test JSON parsing."""

    def test_parse_valid_json(self):
        """Test parsing valid JSON."""
        client = APIClient("https://api.example.com")
        json_string = '{"name": "Alice", "age": 30}'

        result = client.parse_json(json_string)
        assert result == {"name": "Alice", "age": 30}

    def test_parse_empty_json_object(self):
        """Test parsing empty JSON object."""
        client = APIClient("https://api.example.com")
        result = client.parse_json('{}')
        assert result == {}

    def test_parse_invalid_json_raises_error(self):
        """Test that invalid JSON raises ValueError."""
        client = APIClient("https://api.example.com")

        with pytest.raises(ValueError, match="Invalid JSON"):
            client.parse_json('{"invalid": json}')

    def test_parse_malformed_json(self):
        """Test parsing malformed JSON."""
        client = APIClient("https://api.example.com")

        with pytest.raises(ValueError):
            client.parse_json('{name: Alice}')
