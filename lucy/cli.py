"""Minimal CLI for Lucy."""
from __future__ import annotations

from lucy.dispatcher import Dispatcher


def repl() -> None:
    d = Dispatcher()
    try:
        while True:
            prompt = "Lucy> "
            line = input(prompt)
            if line.strip() in ("exit", "quit"):
                print("bye")
                break
            result = d.dispatch(line)
            # deterministic JSON-like output for now
            print(result.stdout, end="")
            if result.stderr:
                print(result.stderr, end="")
    except (EOFError, KeyboardInterrupt):
        print()
        print("exiting")


if __name__ == "__main__":
    repl()
