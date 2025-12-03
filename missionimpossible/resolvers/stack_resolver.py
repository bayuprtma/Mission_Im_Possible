"""
Stack resolver: build full CNN + NLP stack from presets,
framework resolver, and optional YOLO/NLP choices.
"""

from __future__ import annotations
from typing import Dict, Any

from missionimpossible.utils.preset_manager import get_preset
from missionimpossible.resolvers.framework_resolver import resolve_framework_stack
from missionimpossible.resolvers.yolo_resolver import resolve_yolo_stack


def resolve_cnn_nlp_stack(
    use_case: str = "research",
    yolo_family: str = "latest",
    framework: str = "auto",
) -> Dict[str, Any]:
    """
    Build a hybrid CNN + NLP stack.

    Parameters
    ----------
    use_case : str
        Name of preset in presets/*.toml, e.g. "research", "production".
    yolo_family : {"latest","v8","v10","v11"}
        YOLO version family preference.
    framework : {"auto","tensorflow","pytorch"}
        Preferred main DL framework.

    Returns
    -------
    dict : resolved stack, e.g. {"tensorflow": "2.17.0", "ultralytics": "...", "nltk": "..."}
    """
    # 1. Base preset
    stack = get_preset(use_case)

    # 2. Framework
    stack.update(resolve_framework_stack(prefer=framework))

    # 3. YOLO
    stack.update(resolve_yolo_stack(yolo_family=yolo_family))

    return stack
