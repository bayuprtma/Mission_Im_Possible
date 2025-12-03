"""
Example: load user-defined custom preset from presets/custom/.
"""

from missionimpossible.utils.preset_manager import get_preset
from missionimpossible.core.installer import install_stack
from missionimpossible.utils.environment import write_conda_env


def main():
    # This refers to [stacks.my_thesis] in presets/custom/my_thesis.toml
    stack = get_preset("my_thesis")
    write_conda_env(stack, "environment_my_thesis.yml")
    install_stack(stack, use_venv=False)

    print("✅ Custom thesis stack ready!")


if __name__ == "__main__":
    main()
