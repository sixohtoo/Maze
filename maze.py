import pygame
import random
import time

WIDTH = 800
win = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Maze")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)

DIRS = [(0, 1), (1, 0), (-1, 0), (0, -1)]


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.colour = BLACK
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_wall(self):
        return self.colour == BLACK

    def is_path(self):
        return self.colour == WHITE

    def make_wall(self):
        self.colour = BLACK

    def make_path(self):
        self.colour = WHITE

    def draw(self, win):
        # print(self.row, self.col)
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.width))


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
            # if DRAW != IMMEDIATE or not (spot.is_open() or spot.is_closed()):
            #     spot.draw(win)
    #draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_position(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col


def add_frontiers(frontiers, frontiers_set, cell, grid):
    directions = [(2, 0), (0, 2), (-2, 0), (0, -2)]
    row, col = cell.row, cell.col
    for y, x in directions:
        if 0 < row + y < len(grid) - 1 and 0 < col + x < len(grid) - 2:
            if grid[row + y][col + x].is_wall() and grid[row + y][col + x] not in frontiers_set:
                frontiers.append(grid[row + y][col + x])
                frontiers_set.add(grid[row + y][col + x])


def add_connecting_path(cell, grid):
    directions = [(2, 0), (0, 2), (-2, 0), (0, -2)]
    neighbours = []
    row, col = cell.row, cell.col
    for y, x in directions:
        if 0 < row + y < len(grid) - 1 and 0 < col + x < len(grid) - 1:
            if grid[row + y][col + x].is_path():
                neighbours.append(grid[row + y][col + x])
    connector = neighbours.pop(random.randrange(len(neighbours)))
    con_row, con_col = connector.row, connector.col
    grid[(row + con_row) // 2][(col + con_col) // 2].make_path()


def generate_maze(draw, grid, start):
    frontiers = []
    frontiers_set = set()
    add_frontiers(frontiers, frontiers_set, start, grid)
    while frontiers:
        draw()
        #time.sleep(0.5)
        cell = frontiers.pop(random.randrange(len(frontiers)))
        cell.make_path()
        add_frontiers(frontiers, frontiers_set, cell, grid)
        add_connecting_path(cell, grid)


def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    run = True
    while run:
        event = pygame.event.wait()
        if event.type != pygame.MOUSEMOTION:
            draw(win, grid, ROWS, width)
        if event.type == pygame.QUIT:
            run = False

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            row, col = get_clicked_position(pos, ROWS, width)
            spot = grid[row][col]
            if start:
                start.make_wall()
            spot.make_path()
            start = spot

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and start:
                generate_maze(lambda: draw(win, grid, ROWS, width), grid, start)

    pygame.quit()


main(win, WIDTH)
