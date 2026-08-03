"""Dispatcher orchestrates command execution using the registry."""
from __future__ import annotations

import shlex
import importlib
from pathlib import Path
from typing import Optional, List, Dict
from types import SimpleNamespace

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

        # Prefer a single registry.lookup(name) API that returns an "entry"
        # object with .handler and .deterministic attributes.
        entry = None

        if hasattr(default_registry, "lookup"):
            try:
                entry = default_registry.lookup(name)
            except Exception:
                # Registry lookup failed — return a deterministic internal error
                # rather than crashing the whole process.
                return CommandResult(
                    stdout="",
                    stderr="Dispatcher configuration error: registry.lookup(name) raised an exception.\n",
                    exit_code=70,
                    cwd=str(self.cwd),
                )
        else:
            # Backwards-compatibility: build a minimal entry from older APIs.
            handler = default_registry.get(name)
            # Discover deterministic flag via preferred call or collection.
            deterministic = False
            if hasattr(default_registry, "is_deterministic"):
                try:
                    deterministic = bool(default_registry.is_deterministic(name))
                except Exception:
                    return CommandResult(
                        stdout="",
                        stderr="Dispatcher configuration error: registry.is_deterministic(name) raised an exception.\n",
                        exit_code=70,
                        cwd=str(self.cwd),
                    )
            elif hasattr(default_registry, "deterministic_commands"):
                try:
                    deterministic = name in getattr(default_registry, "deterministic_commands")
                except Exception:
                    return CommandResult(
                        stdout="",
                        stderr="Dispatcher configuration error: registry.deterministic_commands is malformed.\n",
                        exit_code=70,
                        cwd=str(self.cwd),
                    )
            else:
                # Registry does not expose deterministic metadata — return an
                # internal error so Lucy stays alive and the problem is visible.
                return CommandResult(
                    stdout="",
                    stderr="Dispatcher configuration error: registry does not expose deterministic command metadata.\n",
                    exit_code=70,
                    cwd=str(self.cwd),
                )

            entry = SimpleNamespace(handler=handler, deterministic=deterministic)

        # If registry provided nothing for this name, fall back to subprocess
        # for legacy/non-registered commands.
        if entry is None:
            return run_subprocess(parts, cwd=self.cwd)

        # If a handler exists, run it.
        if getattr(entry, "handler", None) is not None:
            result = entry.handler(args, self.context)

            # allow handlers to modify cwd in context
            cwd = self.context.get("cwd")
            if isinstance(cwd, Path):
                self.cwd = cwd
            elif isinstance(cwd, str):
                self.cwd = Path(cwd)
            return result

        # No handler. If the registry marks this command deterministic, we must
        # not fall back to subprocess — return command-not-found.
        if getattr(entry, "deterministic", False):
            return CommandResult(
                stdout="",
                stderr=f"{name}: command not found\n",
                exit_code=127,
                cwd=str(self.cwd),
            )

        # Non-deterministic / not-protected commands may be run via subprocess.
        return run_subprocess(parts, cwd=self.cwd)
