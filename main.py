import pygame
import sys
import random
import time

res: tuple[int, int] = (1920, 1080)
# res: tuple[int, int] = (2560, 1440)
pygame.init()
screen: pygame.Surface = pygame.display.set_mode(res)
pygame.display.set_caption("asdf")

colums, rows = (65, 65)
# colums, rows = (17, 17)

running = True

tile_size = 1080 // rows
offset_x, offset_y = (
    res[0] // 2 - colums * tile_size // 2,
    res[1] // 2 - rows * tile_size // 2,
)

# stack
stack = [(1, 1)]
global current_x
global current_y
current_x = 1
current_y = 1

grid: list[list[int]] = [[1 for _ in range(rows)] for _ in range(colums)]


def gen_maze(cx: int, cy: int, _grid):
    global current_x
    global current_y

    directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
    valid = []
    for dir in directions:
        nx, ny = dir
        if (
            0 <= cx + nx < len(_grid)
            and 0 <= cy + ny < len(_grid[0])
            and _grid[cx + nx][cy + ny]
        ):
            valid.append(((cx + nx, cy + ny), (cx + nx // 2, cy + ny // 2)))

    if valid:
        choice = tuple(random.choice(valid))
        x, y = choice[0]
        wall_x, wall_y = choice[1]

        grid[x][y] = 0
        grid[wall_x][wall_y] = 0

        stack.append(choice[0])
        current_x = x
        current_y = y
    elif stack:
        stack.pop()


generating_maze = False

while running:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            if event.key == pygame.K_SPACE and not generating_maze:
                generating_maze = True


    if generating_maze and stack:
        current = stack[-1]
        x, y = current
        current_x = x
        current_y = y
        gen_maze(x, y, grid)
        time.sleep(1.0 / 10)
    elif generating_maze and not stack:
        print("stack is empty!")
        generating_maze = False


    screen.fill(pygame.Color("grey1"))

    for y in range(colums):
        for x in range(rows):
            r = (
                x * tile_size + offset_x,
                y * tile_size + offset_y,
                tile_size,
                tile_size,
            )

            if grid[x][y] == 1:
                pygame.draw.rect(screen, pygame.Color("darkcyan"), r)
                pygame.draw.rect(screen, pygame.Color("darkorchid4"), r, 1)

            else:
                if x == current_x and y == current_y:
                    pygame.draw.rect(screen, pygame.Color("green"), r)
                else:
                    pygame.draw.rect(screen, pygame.Color("maroon"), r)

    pygame.display.flip()

pygame.quit()
sys.exit()
