# Testing Guide

Comprehensive guide to testing practices in this project.

## Test Coverage Goals

### Overall Coverage Target: 80%+

We aim for high test coverage while focusing on meaningful tests that catch real bugs.

### Coverage by Module

| Module | Current Coverage | Target | Priority Areas |
|--------|-----------------|--------|----------------|
| calculator.py | ~100% | 100% | Edge cases, error handling |
| data_processor.py | ~100% | 100% | State management, data validation |
| api_client.py | ~90% | 95% | HTTP mocking, error scenarios |
| utils.py | ~100% | 100% | Input validation, edge cases |

## Testing Pyramid

Our tests follow the testing pyramid principle:

```
       /\
      /  \     E2E Tests (Few)
     /----\
    /      \   Integration Tests (Some)
   /--------\
  /          \ Unit Tests (Many)
 /____________\
```

### Unit Tests (70%)
- Test individual functions and methods in isolation
- Fast, focused, and abundant
- Located in: `tests/test_*.py`

### Integration Tests (20%)
- Test multiple components working together
- Verify data flows between modules
- **TO BE ADDED**: `tests/integration/`

### End-to-End Tests (10%)
- Test complete workflows
- Validate user-facing functionality
- **TO BE ADDED**: `tests/e2e/`

## Test Organization

### Naming Conventions

**Test Files**: `test_<module_name>.py`
- `test_calculator.py` tests `calculator.py`
- `test_utils.py` tests `utils.py`

**Test Classes**: `Test<Functionality>`
- `TestAddition` for testing addition functionality
- `TestDataProcessorInitialization` for initialization tests

**Test Functions**: `test_<what>_<condition>_<expected>`
- `test_divide_by_zero_raises_error`
- `test_add_positive_numbers`
- `test_filter_by_non_existing_value`

### Test Structure (Arrange-Act-Assert)

```python
def test_example():
    # Arrange: Set up test data and conditions
    processor = DataProcessor()
    test_data = {"name": "Test"}

    # Act: Execute the functionality being tested
    processor.add_record(test_data)

    # Assert: Verify the expected outcome
    assert processor.count_records() == 1
```

## What to Test

### Priority 1: Critical Path
- Core business logic
- Data transformations
- API interactions
- Error handling

### Priority 2: Edge Cases
- Empty inputs
- Null/None values
- Maximum/minimum values
- Type mismatches

### Priority 3: Error Scenarios
- Invalid inputs
- Exception handling
- Error messages
- Recovery mechanisms

### Priority 4: Integration Points
- Module interactions
- Data flow
- State management
- External dependencies

## What NOT to Test

- Third-party library internals
- Python built-in functions
- Simple getters/setters without logic
- Auto-generated code
- Configuration files

## Writing Effective Tests

### 1. Test One Thing at a Time

**Bad:**
```python
def test_everything():
    assert add(1, 2) == 3
    assert subtract(5, 3) == 2
    assert multiply(2, 3) == 6
```

**Good:**
```python
def test_add_positive_numbers():
    assert add(1, 2) == 3

def test_subtract_positive_numbers():
    assert subtract(5, 3) == 2
```

### 2. Use Descriptive Names

**Bad:**
```python
def test_1():
    assert validate_email("test@test.com") is True
```

**Good:**
```python
def test_validate_email_accepts_valid_format():
    assert validate_email("test@test.com") is True
```

### 3. Test Behavior, Not Implementation

**Bad (tests implementation):**
```python
def test_uses_regex():
    # This test breaks if we change implementation
    assert "re.match" in inspect.getsource(validate_email)
```

**Good (tests behavior):**
```python
def test_validates_email_format():
    assert validate_email("valid@email.com") is True
    assert validate_email("invalid") is False
```

### 4. Use Fixtures for Common Setup

**Bad:**
```python
def test_filter():
    processor = DataProcessor()
    processor.add_record({"name": "Alice"})
    processor.add_record({"name": "Bob"})
    # ... test code

def test_count():
    processor = DataProcessor()
    processor.add_record({"name": "Alice"})
    processor.add_record({"name": "Bob"})
    # ... test code
```

**Good:**
```python
@pytest.fixture
def populated_processor():
    processor = DataProcessor()
    processor.add_record({"name": "Alice"})
    processor.add_record({"name": "Bob"})
    return processor

def test_filter(populated_processor):
    # ... test code

def test_count(populated_processor):
    # ... test code
```

### 5. Test Error Cases

```python
def test_divide_by_zero_raises_error():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)
```

### 6. Use Parametrize for Similar Tests

