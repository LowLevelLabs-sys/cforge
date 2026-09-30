from pathlib import Path
import tomllib
from .blueprint import create_project_from_blueprint

"""Load toml data from file"""
TOML_PATH = Path(__file__).parent / ".." / "pyproject.toml"
with open(TOML_PATH, "rb") as f:
    TOML_DATA = tomllib.load(f)


def create_project(name=".", build_tool=None, template=None):
    current_path = Path().cwd() / name
    project_name = Path(name).name if name != "." else Path().cwd().name

    selected_build = (
        build_tool or TOML_DATA.get("build", {}).get("build-tool", "Makefile")
    )
    selected_template = template or "basic"

    return create_project_from_blueprint(
        project_name=project_name,
        template_name=selected_template,
        build=selected_build,
        target_dir=current_path,
        verbose=True,
    )
