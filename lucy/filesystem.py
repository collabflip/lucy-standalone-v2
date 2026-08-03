"""Basic filesystem command handlers registered into the default registry."""
from __future__ import annotations

from pathlib import Path
from typing import List, Dict
import os
import shutil

from lucy.registry import default_registry
from lucy.contract import CommandResult


@default_registry.register("pwd")
def cmd_pwd(args: List[str], ctx: Dict) -> CommandResult:
    cwd = ctx.get("cwd")
    if isinstance(cwd, Path):
        cwd = cwd
    else:
        cwd = Path(cwd) if cwd is not None else Path.cwd()
    return CommandResult(stdout=str(cwd) + "\n", stderr="", exit_code=0, cwd=str(cwd))


@default_registry.register("ls")
def cmd_ls(args: List[str], ctx: Dict) -> CommandResult:
    cwd = Path(ctx.get("cwd", Path.cwd()))
    target = cwd
    if args:
        target = (cwd / args[0]).resolve()
    try:
        entries = sorted(os.listdir(target))
        out = "\n".join(entries)
        if out:
            out += "\n"
        return CommandResult(stdout=out, stderr="", exit_code=0, cwd=str(cwd))
    except FileNotFoundError as e:
        return CommandResult(stdout="", stderr=str(e) + "\n", exit_code=2, cwd=str(cwd))


@default_registry.register("mkdir")
def cmd_mkdir(args: List[str], ctx: Dict) -> CommandResult:
    cwd = Path(ctx.get("cwd", Path.cwd()))
    if not args:
        return CommandResult(stdout="", stderr="mkdir: missing operand\n", exit_code=2, cwd=str(cwd))
    out = []
    for name in args:
        target = (cwd / name)
        try:
            target.mkdir(parents=True, exist_ok=False)
            out.append("")
        except FileExistsError:
            return CommandResult(stdout="", stderr=f"mkdir: cannot create directory '{name}': File exists\n", exit_code=1, cwd=str(cwd))
    return CommandResult(stdout="".join(out), stderr="", exit_code=0, cwd=str(cwd))


@default_registry.register("touch")
def cmd_touch(args: List[str], ctx: Dict) -> CommandResult:
    cwd = Path(ctx.get("cwd", Path.cwd()))
    if not args:
        return CommandResult(stdout="", stderr="touch: missing file operand\n", exit_code=2, cwd=str(cwd))
    for name in args:
        target = cwd / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.touch(exist_ok=True)
    return CommandResult(stdout="", stderr="", exit_code=0, cwd=str(cwd))


@default_registry.register("cd")
def cmd_cd(args: List[str], ctx: Dict) -> CommandResult:
    cwd = Path(ctx.get("cwd", Path.cwd()))
    target = cwd
    if not args:
        target = Path.home()
    else:
        target = (cwd / args[0]).resolve()
    if not target.exists() or not target.is_dir():
        return CommandResult(stdout="", stderr=f"cd: {args[0]}: No such file or directory\n", exit_code=1, cwd=str(cwd))
    # update context cwd
    ctx["cwd"] = target
    return CommandResult(stdout="", stderr="", exit_code=0, cwd=str(target))


@default_registry.register("cat")
def cmd_cat(args: List[str], ctx: Dict) -> CommandResult:
    cwd = Path(ctx.get("cwd", Path.cwd()))
    if not args:
        return CommandResult(stdout="", stderr="cat: missing file operand\n", exit_code=2, cwd=str(cwd))
    out_parts = []
    for name in args:
        target = (cwd / name)
        if not target.exists():
            return CommandResult(stdout="", stderr=f"cat: {name}: No such file or directory\n", exit_code=1, cwd=str(cwd))
        if target.is_dir():
            return CommandResult(stdout="", stderr=f"cat: {name}: Is a directory\n", exit_code=1, cwd=str(cwd))
        out_parts.append(target.read_text())
    out = "".join(out_parts)
    if out and not out.endswith("\n"):
        out += "\n"
    return CommandResult(stdout=out, stderr="", exit_code=0, cwd=str(cwd))
