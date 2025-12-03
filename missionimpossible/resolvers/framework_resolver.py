"""
Framework resolver: choose compatible TensorFlow / PyTorch versions
based on GPU availability and (optionally) detected CUDA version.
"""

from __future__ import annotations
from typing import Dict, Any

from missionimpossible.detectors.gpu_detector import detect_gpu_status

# Very rough, simple mappings (bisa kamu perhalus nanti)
TF_CUDA_MAP = {
    "2.15.0": "12.2",
    "2.17.0": "12.3",
    "2.18.0": "12.4",
}

TORCH_CUDA_MAP = {
    "2.1.0+cu121": "12.1",
    "2.2.0+cu122": "12.2",
    "2.3.0+cu124": "12.4",
}


def _best_match(cuda_version: str | None, mapping: Dict[str, str]) -> str:
    """Pick first framework version whose CUDA requirement is <= detected."""
    if not cuda_version:
        # CPU-only fallback
        # Return first key but without CUDA suffix
        first = next(iter(mapping))
        return first.split("+")[0]

    for fw_ver, required_cuda in mapping.items():
        if cuda_version.startswith(required_cuda[:3]):
            return fw_ver
    # fallback: first entry
    return next(iter(mapping))


def resolve_framework_stack(
    prefer: str = "auto",
) -> Dict[str, str]:
    """
    Decide which framework versions to use.

    Parameters
    ----------
    prefer : {"auto","tensorflow","pytorch"}
        Preferred framework family.

    Returns
    -------
    dict : minimal framework part of the stack, e.g.
        {"tensorflow": "2.17.0"} or {"torch": "2.1.0+cu121"}.
    """
    gpu_info: Any = detect_gpu_status()
    cuda_version = gpu_info.get("cuda_version")

    if prefer == "tensorflow":
        tf_ver = _best_match(cuda_version, TF_CUDA_MAP)
        return {"tensorflow": tf_ver}
    if prefer == "pytorch":
        torch_ver = _best_match(cuda_version, TORCH_CUDA_MAP)
        return {"torch": torch_ver}

    # auto: prefer GPU, then TF by default
    if gpu_info.get("torch_gpu_visible"):
        torch_ver = _best_match(cuda_version, TORCH_CUDA_MAP)
        return {"torch": torch_ver}
    tf_ver = _best_match(cuda_version, TF_CUDA_MAP)
    return {"tensorflow": tf_ver}
