import shutil
from pathlib import Path
import tomllib

"""Load toml data from file"""
TOML_PATH = Path(__file__).parent / ".." / "pyproject.toml"
with open(TOML_PATH, "rb") as f:
    TOML_DATA = tomllib.load(f)

TOOL_PATH = Path(__file__).parent / ".." / "template"


def create_project(name=".", build_tool=None, template=None):
    current_path = Path().cwd() / name

    if template is not None:
        print("generate template!")
        shutil.copytree(
            TOOL_PATH / template,
            current_path,
            dirs_exist_ok=True,
        )
    else:
        build_tools = ["Makefile", "build.ninja"]
        # select tool from .toml if build_tool argument is None
        selected = (
            TOML_DATA["build"]["build-tool"] if build_tool is None else build_tool
        )
        # selected = build_tools or TOML_DATA["build"]["build_tool"]

        # append tool that is not in the selected (ignore the un-selected tool)
        ignored = [tool for tool in build_tools if tool.lower() != selected.lower()]
        shutil.copytree(
            TOOL_PATH / "basic",
            current_path,
            ignore=shutil.ignore_patterns(*ignored),
            dirs_exist_ok=True,
        )
