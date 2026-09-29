#include "raylib.h"

int main(void)
{
    InitWindow(800, 450, "Raylib Project");

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
