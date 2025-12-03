"""
Installer utilities for MissionImPossible.

- Creates (optional) virtual environment
- Runs pip install for a resolved stack
- Validates imports after installation
"""

from __future__ import annotations
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional


def run(cmd: List[str], env: Optional[Dict[str, str]] = None) -> int:
    """Run a shell command and stream output."""
    return subprocess.call(cmd, env=env or None)


def install_stack(
    stack: Dict[str, str],
    use_venv: bool = False,
    venv_path: str = ".missionimpossible-env",
) -> None:
    """
    Install a resolved stack of packages.

    Parameters
    ----------
    stack : dict
        Mapping {package_name: version_spec}, e.g. {"tensorflow": "2.17.0"}.
    use_venv : bool
        Whether to create and use a dedicated virtual environment.
    venv_path : str
        Path to the virtual environment directory.
    """
    python_exe = sys.executable

    if use_venv:
        venv_dir = Path(venv_path)
        if not venv_dir.exists():
            print(f"[MissionImPossible] Creating virtualenv at {venv_dir} ...")
            run([python_exe, "-m", "venv", str(venv_dir)])

        # select Python inside venv
        if sys.platform.startswith("win"):
            python_exe = str(venv_dir / "Scripts" / "python.exe")
        else:
            python_exe = str(venv_dir / "bin" / "python")

    # build pip install command
    pkgs = [f"{name}=={ver}" for name, ver in stack.items()]
    cmd = [python_exe, "-m", "pip", "install"] + pkgs
    print("[MissionImPossible] Installing:", " ".join(pkgs))
    code = run(cmd)
    if code != 0:
        raise RuntimeError("Installation failed, see pip output above.")

    # basic validation
    validate_environment(list(stack.keys()), python_exe)


def validate_environment(packages: List[str], python_exe: Optional[str] = None) -> None:
    """
    Try importing every package to ensure environment is consistent.
    """
    python_exe = python_exe or sys.executable
    print("[MissionImPossible] Validating imports ...")
    for pkg in packages:
        # ambil nama modul (tanpa tanda -)
        mod_name = pkg.split("-")[0].replace("-", "_")
        code = run([python_exe, "-c", f"import {mod_name}"])
        if code != 0:
            print(f"[MissionImPossible] WARNING: Failed to import '{mod_name}'.")
        else:
            print(f"[MissionImPossible] OK: {mod_name}")
    print("[MissionImPossible] Validation finished.")


