from types import SimpleNamespace
from pathlib import Path
import pytest

from lucy.dispatcher import Dispatcher
from lucy.contract import CommandResult
from lucy.registry import default_registry


def test_dispatch_empty_returns_ok():
    d = Dispatcher()
    r = d.dispatch("")
    assert isinstance(r, CommandResult)
    assert r.exit_code == 0


def test_dispatch_uses_registered_handler_pwd(tmp_path: Path):
    d = Dispatcher(cwd=tmp_path)
    # Ensure filesystem handlers registered by import
    handler = default_registry.get("pwd")
    assert handler is not None
    r = d.dispatch("pwd")
    assert r.exit_code == 0
    assert r.stdout.strip() == str(tmp_path)


def test_dispatch_missing_deterministic_command_is_blocked(monkeypatch):
    # Make registry.lookup report the command is deterministic but has no handler
    monkeypatch.setattr(default_registry, "lookup", lambda name: SimpleNamespace(handler=None, deterministic=True))

    # Ensure run_subprocess is not called
    def _fail_run(parts, cwd):
        raise AssertionError("run_subprocess should not be called for deterministic commands")

    monkeypatch.setattr("lucy.dispatcher.run_subprocess", _fail_run)

    d = Dispatcher()
    r = d.dispatch("head somefile")
    assert r.exit_code == 127
    assert r.stderr == "head: command not found\n"


def test_dispatch_non_deterministic_falls_to_subprocess(monkeypatch, tmp_path: Path):
    # registry.lookup says non-deterministic and no handler
    monkeypatch.setattr(default_registry, "lookup", lambda name: SimpleNamespace(handler=None, deterministic=False))

    def _fake_run(parts, cwd):
        return CommandResult(stdout="ok\n", stderr="", exit_code=0, cwd=str(cwd))

    monkeypatch.setattr("lucy.dispatcher.run_subprocess", _fake_run)

    d = Dispatcher(cwd=tmp_path)
    r = d.dispatch("echo ok")
    assert r.exit_code == 0
    assert r.stdout == "ok\n"


def test_registry_lookup_exception_returns_internal_error(monkeypatch):
    def _boom(name):
        raise Exception("boom")

    monkeypatch.setattr(default_registry, "lookup", _boom)
    d = Dispatcher()
    r = d.dispatch("anycmd")
    assert r.exit_code == 70
    assert "Dispatcher configuration error" in r.stderr


def test_cd_never_uses_subprocess(monkeypatch, tmp_path: Path):
    sub = tmp_path / "sub"
    sub.mkdir()

    # registry.lookup should mark cd as deterministic with a handler (or handler exists in registry)
    # For this test we'll provide a handler that performs cd behavior
    def cd_handler(args, context):
        # emulate handler changing cwd in context
        new = context["cwd"] / args[0]
        context["cwd"] = new
        return CommandResult(stdout="", stderr="", exit_code=0, cwd=str(new))

    monkeypatch.setattr(default_registry, "lookup", lambda name: SimpleNamespace(handler=cd_handler, deterministic=True))

    def _fail_run(parts, cwd):
        raise AssertionError("run_subprocess should not be called for cd")

    monkeypatch.setattr("lucy.dispatcher.run_subprocess", _fail_run)

    d = Dispatcher(cwd=tmp_path)
    r = d.dispatch("cd sub")
    assert r.exit_code == 0
    # ensure cwd updated
    assert d.cwd == sub
