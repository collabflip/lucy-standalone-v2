def test_cd_does_not_use_subprocess(monkeypatch, tmp_path):
    """Regression test: dispatching 'cd' must not call the subprocess wrapper."""
    from lucy.dispatcher import Dispatcher
    import lucy.utils as lu

    called = {"used": False}

    def fake_run(*args, **kwargs):
        called["used"] = True
        raise AssertionError("run_subprocess was called during cd")

    monkeypatch.setattr(lu, "run_subprocess", fake_run)

    d = Dispatcher(cwd=tmp_path)
    (tmp_path / "sub").mkdir()
    r = d.dispatch("cd sub")
    assert r.exit_code == 0
    assert not called["used"]
