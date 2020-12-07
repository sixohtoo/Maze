import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)


class Cell:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.width = width

    def get_pos(self):
        return self.row, self.col


class Maze:
    def __init__(self, total_rows, width):
        self.width = width
        self.total_rows = total_rows
        self.start = None

    def draw(self, win):
        win.fill(WHITE)
        pygame.display.update()
        for row in self.grid:
            for spot in row:
                spot.draw(win)

    def get_clicked_position(self, pos):
        gap = self.width // self.total_rows
        y, x = pos
        row = y // gap
        col = x // gap
        return row, col

