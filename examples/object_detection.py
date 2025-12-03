"""
Example: generic object detection with YOLO + NLP captions.
"""

from missionimpossible.resolvers.stack_resolver import resolve_cnn_nlp_stack
from missionimpossible.core.installer import install_stack


def main():
    # YOLO + TensorFlow (auto) for CV + basic NLP
    stack = resolve_cnn_nlp_stack(use_case="research", yolo_family="latest", framework="auto")
    install_stack(stack, use_venv=False)

    print("✅ Object detection stack ready!")
    print("Now you can use ultralytics.YOLO + transformers for captioning.")


if __name__ == "__main__":
    main()
