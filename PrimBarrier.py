import pygame
import random
from maze import Maze, Cell, WHITE, BLACK, GREY
import time

MAZE_TYPE = 1

WALL_MAZE = 0
BARRIER_MAZE = 1

WIDTH = 800
win = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Maze")


# DIRS = [(0, 1), (1, 0), (-1, 0), (0, -1)]


class BarrierMazeCell(Cell):

    def __init__(self, row, col, width):
        super().__init__(row, col, width)
        self.colour = BLACK

    def is_wall(self):
        return self.colour == BLACK

    def is_path(self):
        return self.colour == WHITE

    def make_wall(self):
        self.colour = BLACK

    def make_path(self):
        self.colour = WHITE
    #
    # def draw_spot(self, win):
    #     pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.width))


class BarrierMaze(Maze):
    directions = [(2, 0), (0, 2), (-2, 0), (0, -2)]

    def __init__(self, width, total_rows):
        super().__init__(width, total_rows)
        self.grid = []
        self.make_grid()
        self.start = None

    def make_grid(self):
        print('yep')
        gap = self.width // self.total_rows
        for i in range(self.total_rows):
            self.grid.append([])
            for j in range(self.total_rows):
                spot = BarrierMazeCell(i, j, gap)
                self.grid[i].append(spot)

    def set_start(self, pos):
        row, col = self.get_clicked_position(pos)
        square = self.grid[row][col]
        if self.start:
            self.start.make_wall()
        square.make_path()
        self.start = square

    def add_frontiers(self, frontiers, frontiers_set, cell):
        grid = self.grid
        row, col = cell.row, cell.col
        for y, x in BarrierMaze.directions:
            if 0 < row + y < len(grid) - 1 and 0 < col + x < len(grid) - 2:
                if grid[row + y][col + x].is_wall() and grid[row + y][col + x] not in frontiers_set:
                    frontiers.append(grid[row + y][col + x])
                    frontiers_set.add(grid[row + y][col + x])

    def add_connecting_path(self, cell):
        grid = self.grid
        neighbours = []
        row, col = cell.row, cell.col
        for y, x in BarrierMaze.directions:
            if 0 < row + y < len(grid) - 1 and 0 < col + x < len(grid) - 1:
                if grid[row + y][col + x].is_path():
                    neighbours.append(grid[row + y][col + x])
        connector = neighbours.pop(random.randrange(len(neighbours)))
        con_row, con_col = connector.row, connector.col
        grid[(row + con_row) // 2][(col + con_col) // 2].make_path()

    def generate_maze(self, win):
        frontiers = []
        frontiers_set = set()
        self.add_frontiers(frontiers, frontiers_set, self.start)
        while frontiers:
            self.draw(win)
            # time.sleep(0.5)
            cell = frontiers.pop(random.randrange(len(frontiers)))
            cell.make_path()
            self.add_frontiers(frontiers, frontiers_set, cell)
            self.add_connecting_path(cell)


def main(win, width):
    ROWS = 50
    maze = BarrierMaze(ROWS, width)
    num = 0
    run = True
    while run:
        print(num)
        num += 1
        event = pygame.event.wait()
        if event.type != pygame.MOUSEMOTION:
            maze.draw(win)

        if event.type == pygame.QUIT:
            run = False

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            maze.set_start(pos)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                maze.generate_maze(win)

    pygame.quit()


main(win, WIDTH)
