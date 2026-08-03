"""Entrypoint to run Lucy from the project root."""
from lucy.cli import repl


def main() -> None:
    repl()


if __name__ == "__main__":
    main()
