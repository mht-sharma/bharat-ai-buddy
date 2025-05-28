#!/usr/bin/env python3
"""
Test runner for Bharat AI Buddy tests.
"""
import unittest
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def run_tests():
    """Run all unit tests and return the results."""
    # Automatically discover and run all tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result

if __name__ == "__main__":
    result = run_tests()
    # Use proper exit code for CI/CD integration
    sys.exit(not result.wasSuccessful())
