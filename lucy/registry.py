from typing import Callable, Dict, Optional, List
from pathlib import Path
from lucy.contract import CommandResult

Handler = Callable[[List[str], Dict], CommandResult]


class CommandRegistry:
    """Registry for command handlers.

    Handlers are registered with a command name and are responsible for
    executing the command deterministically when possible.
    """

    def __init__(self) -> None:
        self._handlers: Dict[str, Handler] = {}

    def register(self, name: str) -> Callable[[Handler], Handler]:
        def _decorator(func: Handler) -> Handler:
            if name in self._handlers:
                raise ValueError(f"handler for {name!r} already registered")
            self._handlers[name] = func
            return func

        return _decorator

    def get(self, name: str) -> Optional[Handler]:
        return self._handlers.get(name)

    def all_commands(self) -> List[str]:
        return sorted(list(self._handlers.keys()))


# Module-level default registry
default_registry = CommandRegistry()
