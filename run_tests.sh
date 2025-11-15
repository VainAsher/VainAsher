#!/bin/bash
# Script to run tests with coverage reporting

set -e

echo "Running tests with coverage..."
pytest

echo ""
echo "Coverage report generated!"
echo "  - Terminal report shown above"
echo "  - HTML report: htmlcov/index.html"
echo "  - XML report: coverage.xml"
