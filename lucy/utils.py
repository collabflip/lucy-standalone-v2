"""Utility helpers including a safe subprocess runner."""
from __future__ import annotations

import subprocess
import shlex
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from pathlib import Path

from lucy.contract import CommandResult


def run_subprocess(
    command: List[str] | str,
    cwd: Optional[Path] = None,
    timeout: Optional[float] = 10.0,
    capture_output: bool = True,
    text: bool = True,
) -> CommandResult:
    """Run a subprocess safely with timeout and captured output.

    Returns a CommandResult dataclass with stdout, stderr, exit_code and timed_out flag.
    """
    if isinstance(command, str):
        args = shlex.split(command)
    else:
        args = list(command)

    try:
        proc = subprocess.run(
            args,
            cwd=str(cwd) if cwd is not None else None,
            timeout=timeout,
            capture_output=capture_output,
            text=text,
            check=False,
        )
        stdout = proc.stdout or ""
        stderr = proc.stderr or ""
        exit_code = proc.returncode if proc.returncode is not None else 0
        return CommandResult(
            stdout=stdout,
            stderr=stderr,
            exit_code=exit_code,
            timed_out=False,
            cwd=str(cwd) if cwd is not None else None,
            meta=None,
        )
    except subprocess.TimeoutExpired as e:
        stdout = e.stdout or ""
        stderr = (e.stderr or "") + "\n[timeout]"
        return CommandResult(stdout=stdout, stderr=stderr, exit_code=124, timed_out=True, cwd=str(cwd) if cwd is not None else None)
