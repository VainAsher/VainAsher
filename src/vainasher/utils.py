"""Utility functions demonstrating edge cases and error handling."""

from typing import List, Optional, Any
import re


def validate_email(email: str) -> bool:
    """Validate email address format.

    Args:
        email: Email address to validate

    Returns:
        True if valid email format, False otherwise
    """
    if not email or not isinstance(email, str):
        return False

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def sanitize_string(text: str, max_length: Optional[int] = None) -> str:
    """Sanitize string by removing special characters and optionally truncating.

    Args:
        text: Text to sanitize
        max_length: Optional maximum length

    Returns:
        Sanitized string
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string")

    # Remove special characters, keep alphanumeric and spaces
    sanitized = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    # Collapse multiple spaces
    sanitized = re.sub(r'\s+', ' ', sanitized).strip()

    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]

    return sanitized


def find_duplicates(items: List[Any]) -> List[Any]:
    """Find duplicate items in a list.

    Args:
        items: List to search for duplicates

    Returns:
        List of duplicate items (each unique duplicate appears once)
    """
    seen = set()
    duplicates = set()

    for item in items:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)

    return list(duplicates)


def safe_divide_list(numbers: List[float], divisor: float) -> List[float]:
    """Safely divide all numbers in a list by a divisor.

    Args:
        numbers: List of numbers to divide
        divisor: Number to divide by

    Returns:
        List of divided numbers

    Raises:
        ValueError: If divisor is zero
        TypeError: If inputs are not numeric
    """
    if divisor == 0:
        raise ValueError("Cannot divide by zero")

    if not isinstance(numbers, list):
        raise TypeError("numbers must be a list")

    result = []
    for num in numbers:
        if not isinstance(num, (int, float)):
            raise TypeError(f"All elements must be numeric, got {type(num)}")
        result.append(num / divisor)

    return result


def merge_dictionaries(*dicts: Dict[str, Any], deep: bool = False) -> Dict[str, Any]:
    """Merge multiple dictionaries.

    Args:
        *dicts: Variable number of dictionaries to merge
        deep: If True, perform deep merge for nested dicts

    Returns:
        Merged dictionary
    """
    if not dicts:
        return {}

    result = {}

    for d in dicts:
        if not isinstance(d, dict):
            raise TypeError("All arguments must be dictionaries")

        for key, value in d.items():
            if deep and key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = merge_dictionaries(result[key], value, deep=True)
            else:
                result[key] = value

    return result
