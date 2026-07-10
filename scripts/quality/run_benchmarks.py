#!/usr/bin/env python
"""Ejecutar benchmarks del Geometry Engine."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
BENCHMARKS_DIR = ROOT / "benchmarks"


def main() -> int:
    if not list(BENCHMARKS_DIR.glob("*.py")):
        print("No benchmarks found.")
        return 0

    cmd = [sys.executable, "-m", "pytest", str(BENCHMARKS_DIR), "--benchmark-only", "-v"]
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=ROOT)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
