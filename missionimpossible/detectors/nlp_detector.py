"""
NLP stack detector: NLTK, Transformers, spaCy.
"""

from __future__ import annotations
import subprocess
import sys
from typing import Dict, Any


def _pip_show(name: str) -> str | None:
    result = subprocess.run(
        [sys.executable, "-m", "pip", "show", name],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    for line in result.stdout.splitlines():
        if line.lower().startswith("version:"):
            return line.split(":", 1)[1].strip()
    return None


def detect_nlp_conflicts() -> Dict[str, Any]:
    """
    Collect versions and pip conflict status for common NLP libraries.

    Returns
    -------
    dict with keys:
        nltk_version, transformers_version, spacy_version,
        pip_conflicts (bool), pip_output (str)
    """
    pip_check = subprocess.run(
        [sys.executable, "-m", "pip", "check"],
        capture_output=True,
        text=True,
    )

    info = {
        "nltk_version": _pip_show("nltk"),
        "transformers_version": _pip_show("transformers"),
        "spacy_version": _pip_show("spacy"),
        "pip_conflicts": pip_check.returncode != 0,
        "pip_output": pip_check.stdout.strip(),
    }
    return info
