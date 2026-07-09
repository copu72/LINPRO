"""Sistema de versionado de LINPRO.

Proporciona información de versión del programa. La versión sigue
semver (MAJOR.MINOR.PATCH).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from linpro.exceptions import VersionError


VERSION_MAJOR = 0
VERSION_MINOR = 1
VERSION_PATCH = 0
VERSION_SUFFIX = ""  # Ej: "alpha", "beta", "rc1"

VERSION_STRING = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}{VERSION_SUFFIX}"
VERSION_TUPLE = (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)

APP_NAME = "LINPRO Professional"
APP_DESCRIPTION = "Ingeniería Lineal Profesional"
COPYRIGHT = f"Copyright (c) {2026} LINPRO Team"
LICENSE_TYPE = "MIT"


@dataclass
class VersionInfo:
    major: int
    minor: int
    patch: int
    suffix: str = ""
    string: str = ""

    def __post_init__(self) -> None:
        if not self.string:
            self.string = f"{self.major}.{self.minor}.{self.patch}{self.suffix}"


def get_version() -> VersionInfo:
    return VersionInfo(
        major=VERSION_MAJOR,
        minor=VERSION_MINOR,
        patch=VERSION_PATCH,
        suffix=VERSION_SUFFIX,
        string=VERSION_STRING,
    )


def get_version_info() -> str:
    return f"{APP_NAME} v{VERSION_STRING}"


def compare_versions(v1: str, v2: str) -> int:
    """Compara dos versiones. Devuelve -1, 0 ó 1."""
    try:
        parts1 = [int(x) for x in v1.split(".")[:3]]
        parts2 = [int(x) for x in v2.split(".")[:3]]
        for a, b in zip(parts1, parts2):
            if a < b:
                return -1
            if a > b:
                return 1
        return 0
    except (ValueError, IndexError) as e:
        raise VersionError(f"Formato de versión inválido: {v1}, {v2}") from e