"""
Thin wrapper around the PyPI JSON API.
"""

from __future__ import annotations
from typing import List
import requests


PYPI_URL = "https://pypi.org/pypi/{name}/json"


def get_pypi_releases(package_name: str) -> List[str]:
    """
    Return list of available versions on PyPI for a package.
    """
    url = PYPI_URL.format(name=package_name)
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return list(data.get("releases", {}).keys())
