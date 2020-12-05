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
        #self.colour = BLACK
        # self.width = width
        # self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.width))


class Maze:
    def __init__(self, total_rows, width):
        self.width = width
        self.total_rows = total_rows

    def draw(self, win):
        win.fill(WHITE)
        for row in self.grid:
            for spot in row:
                spot.draw(win)
        pygame.display.update()

    def get_clicked_position(self, pos):
        gap = self.width // self.total_rows
        y, x = pos
        row = y // gap
        col = x // gap
        return row, col

