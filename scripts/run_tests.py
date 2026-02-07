#!/usr/bin/env python3
"""
Test runner for Omnimathematics Penalty Framework
"""

import unittest
import sys
import os

# Add the penalty_framework directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

def run_tests():
    """Discover and run all tests"""
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success/failure
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)