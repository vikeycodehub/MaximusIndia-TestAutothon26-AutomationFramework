#!/usr/bin/env python
"""Run all Gajab test cases and generate execution report."""
import subprocess
import sys
from pathlib import Path
from datetime import datetime

test_dir = Path(__file__).parent

# All test files to run
test_files = [
    "framework/tests/web/gajab/test_automated_matrix.py",
    "framework/tests/web/gajab/flow_cases/test_01_login_otp.py",
    "framework/tests/web/gajab/flow_cases/test_02_location_and_home.py",
    "framework/tests/web/gajab/flow_cases/test_03_product_filters.py",
    "framework/tests/web/test_api_example.py",
    "framework/tests/web/test_data_driven_example.py",
]

print("="*80)
print("RUNNING ALL GAJAB AUTOMATION TEST CASES")
print(f"Timestamp: {datetime.now().isoformat()}")
print("="*80 + "\n")

results = {}

for test_file in test_files:
    test_path = test_dir / test_file
    if not test_path.exists():
        print(f"⚠️  {test_file} - NOT FOUND")
        results[test_file] = {"status": "NOT_FOUND"}
        continue
    
    print(f"\n{'='*80}")
    print(f"Running: {test_file}")
    print(f"{'='*80}")
    
    cmd = [
        sys.executable, "-m", "pytest",
        test_file,
        "-v", "--tb=short",
        f"--html=reports/pytest-{test_file.replace('/', '-')}.html",
        "--self-contained-html"
    ]
    
    result = subprocess.run(cmd, cwd=str(test_dir), capture_output=True, text=True, timeout=60)
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    results[test_file] = {
        "status": "PASSED" if result.returncode == 0 else "FAILED",
        "return_code": result.returncode
    }
    print(f"Status: {'✅ PASSED' if result.returncode == 0 else '❌ FAILED'}")

print("\n" + "="*80)
print("TEST EXECUTION SUMMARY")
print("="*80)
for test_file, result in results.items():
    status_symbol = "✅" if result["status"] == "PASSED" else "❌" if result["status"] == "FAILED" else "⚠️"
    print(f"{status_symbol} {test_file}: {result['status']}")

passed_count = sum(1 for r in results.values() if r["status"] == "PASSED")
total_count = len([r for r in results.values() if r["status"] != "NOT_FOUND"])

print(f"\nTotal: {passed_count}/{total_count} passed")
print("="*80)
