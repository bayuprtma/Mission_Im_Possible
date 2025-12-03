import types

from missionimpossible.detectors import cnn_detector, nlp_detector, vision_detector, gpu_detector


def test_cnn_detector_runs():
    info = cnn_detector.detect_cnn_conflicts()
    assert isinstance(info, dict)
    assert "pip_conflicts" in info


def test_nlp_detector_runs():
    info = nlp_detector.detect_nlp_conflicts()
    assert isinstance(info, dict)
    assert "pip_conflicts" in info


def test_vision_detector_runs():
    info = vision_detector.detect_vision_conflicts()
    assert isinstance(info, dict)
    assert "pip_conflicts" in info


def test_gpu_detector_runs():
    info = gpu_detector.detect_gpu_status()
    assert isinstance(info, dict)
    assert "cuda_version" in info
