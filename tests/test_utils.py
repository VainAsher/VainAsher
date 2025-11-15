"""Tests for utility functions demonstrating edge cases and error handling."""

import pytest
from src.vainasher.utils import (
    validate_email,
    sanitize_string,
    find_duplicates,
    safe_divide_list,
    merge_dictionaries,
)


class TestValidateEmail:
    """Test email validation."""

    def test_valid_email_addresses(self):
        """Test that valid emails are accepted."""
        valid_emails = [
            "user@example.com",
            "first.last@example.com",
            "user+tag@example.co.uk",
            "test123@test-domain.com",
        ]
        for email in valid_emails:
            assert validate_email(email) is True, f"Failed for {email}"

    def test_invalid_email_addresses(self):
        """Test that invalid emails are rejected."""
        invalid_emails = [
            "notanemail",
            "@example.com",
            "user@",
            "user @example.com",
            "user@.com",
            "",
        ]
        for email in invalid_emails:
            assert validate_email(email) is False, f"Failed for {email}"

    def test_none_and_non_string_inputs(self):
        """Test validation with None and non-string inputs."""
        assert validate_email(None) is False
        assert validate_email(123) is False
        assert validate_email([]) is False


class TestSanitizeString:
    """Test string sanitization."""

    def test_sanitize_removes_special_characters(self):
        """Test that special characters are removed."""
        assert sanitize_string("Hello! World@123") == "Hello World123"
        assert sanitize_string("Test#$%String") == "TestString"

    def test_sanitize_collapses_spaces(self):
        """Test that multiple spaces are collapsed."""
        assert sanitize_string("Too    many     spaces") == "Too many spaces"

    def test_sanitize_strips_whitespace(self):
        """Test that leading/trailing whitespace is stripped."""
        assert sanitize_string("  space around  ") == "space around"

    def test_sanitize_with_max_length(self):
        """Test sanitization with max length truncation."""
        result = sanitize_string("This is a long string", max_length=10)
        assert len(result) <= 10
        assert result == "This is a "

    def test_sanitize_empty_string(self):
        """Test sanitizing empty string."""
        assert sanitize_string("") == ""

    def test_sanitize_non_string_raises_error(self):
        """Test that non-string input raises TypeError."""
        with pytest.raises(TypeError, match="Input must be a string"):
            sanitize_string(123)

        with pytest.raises(TypeError):
            sanitize_string(None)


class TestFindDuplicates:
    """Test finding duplicates in lists."""

    def test_find_duplicates_with_duplicates(self):
        """Test finding duplicates when they exist."""
        items = [1, 2, 3, 2, 4, 3, 5]
        duplicates = find_duplicates(items)

        assert set(duplicates) == {2, 3}
        assert len(duplicates) == 2

    def test_find_duplicates_no_duplicates(self):
        """Test when no duplicates exist."""
        items = [1, 2, 3, 4, 5]
        duplicates = find_duplicates(items)

        assert duplicates == []

    def test_find_duplicates_all_same(self):
        """Test when all items are the same."""
        items = [5, 5, 5, 5]
        duplicates = find_duplicates(items)

        assert duplicates == [5]

    def test_find_duplicates_empty_list(self):
        """Test with empty list."""
        duplicates = find_duplicates([])
        assert duplicates == []

    def test_find_duplicates_strings(self):
        """Test finding duplicates in string list."""
        items = ["apple", "banana", "apple", "cherry", "banana"]
        duplicates = find_duplicates(items)

        assert set(duplicates) == {"apple", "banana"}


class TestSafeDivideList:
    """Test safe division of lists."""

    def test_divide_list_by_positive_number(self):
        """Test dividing list by positive number."""
        numbers = [10, 20, 30]
        result = safe_divide_list(numbers, 2)

        assert result == [5.0, 10.0, 15.0]

    def test_divide_list_by_negative_number(self):
        """Test dividing list by negative number."""
        numbers = [10, 20]
        result = safe_divide_list(numbers, -2)

        assert result == [-5.0, -10.0]

    def test_divide_by_zero_raises_error(self):
        """Test that division by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            safe_divide_list([1, 2, 3], 0)

    def test_divide_with_floats(self):
        """Test dividing floats."""
        numbers = [1.5, 2.5, 3.5]
        result = safe_divide_list(numbers, 0.5)

        assert result == [3.0, 5.0, 7.0]

    def test_divide_empty_list(self):
        """Test dividing empty list."""
        result = safe_divide_list([], 5)
        assert result == []

    def test_divide_non_list_raises_error(self):
        """Test that non-list input raises TypeError."""
        with pytest.raises(TypeError, match="numbers must be a list"):
            safe_divide_list("not a list", 5)

    def test_divide_list_with_non_numeric_raises_error(self):
        """Test that non-numeric elements raise TypeError."""
        with pytest.raises(TypeError, match="All elements must be numeric"):
            safe_divide_list([1, 2, "three"], 2)


class TestMergeDictionaries:
    """Test dictionary merging."""

    def test_merge_two_dictionaries(self):
        """Test merging two simple dictionaries."""
        dict1 = {"a": 1, "b": 2}
        dict2 = {"c": 3, "d": 4}

        result = merge_dictionaries(dict1, dict2)
        assert result == {"a": 1, "b": 2, "c": 3, "d": 4}

    def test_merge_overlapping_keys(self):
        """Test merging with overlapping keys (later wins)."""
        dict1 = {"a": 1, "b": 2}
        dict2 = {"b": 3, "c": 4}

        result = merge_dictionaries(dict1, dict2)
        assert result == {"a": 1, "b": 3, "c": 4}

    def test_merge_multiple_dictionaries(self):
        """Test merging more than two dictionaries."""
        dict1 = {"a": 1}
        dict2 = {"b": 2}
        dict3 = {"c": 3}

        result = merge_dictionaries(dict1, dict2, dict3)
        assert result == {"a": 1, "b": 2, "c": 3}

    def test_merge_empty_dictionaries(self):
        """Test merging empty dictionaries."""
        result = merge_dictionaries({}, {})
        assert result == {}

    def test_merge_no_arguments(self):
        """Test merging with no arguments."""
        result = merge_dictionaries()
        assert result == {}

    def test_merge_deep_nested_dictionaries(self):
        """Test deep merging of nested dictionaries."""
        dict1 = {"a": {"b": 1, "c": 2}}
        dict2 = {"a": {"c": 3, "d": 4}}

        result = merge_dictionaries(dict1, dict2, deep=True)
        assert result == {"a": {"b": 1, "c": 3, "d": 4}}

    def test_merge_shallow_nested_dictionaries(self):
        """Test shallow merging (default) replaces nested dicts."""
        dict1 = {"a": {"b": 1, "c": 2}}
        dict2 = {"a": {"d": 4}}

        result = merge_dictionaries(dict1, dict2, deep=False)
        assert result == {"a": {"d": 4}}

    def test_merge_non_dict_raises_error(self):
        """Test that non-dictionary input raises TypeError."""
        with pytest.raises(TypeError, match="All arguments must be dictionaries"):
            merge_dictionaries({"a": 1}, "not a dict")
