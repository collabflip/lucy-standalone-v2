from lucy.dispatcher import Dispatcher
from lucy.contract import CommandResult
import tempfile
from pathlib import Path


def test_dispatcher_pwd_and_ls(tmp_path: Path):
    # start dispatcher in a temporary directory
    d = Dispatcher(cwd=tmp_path)
    # create a file
    (tmp_path / "a.txt").write_text("hello")
    r = d.dispatch("pwd")
    assert isinstance(r, CommandResult)
    assert r.exit_code == 0
    assert r.stdout.strip() == str(tmp_path)

    r2 = d.dispatch("ls")
    assert r2.exit_code == 0
    assert "a.txt" in r2.stdout


def test_dispatcher_cd_and_touch(tmp_path: Path):
    d = Dispatcher(cwd=tmp_path)
    r = d.dispatch("mkdir sub")
    assert r.exit_code == 0
    r2 = d.dispatch("cd sub")
    assert r2.exit_code == 0
    # touch a file
    r3 = d.dispatch("touch foo.txt")
    assert r3.exit_code == 0
    assert (tmp_path / "sub" / "foo.txt").exists()

