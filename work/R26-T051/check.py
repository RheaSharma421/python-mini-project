#!/usr/bin/env python3
"""
work/R26-T051/check.py
Focused runner for R26-T051 regression tests.

WHY THE OLD check.py FAILED WITH ModuleNotFoundError: No module named 'tests'
-------------------------------------------------------------------------------
The old runner used:
    python3 -m unittest discover -s tests -p test_word_scramble_game.py -t .

In Python 3.11+ the `discover` sub-command requires the start directory (-s)
to be *importable* as a package (i.e. it must contain an __init__.py).
The `tests/` directory in this repo has no __init__.py, so Python cannot
treat it as a package named "tests" – hence the ImportError.

There are three correct fixes:
  (a) Add an __init__.py to tests/  — changes shared infrastructure, undesirable.
  (b) Call the test file as a script: python3 tests/test_word_scramble_game.py
      — only works when the file has an `if __name__ == "__main__"` block.
  (c) Use pytest, which uses its own file-based collector and does NOT
      require __init__.py.  This is exactly what the project's CI workflow
      does (see .github/workflows/tests.yml: "pytest tests/ -v --tb=short").

This runner uses fix (c): it delegates to the venv pytest so it matches CI.

Usage (from repo root):
    python3 work/R26-T051/check.py
Exit codes:
    0  – all tests passed
    non-zero – at least one test failed or an error occurred
"""

import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]      # …/python-mini-project
VENV_PYTEST = REPO_ROOT / ".venv" / "bin" / "pytest"
TEST_FILE   = REPO_ROOT / "tests" / "test_word_scramble_game.py"

# ---------------------------------------------------------------------------
# Build the command
# ---------------------------------------------------------------------------
# We invoke the venv pytest directly (not via -m) so there is no dependency
# on the system Python having pytest installed – matching the documented
# "use a virtual environment" requirement.
cmd = [
    str(VENV_PYTEST),
    str(TEST_FILE),
    "-v",
    "--tb=short",
]

print("=" * 70)
print("R26-T051 check runner")
print("=" * 70)
print(f"Repo root : {REPO_ROOT}")
print(f"Command   : {' '.join(cmd)}")
print("=" * 70)

# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
result = subprocess.run(cmd, cwd=REPO_ROOT)

print("=" * 70)
# Record non-zero test count: pytest's exit code 0 means all passed.
# Any non-zero code means at least one failure.
if result.returncode == 0:
    print("RESULT: All tests PASSED. Exit code: 0")
else:
    print(f"RESULT: Tests FAILED. Exit code: {result.returncode}")
print("=" * 70)

sys.exit(result.returncode)
