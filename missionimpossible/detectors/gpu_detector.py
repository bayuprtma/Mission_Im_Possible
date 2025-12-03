"""
GPU / CUDA detector: basic info about GPU availability and CUDA toolkit.
"""

from __future__ import annotations
import subprocess
from typing import Dict, Any


def detect_gpu_status() -> Dict[str, Any]:
    """
    Detect whether a GPU and CUDA are available.

    Returns
    -------
    dict with keys:
        cuda_version (str|None),
        nvidia_smi_ok (bool),
        tf_gpu_visible (bool|None),
        torch_gpu_visible (bool|None)
    """
    # CUDA / driver via nvidia-smi
    try:
        smi = subprocess.run(
            ["nvidia-smi"],
            capture_output=True,
            text=True,
        )
        nvidia_smi_ok = smi.returncode == 0
        cuda_version = None
        if nvidia_smi_ok:
            for line in smi.stdout.splitlines():
                if "CUDA Version" in line:
                    cuda_version = line.split("CUDA Version")[-1].strip(" :")
                    break
    except FileNotFoundError:
        nvidia_smi_ok = False
        cuda_version = None

    # TensorFlow GPU
    try:
        import tensorflow as tf  # type: ignore
        tf_gpu_visible = bool(tf.config.list_physical_devices("GPU"))
    except Exception:
        tf_gpu_visible = None

    # PyTorch GPU
    try:
        import torch  # type: ignore
        torch_gpu_visible = bool(torch.cuda.is_available())
    except Exception:
        torch_gpu_visible = None

    return {
        "cuda_version": cuda_version,
        "nvidia_smi_ok": nvidia_smi_ok,
        "tf_gpu_visible": tf_gpu_visible,
        "torch_gpu_visible": torch_gpu_visible,
    }
