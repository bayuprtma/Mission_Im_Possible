"""
Core subpackage for MissionImPossible.
"""

from __future__ import annotations

from .detector import detect_all_conflicts        # BUKAN .core.detector
from .resolver import resolve_universal_stack
from .installer import install_stack, validate_environment

__all__ = [
    "detect_all_conflicts",
    "resolve_universal_stack",
    "install_stack",
    "validate_environment",
]
