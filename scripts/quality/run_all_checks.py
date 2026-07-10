#!/usr/bin/env python
"""Ejecutar todas las herramientas de calidad antes de commitar."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def run(cmd: list[str], name: str) -> bool:
    print(f"\n{'='*60}")
    print(f"  {name}...")
    print(f"{'='*60}")
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        print(f"  ❌ {name} FAILED")
        return False
    print(f"  ✅ {name} passed")
    return True


def main() -> int:
    checks = [
        (["ruff", "check", "src/"], "Ruff lint"),
        (["ruff", "format", "--check", "src/"], "Ruff format"),
        (["mypy", "src/linpro/geometry/"], "Mypy type check"),
    ]
    failures = 0
    for cmd, name in checks:
        if not run(cmd, name):
            failures += 1

    if failures:
        print(f"\n❌ {failures} check(s) failed")
        return 1
    print("\n✅ All quality checks passed!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
