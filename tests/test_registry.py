import sys
import tempfile
from lucy.registry import CommandRegistry
from lucy.registry import default_registry


def test_registry_register_and_get():
    r = CommandRegistry()

    @r.register("hello")
    def _hello(args, ctx):
        """Simple handler for tests"""
        from lucy.contract import CommandResult

        return CommandResult(stdout="ok\n", stderr="", exit_code=0, cwd=str(ctx.get("cwd")))

    assert "hello" in r.all_commands()
    h = r.get("hello")
    assert h is not None
    res = h([], {"cwd": tempfile.gettempdir()})
    assert res.stdout.strip() == "ok"
