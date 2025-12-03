"""
YOLO resolver for MissionImPossible.

- Fetches YOLO (ultralytics) versions from PyPI.
- Supports YOLOv8 / YOLOv10 / YOLOv11 families.
- Picks compatible Torch version (GPU / CPU).
"""

from __future__ import annotations

from typing import Dict, List

from packaging import version

from ..utils.pypi_api import get_pypi_releases


# Default Torch versions we consider "good" for each YOLO family.
YOLO_TORCH_MAP_GPU: Dict[str, str] = {
    "8": "2.1.0",
    "10": "2.2.0",
    "11": "2.3.0",  # future-oriented guess
}

YOLO_TORCH_MAP_CPU: Dict[str, str] = {
    "8": "2.1.0",
    "10": "2.2.0",
    "11": "2.3.0",
}



def resolve_yolo_stack(yolo_family: str = "latest", gpu: bool = True) -> Dict[str, str]:
    """
    Resolve YOLO (ultralytics) and Torch versions.

    Parameters
    ----------
    yolo_family : {"latest","v8","v10","v11"}
        Version family preference. "latest" = auto-detect from PyPI.
    gpu : bool
        Whether to prefer GPU-enabled Torch builds.

    Returns
    -------
    dict
        Minimal stack part, e.g. {"ultralytics": "...", "torch": "..."}.
    """
    releases = get_pypi_releases("ultralytics")
    latest_stable = get_latest_stable_yolo(releases)

    # Decide YOLO constraint
    if yolo_family == "v8":
        yolo_spec = "ultralytics>=8.0.0,<9.0.0"
        family = "8"
    elif yolo_family == "v10":
        yolo_spec = "ultralytics>=10.0.0,<11.0.0"
        family = "10"
    elif yolo_family == "v11":
        yolo_spec = "ultralytics>=11.0.0,<12.0.0"
        family = "11"
    else:  # "latest"
        yolo_spec = f"ultralytics>={latest_stable}"
        family = infer_family_from_version(latest_stable)

    torch_version = get_torch_for_yolo_family(family, gpu)

    return {
        "ultralytics": yolo_spec,
        "torch": torch_version,
    }


def get_latest_stable_yolo(releases: List[str]) -> str:
    """
    Filter out pre-releases and return the highest stable version.
    """
    stable = [
        v for v in releases
        if not any(tag in v.lower() for tag in ("a", "b", "rc", "alpha", "beta"))
    ]
    if not stable:
        # Very defensive fallback
        return "8.2.48"
    return sorted(stable, key=version.parse)[-1]


def infer_family_from_version(ver: str) -> str:
    """
    Infer YOLO family ("8","10","11") from version string.
    """
    major = ver.split(".")[0]
    # YOLOv10 & v11 are effectively "10"/"11" major branches
    if major in {"8", "10", "11"}:
        return major
    # Fallback to 8 if unexpected
    return "8"


def get_torch_for_yolo_family(family: str, gpu: bool) -> str:
    """
    Return a Torch version appropriate for given YOLO family and GPU flag.
    """
    mapping = YOLO_TORCH_MAP_GPU if gpu else YOLO_TORCH_MAP_CPU
    if family in mapping:
        return mapping[family]
    # Fallback to YOLOv8 mapping
    return mapping["8"]

