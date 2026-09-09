#!/usr/bin/env python
"""Verify and execute all Gajab test cases."""
import sys
import os
from pathlib import Path

# Add framework to path
sys.path.insert(0, str(Path(__file__).parent))

print("="*80)
print("GAJAB AUTOMATION TEST SUITE - VERIFICATION & EXECUTION GUIDE")
print("="*80)

# Check all test files exist
test_files = {
    "Authentication": "framework/tests/web/gajab/flow_cases/test_01_login_otp.py",
    "Location & Home": "framework/tests/web/gajab/flow_cases/test_02_location_and_home.py",
    "Product Filters": "framework/tests/web/gajab/flow_cases/test_03_product_filters.py",
    "Automated Matrix": "framework/tests/web/gajab/test_automated_matrix.py",
    "API Tests": "framework/tests/web/test_api_example.py",
    "Data Driven": "framework/tests/web/test_data_driven_example.py",
}

base_dir = Path(__file__).parent
print("\n1. CHECKING TEST FILES EXIST")
print("-" * 80)

existing_tests = {}
for name, path in test_files.items():
    full_path = base_dir / path
    exists = full_path.exists()
    status = "✓ EXISTS" if exists else "✗ MISSING"
    print(f"{status:15} {name:20} - {path}")
    if exists:
        existing_tests[name] = path

print(f"\nTotal: {len(existing_tests)}/{len(test_files)} test files found")

# Verify imports
print("\n2. CHECKING IMPORTS")
print("-" * 80)

try:
    from framework.config.settings import settings
    print("✓ Settings imported")
except Exception as e:
    print(f"✗ Settings import failed: {e}")
    sys.exit(1)

try:
    from framework.pages.gajab.login_page import GajabLoginPage
    from framework.pages.gajab.home_page import GajabHomePage
    from framework.pages.gajab.product_list_page import GajabProductListPage
    print("✓ Page objects imported")
except Exception as e:
    print(f"✗ Page objects import failed: {e}")
    sys.exit(1)

try:
    from framework.core.api_client import ApiClient
    print("✓ API client imported")
except Exception as e:
    print(f"✗ API client import failed: {e}")

# Check environment
print("\n3. CHECKING ENVIRONMENT")
print("-" * 80)

print(f"Base URL: {settings.base_url}")
print(f"Environment: {settings.env}")
print(f"Headless: {settings.headless}")
print(f"Timeout: {settings.default_timeout_ms}ms")

api_key_set = bool(os.getenv("OPENAI_API_KEY"))
print(f"OpenAI API Key: {'✓ SET' if api_key_set else '✗ NOT SET (AI features disabled)'}")

print("\n4. TEST EXECUTION COMMANDS")
print("-" * 80)
print("""
Run individual test suites:

# Authentication tests
pytest framework/tests/web/gajab/flow_cases/test_01_login_otp.py -v

# Location & Home page tests  
pytest framework/tests/web/gajab/flow_cases/test_02_location_and_home.py -v

# Product filter tests
pytest framework/tests/web/gajab/flow_cases/test_03_product_filters.py -v

# All Gajab tests (automated matrix)
pytest framework/tests/web/gajab/test_automated_matrix.py -v

# All Gajab tests together
pytest framework/tests/web/gajab/ -v

# With HTML report
pytest framework/tests/web/gajab/ -v --html=reports/gajab-report.html --self-contained-html

# Run specific test
pytest framework/tests/web/gajab/flow_cases/test_02_location_and_home.py::test_home_sections_return_dynamic_products -v

# Run with markers
pytest framework/tests/web/gajab/ -v -m critical

# Full automation suite (all tests)
pytest framework/tests/ -v --html=reports/full-report.html
""")

print("\n5. TEST CASE MATRIX")
print("-" * 80)

test_matrix = {
    "GJ-MAN-001": {"Description": "Login with OTP", "File": "test_01_login_otp.py", "Status": "⚠ May fail (website OTP field broken)"},
    "GJ-MAN-005": {"Description": "Pincode selection", "File": "test_02_location_and_home.py", "Status": "⚠ Needs verification"},
    "GJ-MAN-007": {"Description": "Deal of the Day", "File": "test_02_location_and_home.py", "Status": "✓ Should work"},
    "GJ-MAN-008": {"Description": "Most-bargained product", "File": "test_02_location_and_home.py", "Status": "✓ Should work"},
    "GJ-MAN-010": {"Description": "Cheapest product", "File": "test_02_location_and_home.py", "Status": "✓ Should work"},
    "GJ-MAN-011+": {"Description": "Category navigation", "File": "test_03_product_filters.py", "Status": "✓ Should work"},
    "GJ-MAN-012+": {"Description": "Brand filters", "File": "test_03_product_filters.py", "Status": "✓ Should work"},
    "GJ-MAN-013+": {"Description": "Price filters", "File": "test_03_product_filters.py", "Status": "✓ Should work"},
}

for case_id, details in test_matrix.items():
    print(f"{case_id:15} - {details['Description']:25} [{details['File']:30}] {details['Status']}")

print("\n" + "="*80)
print("NEXT STEPS:")
print("="*80)
print("""
1. Run all Gajab tests:
   pytest framework/tests/web/gajab/ -v --html=reports/gajab-full.html --self-contained-html

2. Check test results:
   - Passing tests: Ready for submission
   - Failing tests: Investigate selectors or workaround

3. For login failures:
   - Skip login tests if they fail due to Gajab website
   - Focus on non-login features
   - Document as "Known Limitation"

4. Generate report:
   - Reports are in: reports/ directory
   - Open HTML reports in browser to see detailed results
""")
