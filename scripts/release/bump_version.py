#!/usr/bin/env python
"""Incrementar versión del proyecto."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
VERSION_FILE = ROOT / "src" / "linpro" / "version" / "__init__.py"


def read_version() -> str:
    content = VERSION_FILE.read_text()
    match = re.search(r'__version__\s*=\s*"([^"]+)"', content)
    if not match:
        raise ValueError("Version not found")
    return match.group(1)


def bump(part: str) -> str:
    major, minor, patch = read_version().split(".")
    if part == "major":
        return f"{int(major)+1}.0.0"
    elif part == "minor":
        return f"{major}.{int(minor)+1}.0"
    elif part == "patch":
        return f"{major}.{minor}.{int(patch)+1}"
    else:
        raise ValueError(f"Unknown part: {part}")


def main() -> int:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <major|minor|patch>")
        return 1

    new_version = bump(sys.argv[1])
    content = VERSION_FILE.read_text()
    content = re.sub(r'__version__\s*=\s*"[^"]+"', f'__version__ = "{new_version}"', content)
    VERSION_FILE.write_text(content)
    print(f"✅ Version bumped to {new_version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
