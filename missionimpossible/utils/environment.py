"""
Environment utilities for MissionImPossible.

Provides functions to export the resolved ML stack to common environment specification formats:

- requirements.txt (pip)
- environment.toml (simple reproducibility format)
- environment.yml (Conda environment with pip section)
- Dockerfile (minimal Dockerfile to build image with dependencies installed)
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict


def write_requirements_txt(stack: Dict[str, str], path: str = "requirements.txt") -> None:
    """
    Save the stack as a standard pip requirements.txt file.

    If a version specifier contains comparison operators ('>', '<', '=', '~'),
    it is written as-is; otherwise, the exact version is pinned with '=='.
    """
    p = Path(path)
    lines = []
    for name, spec in stack.items():
        spec = str(spec).strip()
        if any(op in spec for op in (">", "<", "=", "~")):
            lines.append(f"{spec}\n")
        else:
            lines.append(f"{name}=={spec}\n")
    p.write_text("".join(lines), encoding="utf-8")


def write_environment_toml(stack: Dict[str, str], path: str = "environment.toml") -> None:
    """
    Export the stack as a simple TOML file for reproducibility.

    Format:

    [packages]
      tensorflow = "2.17.0"
      ultralytics = ">=8.3.234"
    """
    body_lines = [f'  {k} = "{v}"' for k, v in stack.items()]
    content = "[packages]\n" + "\n".join(body_lines) + "\n"
    Path(path).write_text(content, encoding="utf-8")


def write_conda_env(stack: Dict[str, str], path: str = "environment.yml") -> None:
    """
    Export the stack as a Conda environment.yml file with pip section.

    This minimal file includes python and pip, then pip installs all dependencies.
    """
    lines = [
        "name: missionimpossible-env\n",
        "dependencies:\n",
        "  - python\n",
        "  - pip\n",
        "  - pip:\n",
    ]
    for _, spec in stack.items():
        spec = str(spec).strip()
        lines.append(f"    - {spec}\n")
    Path(path).write_text("".join(lines), encoding="utf-8")


def write_dockerfile(stack: Dict[str, str], path: str = "Dockerfile") -> None:
    """
    Generate a minimal Dockerfile that installs the stack via pip.

    Resulting Dockerfile example:

    FROM python:3.11-slim
    WORKDIR /app
    RUN pip install --upgrade pip \
        && pip install pkg1>=1.0 pkg2==2.0 ...
    CMD ["python"]
    """
    pkgs = [str(spec).strip() for spec in stack.values()]
    pkgs_str = " ".join(pkgs) if pkgs else ""

    docker_lines = [
        "FROM python:3.11-slim\n\n",
        "WORKDIR /app\n\n",
        "RUN pip install --upgrade pip \\\n",
        f"    && pip install {pkgs_str}\n\n",
        'CMD ["python"]\n',
    ]

    Path(path).write_text("".join(docker_lines), encoding="utf-8")
