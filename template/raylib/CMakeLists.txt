cmake_minimum_required(VERSION 4.4)

project(raylib-project C)

set(CMAKE_C_STANDARD 17)
set(CMAKE_C_STANDARD_REQUIRED ON)

find_package(raylib CONFIG REQUIRED)

add_executable(${PROJECT_NAME}
    src/main.c
)

target_link_libraries(${PROJECT_NAME}
    PRIVATE raylib
)
