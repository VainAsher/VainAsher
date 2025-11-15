"""Tests for data processor module demonstrating class-based testing."""

import pytest
from src.vainasher.data_processor import DataProcessor


class TestDataProcessorInitialization:
    """Test DataProcessor initialization."""

    def test_init_with_no_data(self):
        """Test initialization without data."""
        processor = DataProcessor()
        assert processor.data == []
        assert processor.count_records() == 0

    def test_init_with_data(self):
        """Test initialization with data."""
        initial_data = [{"name": "Alice", "age": 30}]
        processor = DataProcessor(data=initial_data)
        assert processor.count_records() == 1


class TestAddRecord:
    """Test adding records to the processor."""

    def test_add_single_record(self):
        """Test adding a single record."""
        processor = DataProcessor()
        processor.add_record({"name": "Bob", "age": 25})
        assert processor.count_records() == 1

    def test_add_multiple_records(self):
        """Test adding multiple records."""
        processor = DataProcessor()
        processor.add_record({"name": "Alice", "age": 30})
        processor.add_record({"name": "Bob", "age": 25})
        assert processor.count_records() == 2


class TestFilterByKey:
    """Test filtering records."""

    @pytest.fixture
    def populated_processor(self):
        """Fixture providing a processor with test data."""
        processor = DataProcessor()
        processor.add_record({"name": "Alice", "age": 30, "city": "NYC"})
        processor.add_record({"name": "Bob", "age": 25, "city": "LA"})
        processor.add_record({"name": "Charlie", "age": 30, "city": "NYC"})
        return processor

    def test_filter_by_existing_value(self, populated_processor):
        """Test filtering by an existing value."""
        results = populated_processor.filter_by_key("age", 30)
        assert len(results) == 2
        assert all(r["age"] == 30 for r in results)

    def test_filter_by_non_existing_value(self, populated_processor):
        """Test filtering by non-existing value."""
        results = populated_processor.filter_by_key("age", 99)
        assert len(results) == 0

    def test_filter_by_string_value(self, populated_processor):
        """Test filtering by string value."""
        results = populated_processor.filter_by_key("city", "NYC")
        assert len(results) == 2


class TestGetUniqueValues:
    """Test getting unique values."""

    def test_get_unique_values_with_duplicates(self):
        """Test getting unique values when duplicates exist."""
        processor = DataProcessor()
        processor.add_record({"status": "active"})
        processor.add_record({"status": "inactive"})
        processor.add_record({"status": "active"})

        unique_statuses = processor.get_unique_values("status")
        assert len(unique_statuses) == 2
        assert set(unique_statuses) == {"active", "inactive"}

    def test_get_unique_values_missing_key(self):
        """Test getting unique values for non-existent key."""
        processor = DataProcessor()
        processor.add_record({"name": "Alice"})
        processor.add_record({"name": "Bob"})

        unique_values = processor.get_unique_values("age")
        assert len(unique_values) == 0


class TestAggregateSum:
    """Test aggregating sums."""

    def test_aggregate_sum_integers(self):
        """Test summing integer values."""
        processor = DataProcessor()
        processor.add_record({"score": 10})
        processor.add_record({"score": 20})
        processor.add_record({"score": 30})

        total = processor.aggregate_sum("score")
        assert total == 60

    def test_aggregate_sum_floats(self):
        """Test summing float values."""
        processor = DataProcessor()
        processor.add_record({"price": 10.5})
        processor.add_record({"price": 20.75})

        total = processor.aggregate_sum("price")
        assert pytest.approx(total, 0.01) == 31.25

    def test_aggregate_sum_non_numeric_raises_error(self):
        """Test that non-numeric values raise ValueError."""
        processor = DataProcessor()
        processor.add_record({"value": "not a number"})

        with pytest.raises(ValueError, match="Non-numeric value found"):
            processor.aggregate_sum("value")

    def test_aggregate_sum_empty_data(self):
        """Test summing with no data."""
        processor = DataProcessor()
        total = processor.aggregate_sum("score")
        assert total == 0


class TestClear:
    """Test clearing data."""

    def test_clear_removes_all_records(self):
        """Test that clear removes all records."""
        processor = DataProcessor()
        processor.add_record({"name": "Alice"})
        processor.add_record({"name": "Bob"})

        assert processor.count_records() == 2

        processor.clear()
        assert processor.count_records() == 0
        assert processor.data == []
