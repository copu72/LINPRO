"""Sistema de eventos para comunicación entre módulos.

LINPRO usa un bus de eventos para que los módulos se comuniquen
sin conocerse entre sí. El Core publica eventos; los módulos
se suscriben a los que les interesan.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

from linpro.exceptions import EventError

EventHandler = Callable[["Event"], None]


@dataclass
class Event:
    name: str
    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = ""


class EventBus:
    _instance: Optional["EventBus"] = None

    def __init__(self) -> None:
        self._handlers: Dict[str, List[EventHandler]] = {}

    @classmethod
    def get_instance(cls) -> "EventBus":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        self._handlers[event_name].append(handler)

    def unsubscribe(self, event_name: str, handler: EventHandler) -> None:
        if event_name in self._handlers:
            self._handlers[event_name] = [h for h in self._handlers[event_name] if h is not handler]

    def publish(self, event: Event) -> None:
        if event.name not in self._handlers:
            return
        for handler in self._handlers[event.name]:
            try:
                handler(event)
            except Exception as e:
                raise EventError(f"Error en handler para evento '{event.name}': {e}") from e

    def clear(self) -> None:
        self._handlers.clear()


# Eventos estándar del Core
CORE_STARTING = "core.starting"
CORE_STARTED = "core.started"
CORE_STOPPING = "core.stopping"
CORE_STOPPED = "core.stopped"
PROJECT_OPENED = "project.opened"
PROJECT_CLOSED = "project.closed"
PROJECT_SAVED = "project.saved"
PROJECT_MODIFIED = "project.modified"
PLUGIN_LOADED = "plugin.loaded"
PLUGIN_UNLOADED = "plugin.unloaded"
SETTINGS_CHANGED = "settings.changed"
CONFIG_CHANGED = "config.changed"