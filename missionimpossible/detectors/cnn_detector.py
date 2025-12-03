"""
CNN stack detector: TensorFlow, PyTorch, YOLO (ultralytics).
"""

from __future__ import annotations
import subprocess
import sys
from typing import Dict, Any


def _pip_show(name: str) -> str | None:
    result = subprocess.run(
        [sys.executable, "-m", "pip", "show", name],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    for line in result.stdout.splitlines():
        if line.lower().startswith("version:"):
            return line.split(":", 1)[1].strip()
    return None


def detect_cnn_conflicts() -> Dict[str, Any]:
    """
    Detect basic information about CNN-related packages.

    Returns
    -------
    dict with keys:
        tensorflow_version, torch_version, yolo_version, pip_conflicts (bool), pip_output (str)
    """
    pip_check = subprocess.run(
        [sys.executable, "-m", "pip", "check"],
        capture_output=True,
        text=True,
    )

    info = {
        "tensorflow_version": _pip_show("tensorflow"),
        "torch_version": _pip_show("torch"),
        "yolo_version": _pip_show("ultralytics"),
        "pip_conflicts": pip_check.returncode != 0,
        "pip_output": pip_check.stdout.strip(),
    }
    return info
