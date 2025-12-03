"""
Preset manager: load and manage stack presets from presets/*.toml.
"""

from __future__ import annotations
from pathlib import Path
from typing import Dict, Any

import tomllib  # Python 3.11+; untuk 3.9/3.10 pakai 'tomli' dan import berbeda


PRESETS_DIR = Path(__file__).resolve().parents[2] / "presets"


def _load_toml(path: Path) -> Dict[str, Any]:
    with path.open("rb") as f:
        return tomllib.load(f)


def get_preset(name: str) -> Dict[str, str]:
    """
    Load a preset stack by name.

    Looks into:
      presets/research.toml
      presets/production.toml
      presets/lightweight.toml
    and expects a table [stacks.<name>].

    Example:
      [stacks.research]
      tensorflow = "2.17.0"
      nltk = "3.8.1"
    """
    for file in PRESETS_DIR.glob("*.toml"):
        data = _load_toml(file)
        stacks = data.get("stacks", {})
        if name in stacks:
            raw = stacks[name]
            # cast all values to str
            return {k: str(v) for k, v in raw.items()}
    raise KeyError(f"Preset '{name}' not found in {PRESETS_DIR}")


def list_presets() -> Dict[str, Path]:
    """
    List available preset names and source files.
    """
    mapping: Dict[str, Path] = {}
    for file in PRESETS_DIR.glob("*.toml"):
        data = _load_toml(file)
        stacks = data.get("stacks", {})
        for name in stacks:
            mapping[name] = file
    return mapping
