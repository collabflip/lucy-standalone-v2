import sys
from lucy.utils import run_subprocess


def test_run_subprocess_basic():
    # use the current python interpreter to print
    res = run_subprocess([sys.executable, "-c", "print('xyz')"], timeout=5)
    assert res.exit_code == 0
    assert "xyz" in res.stdout
