#!/usr/bin/env python
"""Ejecutar tests con cobertura."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def main() -> int:
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "tests/unit/geometry/",
        "--cov=linpro.geometry",
        "--cov-report=term-missing",
        "--cov-fail-under=95",
        "-v",
    ]
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=ROOT)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