**Bad:**
```python
def test_email_valid_1():
    assert validate_email("user@example.com") is True

def test_email_valid_2():
    assert validate_email("test@test.co.uk") is True
```

**Good:**
```python
@pytest.mark.parametrize("email", [
    "user@example.com",
    "test@test.co.uk",
    "first.last@domain.org",
])
def test_email_validation_accepts_valid_emails(email):
    assert validate_email(email) is True
```

## Advanced Testing Techniques

### Mocking

Use mocking to isolate tests from external dependencies:

```python
def test_api_call_with_mock(mocker):
    # Mock the HTTP library
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"status": "success"}

    mocker.patch('requests.get', return_value=mock_response)

    # Test your code that uses requests.get
    # ...
```

### Property-Based Testing

Test properties that should always hold true:

```python
from hypothesis import given
import hypothesis.strategies as st

@given(st.integers(), st.integers())
def test_addition_is_commutative(a, b):
    """Addition should be commutative: a + b = b + a"""
    assert add(a, b) == add(b, a)

@given(st.lists(st.integers()))
def test_find_duplicates_never_returns_unique_items(items):
    """Duplicates list should not contain items that appear once"""
    duplicates = find_duplicates(items)
    for dup in duplicates:
        assert items.count(dup) > 1
```

### Performance Testing

```python
import pytest

@pytest.mark.benchmark
def test_data_processor_performance(benchmark):
    processor = DataProcessor()
    for i in range(1000):
        processor.add_record({"id": i, "value": i * 2})

    result = benchmark(processor.aggregate_sum, "value")
    assert result == sum(i * 2 for i in range(1000))
```

## Running Tests

### Run All Tests
```bash
pytest
```

### Run with Coverage
```bash
pytest --cov=src/vainasher --cov-report=html
```

### Run Specific Tests
```bash
# By file
pytest tests/test_calculator.py

# By class
pytest tests/test_calculator.py::TestAddition

# By function
pytest tests/test_calculator.py::TestAddition::test_add_positive_numbers

# By marker
pytest -m slow  # Run only slow tests

# By keyword
pytest -k "addition"  # Run tests with "addition" in name
```

### Run with Verbose Output
```bash
pytest -v
```

### Run and Stop on First Failure
```bash
pytest -x
```

### Run Last Failed Tests
```bash
pytest --lf
```

## Coverage Analysis

### Reading Coverage Reports

After running tests with coverage:

```bash
pytest --cov=src/vainasher --cov-report=term-missing
```

Output shows:
- **Stmts**: Total statements in file
- **Miss**: Statements not covered by tests
- **Cover**: Coverage percentage
- **Missing**: Line numbers not covered

### Improving Coverage

1. **Identify uncovered lines**: Check coverage report
2. **Write tests for missing lines**: Focus on critical paths first
3. **Verify tests are meaningful**: Don't just execute code, verify behavior
4. **Check for dead code**: Remove if truly unreachable

### Coverage Exemptions

Mark code that doesn't need coverage:

```python
def debug_only_function():  # pragma: no cover
    # This won't affect coverage metrics
    print("Debug info")

if __name__ == "__main__":  # pragma: no cover
    main()
```

## Continuous Integration

Our CI pipeline runs on every push and pull request:

1. **Lint Check**: Ensures code style compliance
2. **Type Check**: Validates type hints
3. **Unit Tests**: Runs all unit tests
4. **Coverage Check**: Fails if coverage drops below 80%
5. **Report Upload**: Sends coverage to Codecov

See `.github/workflows/tests.yml` for configuration.

## Test Maintenance

### When to Update Tests

- **After bug fixes**: Add test to prevent regression
- **When adding features**: Write tests first (TDD)
- **When refactoring**: Ensure tests still pass
- **When requirements change**: Update tests to match

### Avoiding Flaky Tests

- **Don't depend on timing**: Use deterministic waits
- **Avoid external dependencies**: Mock APIs and databases
- **Clean up after tests**: Use fixtures with cleanup
- **Don't rely on order**: Each test should be independent

### Test Code Quality

Tests are code too! Apply the same standards:

- Clear naming
- No duplication
- Good documentation
- Regular refactoring

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
- [pytest-mock](https://pytest-mock.readthedocs.io/)
- [Hypothesis](https://hypothesis.readthedocs.io/)
- [Effective Python Testing](https://realpython.com/pytest-python-testing/)
- [Test-Driven Development](https://testdriven.io/test-driven-development/)

## Getting Help

- Check existing tests for examples
- Review pytest documentation
- Ask in pull request reviews
- Consult the team lead

Remember: **Good tests are investments in code quality and developer confidence!**
