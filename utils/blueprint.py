import sys
from pathlib import Path
from string import Template


def _get_check_mark() -> str:
    """Return [✓] if stdout encoding supports it, else [+] fallback."""
    try:
        "✓".encode(sys.stdout.encoding or "ascii")
        return "[✓]"
    except Exception:
        return "[+]"


# =============================================================================
# Templates
# =============================================================================

main = """#include <stdio.h>

int main(int argc, char *argv[]) {
    (void)argc;
    (void)argv;
    printf("Hello, this is ${project_name}!\\n");

    return 0;
}
"""

LIB_H = """#ifndef ${guard}_H
#define ${guard}_H

void hello(void);

#endif // ${guard}_H
"""

LIB_C = """#include <stdio.h>
#include "lib.h"

void hello(void) {
    printf("Hello from library!\\n");
}
"""

MAKEFILE = """CC ?= clang
CFLAGS ?= -Wall -Wextra -Wpedantic -std=c11 -Iinclude
LDFLAGS ?=

SRC_DIR := src
BUILD_DIR := build
TARGET := $(BUILD_DIR)/${project_name}

SRCS := $(wildcard $(SRC_DIR)/*.c)
OBJS := $(patsubst $(SRC_DIR)/%.c,$(BUILD_DIR)/%.o,$(SRCS))

# Deteksi sistem operasi
ifeq ($(OS),Windows_NT)
    TARGET := $(TARGET).exe
    ifeq ($(SHELL),sh.exe)
        MKDIR = mkdir -p $(BUILD_DIR)
        RM = rm -rf $(BUILD_DIR)
    else ifeq ($(findstring /sh,$(SHELL)),/sh)
        MKDIR = mkdir -p $(BUILD_DIR)
        RM = rm -rf $(BUILD_DIR)
    else
        MKDIR = if not exist $(BUILD_DIR) mkdir $(BUILD_DIR)
        RM = if exist $(BUILD_DIR) rmdir /s /q $(BUILD_DIR)
    endif
else
    MKDIR = mkdir -p $(BUILD_DIR)
    RM = rm -rf $(BUILD_DIR)
endif

.PHONY: all run clean

all: $(TARGET)

$(TARGET): $(OBJS)
\t@$(MKDIR)
\t$(CC) $(OBJS) -o $@ $(LDFLAGS)

$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c
\t@$(MKDIR)
\t$(CC) $(CFLAGS) -c $< -o $@

run: $(TARGET)
\t@$(TARGET)

clean:
\t@$(RM)
"""

BUILD_NINJA = """builddir = build
cc = clang
cflags = -Wall -Wextra -Wpedantic -std=c11 -Iinclude
ldflags =

rule cc
  command = $cc -MD -MF $out.d $cflags -c $in -o $out
  depfile = $out.d
  deps = gcc
  description = CC $in

rule link
  command = $cc $in -o $out $ldflags
  description = LINK $out

build $builddir/${project_name}.o: cc src/main.c
build $builddir/${project_name}.exe: link $builddir/${project_name}.o
build $builddir/${project_name}: link $builddir/${project_name}.o

default $builddir/${project_name}
"""

CMAKELISTS = """cmake_minimum_required(VERSION 3.16)

project(${project_name} C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

include_directories(include)

file(GLOB_RECURSE SOURCES "src/*.c")

add_executable(${project_name} $${SOURCES})
"""

README_MD = """# ${project_name}

A clean C project generated with cforge.

## Project Structure

```text
├── include/     # Header files (.h)
├── src/         # Source files (.c)
├── Makefile     # Build configuration
└── README.md
```

## How to Build and Run

### Using Make:
```bash
make
make run
```

To clean the build directory:
```bash
make clean
```
"""

GITIGNORE = """# Object and dependency files
*.o
*.obj
*.d

# Build outputs
build/
bin/
*.exe
*.out

# Ninja logs
.ninja_log
.ninja_deps

# IDEs & Editor configs
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
"""

# Raylib Templates
RAYLIB_MAIN_C = """#include "raylib.h"

int main(void)
{
    InitWindow(800, 450, "${project_name}");

    SetTargetFPS(60);

    while (!WindowShouldClose())
    {
        BeginDrawing();

        ClearBackground(RAYWHITE);

        DrawText("Hello, raylib!", 300, 200, 30, BLACK);

        EndDrawing();
    }

    CloseWindow();

    return 0;
}
"""

RAYLIB_CMAKELISTS = """cmake_minimum_required(VERSION 3.16)

project(${project_name} C)

set(CMAKE_C_STANDARD 17)
set(CMAKE_C_STANDARD_REQUIRED ON)

find_package(raylib CONFIG REQUIRED)

add_executable($${PROJECT_NAME}
    src/main.c
)

target_link_libraries($${PROJECT_NAME}
    PRIVATE raylib
)
"""

RAYLIB_VCPKG_JSON = """{
    "name": "${project_name}",
    "version-string": "0.1.0",
    "dependencies": [
        "raylib"
    ]
}
"""

RAYLIB_README = """# ${project_name}

A raylib C project generated with cforge.

## Build Instructions (CMake + vcpkg)

```bash
cmake -B build -S .
cmake --build build
```
"""

# =============================================================================
# Blueprints & Mappings
# =============================================================================

