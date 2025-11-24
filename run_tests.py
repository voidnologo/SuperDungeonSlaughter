#!/usr/bin/env python
"""Central test runner for SuperDungeonSlaughter test suite."""

import sys
import unittest


def run_tests() -> int:
    """Discover and run all tests in the src/tests directory."""
    loader = unittest.TestLoader()
    start_dir = 'src/tests'
    suite = loader.discover(start_dir, pattern='test_*.py')

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
