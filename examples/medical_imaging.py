"""
Example: medical imaging + report generation
Uses a research/medical preset resolved by MissionImPossible.
"""

from missionimpossible.resolvers.stack_resolver import resolve_cnn_nlp_stack
from missionimpossible.core.installer import install_stack
from missionimpossible.utils.environment import write_requirements_txt


def main():
    stack = resolve_cnn_nlp_stack(use_case="research", yolo_family="v10", framework="pytorch")
    write_requirements_txt(stack, "requirements_medical.txt")
    install_stack(stack, use_venv=False)

    print("✅ Medical imaging environment ready!")
    # Here you would import MONAI, pydicom etc if added to preset


if __name__ == "__main__":
    main()
