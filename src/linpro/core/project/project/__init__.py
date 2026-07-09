"""Gestión de proyectos LINPRO.

Project es el objeto central. Todos los módulos leen y escriben sobre él.
Ningún módulo se comunica directamente con otro; todo pasa por Project.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from linpro.core.exceptions import ProjectError, WorkspaceError


@dataclass
class ProjectMetadata:
    name: str
    description: str = ""
    author: str = ""
    company: str = ""
    created: datetime = field(default_factory=datetime.now)
    modified: datetime = field(default_factory=datetime.now)
    version: str = "0.1.0"
    epsg: int = 25830


@dataclass
class ProjectState:
    is_dirty: bool = False
    is_loaded: bool = False
    has_alignment: bool = False
    has_analysis: bool = False
    has_results: bool = False


class Project:
    def __init__(self, name: str = "Sin título") -> None:
        self._metadata = ProjectMetadata(name=name)
        self._state = ProjectState()
        self._path: Optional[Path] = None
        self._data: Dict[str, Any] = {}

    @property
    def metadata(self) -> ProjectMetadata:
        return self._metadata

    @property
    def state(self) -> ProjectState:
        return self._state

    @property
    def path(self) -> Optional[Path]:
        return self._path

    @path.setter
    def path(self, value: Optional[Path]) -> None:
        self._path = value

    def set_data(self, key: str, value: Any) -> None:
        self._data[key] = value
        self._metadata.modified = datetime.now()
        self._state.is_dirty = True

    def get_data(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def mark_loaded(self) -> None:
        self._state.is_loaded = True
        self._state.is_dirty = False

    def mark_saved(self) -> None:
        self._state.is_dirty = False
        self._metadata.modified = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metadata": {
                "name": self._metadata.name,
                "description": self._metadata.description,
                "author": self._metadata.author,
                "company": self._metadata.company,
                "created": self._metadata.created.isoformat(),
                "modified": self._metadata.modified.isoformat(),
                "version": self._metadata.version,
                "epsg": self._metadata.epsg,
            },
            "data": self._data,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Project":
        meta = data.get("metadata", {})
        project = cls(name=meta.get("name", "Sin título"))
        project._metadata.description = meta.get("description", "")
        project._metadata.author = meta.get("author", "")
        project._metadata.company = meta.get("company", "")
        project._metadata.epsg = meta.get("epsg", 25830)
        project._data = data.get("data", {})
        project.mark_loaded()
        return project

    def __repr__(self) -> str:
        return f"Project(name='{self._metadata.name}', dirty={self._state.is_dirty})"


class Workspace:
    _instance: Optional["Workspace"] = None

    def __init__(self) -> None:
        self._current_project: Optional[Project] = None
        self._open_projects: List[Project] = []

    @classmethod
    def get_instance(cls) -> "Workspace":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @property
    def current_project(self) -> Optional[Project]:
        return self._current_project

    def open_project(self, project: Project) -> None:
        self._current_project = project
        if project not in self._open_projects:
            self._open_projects.append(project)
        project.mark_loaded()

    def close_project(self) -> None:
        if self._current_project:
            self._open_projects.remove(self._current_project)
            self._current_project = None

    def list_open_projects(self) -> List[Project]:
        return self._open_projects.copy()