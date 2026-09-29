
# Raylib

A basic raylib project using cmake, vcpkg.

## Build

```bash
cmake -B build -S . -DCMAKE_TOOLCHAIN_FILE="$env:VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake"
cmake --build build
```
