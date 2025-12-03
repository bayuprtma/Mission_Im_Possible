"""
Environment utilities: export resolved stacks to various formats.
"""

from __future__ import annotations
from pathlib import Path
from typing import Dict


def write_requirements_txt(stack: Dict[str, str], path: str = "requirements.txt") -> None:
    """Save stack as requirements.txt."""
    p = Path(path)
    lines = [f"{name}=={ver}\n" for name, ver in stack.items()]
    p.write_text("".join(lines), encoding="utf-8")


def write_environment_toml(stack: Dict[str, str], path: str = "environment.toml") -> None:
    """Simple TOML export for reproducibility."""
    from textwrap import indent

    body = "\n".join(f'{k} = "{v}"' for k, v in stack.items())
    content = "[packages]\n" + indent(body, "  ")
    Path(path).write_text(content, encoding="utf-8")


def write_conda_env(stack: Dict[str, str], path: str = "environment.yml") -> None:
    """Very simple conda env writer (pip section)."""
    lines = [
        "name: missionimpossible-env\n",
        "dependencies:\n",
        "  - python\n",
        "  - pip\n",
        "  - pip:\n",
    ]
    for name, ver in stack.items():
        lines.append(f"    - {name}=={ver}\n")
    Path(path).write_text("".join(lines), encoding="utf-8")


def write_dockerfile(stack: Dict[str, str], path: str = "Dockerfile") -> None:
    """Generate a minimal Dockerfile that installs the stack with pip."""
    from textwrap import indent

    req_lines = "\n".join(f"{name}=={ver}" for name, ver in stack.items())
    docker = f"""FROM python:3.11-slim

WORKDIR /app

RUN pip install --upgrade pip \\
    && pip install \\
{indent('\\n'.join(f'{n}=={v} \\\\' for n, v in stack.items()), '       ')} 
    && rm -rf /root/.cache/pip

CMD ["python"]
"""
    Path(path).write_text(docker, encoding="utf-8")
