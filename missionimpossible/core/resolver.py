"""
Universal Stack Resolver with Dynamic YOLO Support
"""
from ..resolvers.yolo_resolver import resolve_yolo_stack
from ..resolvers.framework_resolver import resolve_framework_stack
from ..utils.preset_manager import get_preset

def resolve_universal_stack(
    use_case="research",
    yolo_family="latest",
    gpu=True,
    framework="auto"
):
    """Resolve complete ML research stack"""
    
    # 1. Detect current state
    diagnostics = detect_all_conflicts()
    
    # 2. Generate dynamic preset
    preset = get_preset(use_case)
    
    # 3. Dynamic YOLO integration
    yolo_stack = resolve_yolo_stack(yolo_family, gpu)
    preset.update(yolo_stack)
    
    # 4. Framework auto-resolution
    if framework == "auto":
        framework_stack = resolve_framework_stack(gpu, yolo_stack)
        preset.update(framework_stack)
    
    return {
        "preset": preset,
        "diagnostics": diagnostics,
        "install_command": generate_pip_command(preset),
        "dockerfile": generate_dockerfile(preset)
    }
