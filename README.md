# VainAsher Python Project

A Python project demonstrating best practices for testing, code coverage, and CI/CD.

## About Me

- 👋 Hi, I'm @VainAsher
- 👀 I'm interested in gaming and homelabbing
- 🌱 I'm currently learning self hosted virtualization
- ⚡ Fun fact: I'm also learning software development and testing best practices!

## Project Structure

```
VainAsher/
├── src/
│   └── vainasher/
│       ├── __init__.py
│       ├── calculator.py        # Basic mathematical operations
│       ├── data_processor.py    # Data processing and analysis
│       ├── api_client.py        # API client utilities
│       └── utils.py             # Utility functions
├── tests/
│   ├── __init__.py
│   ├── test_calculator.py
│   ├── test_data_processor.py
│   ├── test_api_client.py
│   └── test_utils.py
├── .github/
│   └── workflows/
│       └── tests.yml            # CI/CD pipeline
├── pyproject.toml               # Project configuration
├── requirements.txt             # Production dependencies
├── requirements-dev.txt         # Development dependencies
└── run_tests.sh                 # Test runner script
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/VainAsher/VainAsher.git
cd VainAsher
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements-dev.txt
pip install -e .
```

## Running Tests

### Quick Test Run

```bash
pytest
```

### Run Tests with Coverage Report

```bash
./run_tests.sh
```

Or manually:
```bash
pytest --cov=src/vainasher --cov-report=term-missing --cov-report=html
```

### View HTML Coverage Report

After running tests with coverage, open the HTML report:
```bash
open htmlcov/index.html  # On macOS
xdg-open htmlcov/index.html  # On Linux
start htmlcov/index.html  # On Windows
```

### Run Specific Tests

```bash
# Run tests for a specific module
pytest tests/test_calculator.py

# Run a specific test class
pytest tests/test_calculator.py::TestAddition

# Run a specific test function
pytest tests/test_calculator.py::TestAddition::test_add_positive_numbers
```

## Code Quality

### Linting

```bash
flake8 src
```

### Type Checking

```bash
mypy src/vainasher --ignore-missing-imports
```

### Code Formatting

```bash
black src tests
```

## Test Coverage Analysis

### Current Coverage

The project aims for **80%+ test coverage**. Run tests to see current coverage:

```bash
pytest --cov=src/vainasher --cov-report=term-missing
```

### Coverage Reports

The project generates three types of coverage reports:

1. **Terminal Report**: Shows coverage summary in the console
2. **HTML Report**: Interactive report in `htmlcov/index.html`
3. **XML Report**: Machine-readable `coverage.xml` for CI/CD integration

### What's Tested

The test suite includes:

- **Unit Tests**: Testing individual functions and methods
- **Class-Based Tests**: Testing object-oriented code
- **Edge Cases**: Boundary conditions and unusual inputs
- **Error Handling**: Exception raising and handling
- **Type Validation**: Input type checking
- **Integration Patterns**: Using fixtures and mocks

## Areas for Test Improvement

Based on the current setup, here are key areas where you should focus testing efforts:

### 1. Integration Testing
**Current Gap**: Only unit tests exist
**Recommendation**: Add integration tests that verify multiple components working together

```python
# Example: tests/integration/test_data_workflow.py
def test_complete_data_processing_workflow():
    # Test DataProcessor + Utils working together
    pass
```

### 2. Mocking External Dependencies
**Current Gap**: API client doesn't have tests with actual HTTP mocking
**Recommendation**: Use `pytest-mock` or `responses` library to mock HTTP calls

```python
# Example addition to test_api_client.py
def test_api_call_with_mock(mocker):
    # Mock actual HTTP requests
    pass
```

### 3. Parametrized Tests
**Current Gap**: Some tests could be more concise with parametrization
**Recommendation**: Use `@pytest.mark.parametrize` for testing multiple inputs

```python
@pytest.mark.parametrize("email,expected", [
    ("valid@email.com", True),
    ("invalid", False),
])
def test_email_validation(email, expected):
    assert validate_email(email) == expected
```

### 4. Performance Testing
**Current Gap**: No performance or load tests
**Recommendation**: Add benchmark tests for performance-critical functions

```python
# Example: tests/test_performance.py
def test_data_processor_performance(benchmark):
    processor = DataProcessor()
    benchmark(processor.aggregate_sum, "score")
```

### 5. Property-Based Testing
**Current Gap**: Only example-based tests
**Recommendation**: Use `hypothesis` for property-based testing

```python
from hypothesis import given
import hypothesis.strategies as st

@given(st.integers(), st.integers())
def test_add_commutative(a, b):
    assert add(a, b) == add(b, a)
```

### 6. Error Message Testing
**Current Gap**: Tests verify exceptions are raised but not messages
**Recommendation**: More specific error message assertions

```python
# Already done in some tests, expand to all error cases
with pytest.raises(ValueError, match="Cannot divide by zero"):
    divide(5, 0)
```

### 7. Boundary Testing
**Current Gap**: Limited boundary condition testing
**Recommendation**: Test edge cases more thoroughly
- Maximum/minimum values
- Empty inputs
- Very large datasets
- Unicode and special characters

### 8. Test Documentation
**Current Gap**: Some tests lack detailed docstrings
**Recommendation**: Add clear docstrings to all tests explaining what they verify

### 9. Fixture Expansion
**Current Gap**: Limited use of fixtures for test data
**Recommendation**: Create more reusable fixtures in `conftest.py`

```python
# tests/conftest.py
@pytest.fixture
def sample_user_data():
    return {"name": "Test User", "email": "test@example.com"}
```

### 10. Mutation Testing
**Current Gap**: No mutation testing to verify test quality
**Recommendation**: Use `mutmut` to ensure tests catch bugs

```bash
pip install mutmut
mutmut run
```

## CI/CD

The project uses GitHub Actions for continuous integration. On every push and pull request:

1. Tests run on Python 3.8, 3.9, 3.10, 3.11, and 3.12
2. Code is linted with flake8
3. Type checking with mypy
4. Coverage reports are generated
5. Coverage reports uploaded to Codecov (when configured)

See `.github/workflows/tests.yml` for details.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for your changes
4. Ensure all tests pass and coverage remains above 80%
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This is a personal project for learning and experimentation.

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)
- [Test Coverage Best Practices](https://testing.googleblog.com/2020/08/code-coverage-best-practices.html)
