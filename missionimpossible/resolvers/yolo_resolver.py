"""
Dynamic YOLO Resolver - v8/v10/v11 auto-detection
"""
import requests
from packaging import version
from ..utils.pypi_api import get_pypi_releases

def resolve_yolo_stack(yolo_family="latest", gpu=True):
    """Dynamic YOLO version resolution"""
    releases = get_pypi_releases("ultralytics")
    latest_stable = get_latest_stable_yolo(releases)
    
    if yolo_family == "latest":
        yolo_version = f"ultralytics>={latest_stable}"
    elif yolo_family == "v11":
        yolo_version = f"ultralytics>=11.0.0,<12.0.0"
    elif yolo_family == "v10":
        yolo_version = f"ultralytics>=10.0.0,<11.0.0"
    else:
        yolo_version = "ultralytics==8.2.48"
    
    # Map to framework dependencies
    stack = {
        "ultralytics": yolo_version,
        **get_framework_for_yolo(latest_stable, gpu)
    }
    return stack

def get_latest_stable_yolo(releases):
    """Filter stable releases from PyPI"""
    stable = [v for v in releases if not any(x in v.lower() for x in ['a','b','rc','alpha','beta'])]
    return sorted(stable, key=version.parse)[-1]
