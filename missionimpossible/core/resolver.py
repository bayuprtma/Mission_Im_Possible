"""
Universal Stack Resolver with Dynamic YOLO Support
"""

from __future__ import annotations

from .detector import detect_all_conflicts          # <- panggil detector di core
from ..resolvers.yolo_resolver import resolve_yolo_stack
from ..resolvers.framework_resolver import resolve_framework_stack
from ..utils.preset_manager import get_preset
from ..utils.environment import write_dockerfile as generate_dockerfile


def generate_pip_command(stack: dict) -> str:
    """Generate pip install command string from a stack dict."""
    parts = [f"{name}=={ver}" for name, ver in stack.items()]
    return "pip install " + " ".join(parts)


def resolve_universal_stack(
    use_case: str = "research",
    yolo_family: str = "latest",
    gpu: bool = True,
    framework: str = "auto",
) -> dict:
    """Resolve complete ML research stack."""

    # 1. Detect current state
    diagnostics = detect_all_conflicts()

    # 2. Generate dynamic preset
    preset = get_preset(use_case)

    # 3. Dynamic YOLO integration
    yolo_stack = resolve_yolo_stack(yolo_family=yolo_family, gpu=gpu)
    preset.update(yolo_stack)

    # 4. Framework auto-resolution
    if framework == "auto":
        framework_stack = resolve_framework_stack(prefer="auto")
    else:
        framework_stack = resolve_framework_stack(prefer=framework)
    preset.update(framework_stack)

    return {
        "preset": preset,
        "diagnostics": diagnostics,
        "install_command": generate_pip_command(preset),
        "dockerfile": generate_dockerfile(preset),
    }
