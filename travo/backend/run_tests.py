#!/usr/bin/env python
import os
import sys
import pytest
import argparse


def main():
    """Run the test suite with specified options."""
    parser = argparse.ArgumentParser(description="Run TRAVO backend tests")
    parser.add_argument(
        "--service", 
        choices=["all", "vision", "recommendation"], 
        default="all",
        help="Specify which service tests to run"
    )
    parser.add_argument(
        "--verbose", "-v", 
        action="store_true", 
        help="Enable verbose output"
    )
    parser.add_argument(
        "--coverage", 
        action="store_true", 
        help="Generate coverage report"
    )
    
    args = parser.parse_args()
    
    # Build pytest arguments
    pytest_args = []
    
    # Add verbosity
    if args.verbose:
        pytest_args.append("-v")
    
    # Add coverage if requested
    if args.coverage:
        pytest_args.extend(["--cov=services", "--cov-report=term", "--cov-report=html"])
    
    # Select tests based on service
    if args.service == "vision":
        pytest_args.append("tests/test_vision_service.py")
    elif args.service == "recommendation":
        pytest_args.append("tests/test_recommendation_service.py")
    else:  # all
        pytest_args.append("tests/")
    
    # Run the tests
    return pytest.main(pytest_args)


if __name__ == "__main__":
    sys.exit(main())
