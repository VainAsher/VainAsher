"""Data processing module to demonstrate class-based testing."""

from typing import List, Dict, Any, Optional


class DataProcessor:
    """Process and analyze data."""

    def __init__(self, data: Optional[List[Dict[str, Any]]] = None):
        """Initialize the data processor.

        Args:
            data: Optional initial data to process
        """
        self.data = data or []
        self._processed = False

    def add_record(self, record: Dict[str, Any]) -> None:
        """Add a record to the dataset.

        Args:
            record: Dictionary containing record data
        """
        self.data.append(record)
        self._processed = False

    def filter_by_key(self, key: str, value: Any) -> List[Dict[str, Any]]:
        """Filter records by a key-value pair.

        Args:
            key: The key to filter on
            value: The value to match

        Returns:
            List of records matching the filter
        """
        return [record for record in self.data if record.get(key) == value]

    def get_unique_values(self, key: str) -> List[Any]:
        """Get unique values for a given key across all records.

        Args:
            key: The key to extract values from

        Returns:
            List of unique values
        """
        values = [record.get(key) for record in self.data if key in record]
        return list(set(values))

    def aggregate_sum(self, key: str) -> float:
        """Calculate sum of numeric values for a given key.

        Args:
            key: The key containing numeric values

        Returns:
            Sum of all numeric values

        Raises:
            ValueError: If non-numeric values are encountered
        """
        total = 0
        for record in self.data:
            if key in record:
                value = record[key]
                if not isinstance(value, (int, float)):
                    raise ValueError(f"Non-numeric value found: {value}")
                total += value
        return total

    def count_records(self) -> int:
        """Count total number of records.

        Returns:
            Number of records in the dataset
        """
        return len(self.data)

    def clear(self) -> None:
        """Clear all records from the dataset."""
        self.data = []
        self._processed = False
