#!/usr/bin/env python3
"""
Test runner for Ollama connection and model tests

Usage:
    python run_tests.py              # Run all tests
    python run_tests.py -v           # Run with verbose output
    python run_tests.py --real       # Include real Ollama server tests
"""

import unittest
import sys
import os
import argparse

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def main():
    """Main test runner function"""
    parser = argparse.ArgumentParser(description='Run GenAI Demo Ollama tests')
    parser.add_argument('-v', '--verbose', action='store_true', 
                       help='Run tests with verbose output')
    parser.add_argument('--real', action='store_true',
                       help='Include tests that connect to real Ollama server')
    parser.add_argument('--mock-only', action='store_true',
                       help='Run only mocked tests (no real server connection)')
    
    args = parser.parse_args()
    
    # Discover tests
    loader = unittest.TestLoader()
    
    if args.mock_only:
        # Load only mocked tests
        pattern = 'test_ollama_connection.py'
    else:
        # Load all tests
        pattern = 'test_*.py'
    
    suite = loader.discover('tests', pattern=pattern)
    
    # Set up test runner
    verbosity = 2 if args.verbose else 1
    runner = unittest.TextTestRunner(verbosity=verbosity)
    
    print("🧪 Running GenAI Demo Ollama Tests")
    print("=" * 50)
    
    if args.real:
        print("ℹ️  Including real Ollama server tests")
    elif args.mock_only:
        print("ℹ️  Running mocked tests only")
    else:
        print("ℹ️  Running all tests (some may skip if server unavailable)")
    
    print()
    
    # Run tests
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if result.skipped:
        print(f"\n⏭️  SKIPPED TESTS ({len(result.skipped)}):")
        for test, reason in result.skipped:
            print(f"  - {test}: {reason}")
    
    if result.failures:
        print(f"\n❌ FAILURES ({len(result.failures)}):")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print(f"\n🚨 ERRORS ({len(result.errors)}):")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    # Return appropriate exit code
    if result.wasSuccessful():
        print("\n✅ All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {len(result.failures + result.errors)} test(s) failed")
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)