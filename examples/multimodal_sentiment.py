"""
Example: multimodal sentiment (image + text).
"""

from missionimpossible.resolvers.stack_resolver import resolve_cnn_nlp_stack
from missionimpossible.core.installer import install_stack
from missionimpossible.utils.environment import write_environment_toml


def main():
    # Could later add CLIP/BLIP to this preset
    stack = resolve_cnn_nlp_stack(use_case="research", yolo_family="v8", framework="pytorch")
    write_environment_toml(stack, "environment_multimodal.toml")
    install_stack(stack, use_venv=False)

    print("✅ Multimodal sentiment environment ready!")


if __name__ == "__main__":
    main()
