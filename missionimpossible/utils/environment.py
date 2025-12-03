"""
Environment utilities: export resolved stacks to various formats.

- requirements.txt
- environment.toml
- Conda environment.yml (pip section)
- Dockerfile (minimal)
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict


def write_requirements_txt(stack: Dict[str, str], path: str = "requirements.txt") -> None:
    """
    Save stack as a standard requirements.txt file.

    Jika value sudah mengandung operator versi (>, <, =, ~),
    maka ditulis apa adanya. Kalau tidak, akan dibuat "name==version".
    """
    p = Path(path)
    lines = []
    for name, spec in stack.items():
        spec = str(spec).strip()
        if any(op in spec for op in (">", "<", "=", "~")):
            # Sudah berupa spec lengkap, contoh: "ultralytics>=8.3.234"
            line = f"{spec}\n"
        else:
            # Hanya angka versi, contoh: "2.17.0"
            line = f"{name}=={spec}\n"
        lines.append(line)

    p.write_text("".join(lines), encoding="utf-8")


def write_environment_toml(stack: Dict[str, str], path: str = "environment.toml") -> None:
    """
    Export stack to a simple TOML file:

    [packages]
      tensorflow = "2.17.0"
      ultralytics = ">=8.3.234"
    """
    body_lines = [f'  {k} = "{v}"' for k, v in stack.items()]
    content = "[packages]\n" + "\n".join(body_lines) + "\n"
    Path(path).write_text(content, encoding="utf-8")


def write_conda_env(stack: Dict[str, str], path: str = "environment.yml") -> None:
    """
    Export stack as a minimal Conda environment.yml using pip section.
    """
    lines = [
        "name: missionimpossible-env\n",
        "dependencies:\n",
        "  - python\n",
        "  - pip\n",
        "  - pip:\n",
    ]
    for name, spec in stack.items():
        spec = str(spec).strip()
        if any(op in spec for op in (">", "<", "=", "~")):
            lines.append(f"    - {spec}\n")
        else:
            lines.append(f"    - {name}=={spec}\n")

    Path(path).write_text("".join(lines), encoding="utf-8")


def write_dockerfile(stack: Dict[str, str], path: str = "Dockerfile") -> None:
    """
    Generate a minimal Dockerfile that installs the resolved stack with pip.

    FROM python:3.11-slim
    WORKDIR /app
    RUN pip install --upgrade pip \
        && pip install <all packages>
    CMD ["python"]
    """
    # Susun daftar constraint seperti di requirements.txt
    pkgs: list[str] = []
    for name, spec in stack.items():
        spec = str(spec).strip()
        if any(op in spec for op in (">", "<", "=", "~")):
            pkgs.append(spec)
        else:
            pkgs.append(f"{name}=={spec}")

    pkgs_str = " ".join(pkgs) if pkgs else ""

    docker_lines = [
        "FROM python:3.11-slim\n",
        "\n",
        "WORKDIR /app\n",
        "\n",
        "RUN pip install --upgrade pip \\\n",
        f"    && pip install {pkgs_str}\n",
        "\n",
        'CMD ["python"]\n',
    ]

    Path(path).write_text("".join(docker_lines), encoding="utf-8")
