"""
Computer Vision detector: OpenCV, Albumentations, Segment-Anything.
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


def detect_vision_conflicts() -> Dict[str, Any]:
    """
    Inspect main CV libraries.

    Returns
    -------
    dict with keys:
        opencv_version, albumentations_version, sam_version,
        pip_conflicts (bool), pip_output (str)
    """
    pip_check = subprocess.run(
        [sys.executable, "-m", "pip", "check"],
        capture_output=True,
        text=True,
    )

    info = {
        "opencv_version": _pip_show("opencv-python"),
        "albumentations_version": _pip_show("albumentations"),
        "sam_version": _pip_show("segment-anything"),
        "pip_conflicts": pip_check.returncode != 0,
        "pip_output": pip_check.stdout.strip(),
    }
    return info
