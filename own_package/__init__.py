import toml
import os


def get_version():
    pyproject_path = os.path.join(os.path.dirname(__file__), "..", "pyproject.toml")
    with open(pyproject_path, "r") as f:
        data = toml.load(f)
    return data["project"]["version"]


__version__ = get_version()


def print_version():

    print(f"own_package version: {__version__}")
