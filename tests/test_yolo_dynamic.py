from missionimpossible.resolvers.yolo_resolver import resolve_yolo_stack


def test_yolo_latest_stack():
    stack = resolve_yolo_stack(yolo_family="latest", gpu=False)
    assert isinstance(stack, dict)
    assert "ultralytics" in stack
    assert "ultralytics" in stack["ultralytics"] or "==" in stack["ultralytics"]


def test_yolo_v8_v10_v11_keywords():
    for fam in ("v8", "v10", "v11"):
        stack = resolve_yolo_stack(yolo_family=fam, gpu=False)
        assert "ultralytics" in stack
