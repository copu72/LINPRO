#!/usr/bin/env python
"""Limpiar archivos temporales del proyecto."""

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DIRS_TO_CLEAN = [
    ROOT / ".pytest_cache",
    ROOT / ".coverage",
    ROOT / "htmlcov",
    ROOT / "__pycache__",
]
EXTENSIONS = [".pyc", ".pyo", ".egg-info"]


def main() -> None:
    for d in DIRS_TO_CLEAN:
        if d.is_dir():
            shutil.rmtree(d)
            print(f"  Removed: {d}")
        elif d.is_file():
            d.unlink()
            print(f"  Removed: {d}")

    for ext in EXTENSIONS:
        for f in ROOT.rglob(f"*{ext}"):
            if f.is_file():
                f.unlink()
                print(f"  Removed: {f}")

    for d in ROOT.rglob("__pycache__"):
        if d.is_dir():
            shutil.rmtree(d)
            print(f"  Removed: {d}")

    print("✅ Cleanup complete")


if __name__ == "__main__":
    main()
