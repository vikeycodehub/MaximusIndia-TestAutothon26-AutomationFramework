#!/usr/bin/env python
"""Direct test runner to capture errors."""
import sys
import subprocess
from pathlib import Path

test_dir = Path(__file__).parent
sys.path.insert(0, str(test_dir))

# Run a simple test and capture output
cmd = [
    sys.executable, "-m", "pytest",
    "framework/tests/web/gajab/flow_cases/test_02_location_and_home.py::test_pincode_is_reflected_in_header",
    "-v", "--tb=short", "-s", "--capture=no"
]

print("Running command:", " ".join(cmd))
print("=" * 80)

result = subprocess.run(cmd, cwd=str(test_dir))
sys.exit(result.returncode)
