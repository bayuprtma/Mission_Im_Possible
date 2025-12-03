"""
MissionImPossible v0.3.0 - Universal ML Dependency Resolver
Dynamic YOLOv8/v10/v11 + CNN/NLP stack resolution
"""
__version__ = "0.3.0"

from .core.detector import detect_all_conflicts
from .core.resolver import resolve_universal_stack
from .core.installer import install_stack, validate_environment
from .resolvers.yolo_resolver import resolve_yolo_stack

__all__ = [
    "detect_all_conflicts", "resolve_universal_stack", 
    "install_stack", "validate_environment", "resolve_yolo_stack"
]