BUILD_TEMPLATES = {
    "Makefile": Template(MAKEFILE),
    "build.ninja": Template(BUILD_NINJA),
    "CMakeLists.txt": Template(CMAKELISTS),
}

project_structure = {
    "name": "basic",
    "include": {},
    "src": {"main.c": Template(main)},
    "build": ["Makefile", "build.ninja", "CMakeLists.txt"],
    "README.md": Template(README_MD),
    ".gitignore": Template(GITIGNORE),
}

raylib_structure = {
    "name": "raylib",
    "src": {"main.c": Template(RAYLIB_MAIN_C)},
    "CMakeLists.txt": Template(RAYLIB_CMAKELISTS),
    "vcpkg.json": Template(RAYLIB_VCPKG_JSON),
    "README.md": Template(RAYLIB_README),
    ".gitignore": Template(GITIGNORE),
}

BLUEPRINTS = {
    "basic": project_structure,
    "raylib": raylib_structure,
}


def normalize_build_tool(build_name: str) -> str:
    """Normalize input build tool name to supported file name."""
    lowered = (build_name or "Makefile").lower().strip()
    if "ninja" in lowered:
        return "build.ninja"
    elif "cmake" in lowered:
        return "CMakeLists.txt"
    return "Makefile"


def generate_blueprint(
    structure: dict,
    project_name: str,
    build: str = "Makefile",
    target_dir: Path | str | None = None,
    verbose: bool = False,
) -> dict[str, str]:
    """
    Renders blueprint dictionary into files and directories without using shutil.
    If target_dir is provided, writes directories and files directly to disk via pathlib.
    Returns a dictionary of {relative_file_path: rendered_content}.
    """
    selected_build = normalize_build_tool(build)
    guard_name = "".join(c if c.isalnum() else "_" for c in project_name).upper()
    context = {
        "project_name": project_name,
        "guard": guard_name,
    }

    files: dict[str, str] = {}
    directories: list[Path] = []

    def walk(node: dict, current_dir: Path):
        for key, val in node.items():
            if key == "name":
                continue

            item_path = current_dir / key if str(current_dir) != "." else Path(key)

            if isinstance(val, dict):
                directories.append(item_path)
                walk(val, item_path)
            elif isinstance(val, list):
                # Build tool choices (e.g. ["Makefile", "build.ninja", "CMakeLists.txt"])
                chosen_tool = None
                for tool in val:
                    if tool.lower() == selected_build.lower():
                        chosen_tool = tool
                        break
                if not chosen_tool and val:
                    chosen_tool = val[0]
                if chosen_tool and chosen_tool in BUILD_TEMPLATES:
                    tmpl = BUILD_TEMPLATES[chosen_tool]
                    rel_p = str(
                        current_dir / chosen_tool
                        if str(current_dir) != "."
                        else Path(chosen_tool)
                    ).replace("\\", "/")
                    files[rel_p] = tmpl.safe_substitute(context)
            elif isinstance(val, Template):
                rel_p = str(item_path).replace("\\", "/")
                files[rel_p] = val.safe_substitute(context)
            elif isinstance(val, str):
                rel_p = str(item_path).replace("\\", "/")
                files[rel_p] = Template(val).safe_substitute(context)

    walk(structure, Path("."))

    if target_dir is not None:
        dest = Path(target_dir)
        dest.mkdir(parents=True, exist_ok=True)

        check = _get_check_mark()
        if verbose:
            print(f"Creating project '{project_name}'...")

        for d in directories:
            (dest / d).mkdir(parents=True, exist_ok=True)
            if verbose:
                print(f"  {check} Created {str(d).replace('\\\\', '/')}/")

        for rel_path, content in files.items():
            fpath = dest / rel_path
            fpath.parent.mkdir(parents=True, exist_ok=True)
            fpath.write_text(content, encoding="utf-8")
            if verbose:
                print(f"  {check} Created {rel_path}")

        if verbose:
            print(f"\nProject '{project_name}' ready.")
            print("\nNext steps:")
            print(f"  cd {project_name}")
            if "Makefile" in files:
                print("  make")
                print(f"  ./build/{project_name}")
            elif "build.ninja" in files:
                print("  ninja")
                print(f"  ./build/{project_name}")
            elif "CMakeLists.txt" in files:
                print("  cmake -B build -S .")
                print("  cmake --build build")

    return files


def basic_project(
    project_name: str,
    build: str = "Makefile",
    target_dir: Path | str | None = None,
    verbose: bool = False,
) -> dict[str, str]:
    """Generates the basic project structure using the blueprint."""
    return generate_blueprint(
        structure=project_structure,
        project_name=project_name,
        build=build,
        target_dir=target_dir,
        verbose=verbose,
    )


def create_project_from_blueprint(
    project_name: str,
    template_name: str | None = "basic",
    build: str = "Makefile",
    target_dir: Path | str | None = None,
    verbose: bool = True,
) -> dict[str, str]:
    """Unified entry point to generate any blueprint template without shutil."""
    blueprint = BLUEPRINTS.get(template_name or "basic", project_structure)
    return generate_blueprint(
        structure=blueprint,
        project_name=project_name,
        build=build,
        target_dir=target_dir,
        verbose=verbose,
    )


