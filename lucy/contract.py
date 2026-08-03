from dataclasses import dataclass
from typing import Optional, Any


@dataclass(frozen=True)
class CommandResult:
    stdout: str
    stderr: str
    exit_code: int
    timed_out: bool = False
    cwd: Optional[str] = None
    meta: Optional[Any] = None

    def to_dict(self) -> dict:
        return {
            "stdout": self.stdout,
            "stderr": self.stderr,
            "exit_code": self.exit_code,
            "timed_out": self.timed_out,
            "cwd": self.cwd,
            "meta": self.meta,
        }
