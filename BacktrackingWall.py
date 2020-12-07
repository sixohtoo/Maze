import pygame
import random
import time
from maze import Maze, Cell, WHITE, BLACK

BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
PINK = (250, 0, 100)
LIGHT_BLUE = (0, 191, 255)


WIDTH = 800
win = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Randomised Prim's Algorithm")


class WallMazeCell(Cell):
    def __init__(self, row, col, width):
        super().__init__(row, col, width)
        self.walls = {}
        self.reset_walls()
        self.colour = WHITE

    def __str__(self):
        return str(self.row, self.col)

    def __repr__(self):
        return str(self.row, self.com)

    def reset_walls(self):
        self.walls = {
            (0, 1): True,
            (0, -1): True,
            (1, 0): True,
            (-1, 0): True
        }

    def is_wall(self, wall):
        return self.walls[wall]

    def draw(self, win):
        # Draws left and bottom wall.
        if self.walls[(1, 0)]: # bottom wall
            pygame.draw.line(win, BLACK, (self.x + self.width, self.y), (self.x + self.width, self.y + self.width), 2)

        if self.walls[(0, 1)]: # left wall
            pygame.draw.line(win, BLACK, (self.x, self.y + self.width), (self.x + self.width, self.y + self.width), 2)



class WallMaze(Maze):
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def __init__(self, width, total_rows):
        super().__init__(width, total_rows)
        self.grid = []
        self.make_grid()
        self.visited = set()

    def __str__(self):
        return str(self.visited)

    def make_grid(self):
        gap = self.width // self.total_rows
        for i in range(self.total_rows):
            self.grid.append([])
            for j in range(self.total_rows):
                spot = WallMazeCell(i, j, gap)
                self.grid[i].append(spot)

    def remove_wall(self, cell, wall):
        cell.walls[wall] = False
        other = self.grid[cell.row + wall[0]][cell.col + wall[1]]
        flipped_wall = (-wall[0], -wall[1])
        other.walls[flipped_wall] = False

    def draw(self, win):
        super().draw(win)
        pygame.draw.line(win, BLACK, (0, 0), (0, self.width), 1)
        pygame.draw.line(win, BLACK, (self.width, 0), (self.width, self.width), 1)
        pygame.draw.line(win, BLACK, (0, 0), (self.width, 0), 1)
        pygame.draw.line(win, BLACK, (0, self.width), (self.width, self.width), 1)
        pygame.display.update()
        print('draw')

    def has_start(self):
        return self.start

    def set_start(self, pos):
        row, col = self.get_clicked_position(pos)
        square = self.grid[row][col]
        self.start = square

    def get_valid_edges(self, cell):
        valid_edges = [x for x in cell.walls if cell.walls[x]]
        row, col = cell.row, cell.col
        for y, x in valid_edges[::-1]:
            if row + y < 0 or row + y >= len(self.grid):
                valid_edges.remove((y, x))
            elif col + x < 0 or col + x >= len(self.grid):
                valid_edges.remove((y, x))
            elif self.grid[row + y][col + x] in self.visited:
                valid_edges.remove((y, x))

        return valid_edges

    def backtracker(self, win, cell):
        self.visited.add(cell)
        stack = [cell]
        while stack:
            #time.sleep(0.1)
            self.draw(win)
            if stack[0] != cell:
                self.visited.add(cell)
            row, col = cell.row, cell.col
            edges = self.get_valid_edges(cell)
            if edges:
                wall = edges.pop(random.randrange(len(edges)))
                y, x = wall
                self.remove_wall(cell, wall)
                stack.append(cell)
                cell = self.grid[row + y][col + x]
            else:
                stack.pop()
                if stack:
                    cell = stack[-1]
        print('DONE')
        self.draw(win)



def main(win, width):
    ROWS = 50
    maze = WallMaze(ROWS, width)

    run = True
    maze.draw(win)
    while run:
        event = pygame.event.wait()


        if event.type == pygame.QUIT:
            run = False

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            maze.set_start(pos)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and maze.has_start():
                maze.backtracker(win, maze.start)
                # maze.visited.add(maze.start)
                # maze.get_valid_edges(maze.start)

    pygame.quit()


main(win, WIDTH)
