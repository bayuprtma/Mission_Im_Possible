"""
Universal ML Stack Conflict Detector
"""

from __future__ import annotations

from ..detectors.cnn_detector import detect_cnn_conflicts
from ..detectors.nlp_detector import detect_nlp_conflicts
from ..detectors.vision_detector import detect_vision_conflicts
from ..detectors.gpu_detector import detect_gpu_status


def detect_all_conflicts() -> dict:
    """Detect conflicts across all ML domains."""
    return {
        "cnn": detect_cnn_conflicts(),
        "nlp": detect_nlp_conflicts(),
        "vision": detect_vision_conflicts(),
        "gpu": detect_gpu_status(),
        "pip": check_pip_conflicts(),
    }


def check_pip_conflicts() -> dict:
    """Run `pip check` and return whether conflicts exist."""
    import subprocess
    import sys

    result = subprocess.run(
        [sys.executable, "-m", "pip", "check"],
        capture_output=True,
        text=True,
    )
    return {
        "conflicts": result.returncode != 0,
        "details": result.stdout.strip(),
    }
