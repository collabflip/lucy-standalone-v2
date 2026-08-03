from typing import Callable, Dict, Optional, List
from types import SimpleNamespace
from lucy.contract import CommandResult

Handler = Callable[[List[str], Dict], CommandResult]


class CommandRegistry:
    """Registry for deterministic command handlers."""

    def __init__(self) -> None:
        self._handlers: Dict[str, Handler] = {}
        self._deterministic: set[str] = set()

    def register(self, name: str) -> Callable[[Handler], Handler]:
        def _decorator(func: Handler) -> Handler:
            if name in self._handlers:
                raise ValueError(f"handler for {name!r} already registered")
            self._handlers[name] = func
            self._deterministic.add(name)
            return func

        return _decorator

    def get(self, name: str) -> Optional[Handler]:
        return self._handlers.get(name)

    def lookup(self, name: str) -> Optional[SimpleNamespace]:
        """Return registry metadata expected by Dispatcher."""
        handler = self._handlers.get(name)
        if handler is None:
            return None
        return SimpleNamespace(
            handler=handler,
            deterministic=True,
        )

    def is_deterministic(self, name: str) -> bool:
        return name in self._deterministic

    def all_commands(self) -> List[str]:
        return sorted(self._handlers.keys())


# Module-level default registry
default_registry = CommandRegistry()
