"""Dispatcher orchestrates command execution using the registry."""
from __future__ import annotations

import shlex
import importlib
from pathlib import Path
from typing import Optional, List, Dict

from lucy.registry import default_registry
from lucy.contract import CommandResult
from lucy.utils import run_subprocess


class Dispatcher:
    def __init__(self, cwd: Optional[Path] = None) -> None:
        # sandbox to repository root
        # Resolve cwd relative to repository root if provided as str
        self.repo_root = Path.cwd()
        self.cwd = Path(cwd) if cwd is not None else Path.cwd()
        if not self.cwd.is_absolute():
            self.cwd = (Path.cwd() / self.cwd).resolve()
        # Enforce sandbox
        try:
            self.cwd = self.cwd.resolve()
        except Exception:
            self.cwd = Path.cwd()

        # Ensure deterministic command handlers are imported and registered
        # Import filesystem and git handlers so they self-register with the registry
        try:
            importlib.import_module("lucy.filesystem")
        except Exception:
            # best-effort: handlers may be missing in some environments
            pass
        try:
            importlib.import_module("lucy.gittools")
        except Exception:
            pass

        # simple environment/context passed to handlers
        self.context: Dict = {"cwd": self.cwd, "repo_root": self.repo_root}

    def dispatch(self, command_line: str) -> CommandResult:
        command_line = command_line.strip()
        if not command_line:
            return CommandResult(stdout="", stderr="", exit_code=0, cwd=str(self.cwd))

        parts = shlex.split(command_line)
        name = parts[0]
        args = parts[1:]

        handler = default_registry.get(name)
        if handler is not None:
            # call handler with args and mutable context
            result = handler(args, self.context)
            # allow handlers to modify cwd in context
            cwd = self.context.get("cwd")
            if isinstance(cwd, Path):
                self.cwd = cwd
            elif isinstance(cwd, str):
                self.cwd = Path(cwd)
            return result

        # deterministic builtins not found: fallback to subprocess
        # Use run_subprocess in the dispatcher's cwd
        return run_subprocess(parts, cwd=self.cwd)
