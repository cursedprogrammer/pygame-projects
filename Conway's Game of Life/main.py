import pygame
import random
import grid
import time

RES = (1280, 720)
BLOCK_SIZE = 10
GRID_W = 128
GRID_H = 72
VALUES = (0, 1)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (20, 20, 20)
CAPTION = "Game of Life"
PAUSED = 0
RUNNING = 1

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(RES)
        pygame.display.set_caption(CAPTION)
        self.start = grid.make_grid(grid.GRID_W, grid.GRID_H)
        self.matrix = grid.make_grid(GRID_W, GRID_H)
        self.matrix2 = grid.make_grid(GRID_W, GRID_H)
        self.current_matrix = self.matrix
        grid.random_seed(self.matrix)
        self.state = PAUSED

    def run(self):
        while True:
            self.window.fill(BLACK)
            self.draw_grid()
            self.render(self.current_matrix)            
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    self.selected_coords = self.get_grid_pos(self.current_matrix, pygame.mouse.get_pos())
                    if self.current_matrix[self.selected_coords[0]][self.selected_coords[1]] == 1:
                        self.current_matrix[self.selected_coords[0]][self.selected_coords[1]] = 0
                    else:
                        self.current_matrix[self.selected_coords[0]][self.selected_coords[1]] = 1
                    print(self.get_grid_pos(self.current_matrix, pygame.mouse.get_pos()))
                elif e.type == pygame.KEYDOWN and e.key == pygame.K_p:
                    if self.state == PAUSED:
                        self.state = RUNNING
                    else:
                        self.state = PAUSED
            if self.state is not PAUSED:
                if self.current_matrix == self.matrix:
                    grid.new_matrix2(self.matrix, self.matrix2)
                    self.current_matrix = self.matrix2
                else:
                    grid.new_matrix2(self.matrix2, self.matrix)
                    self.current_matrix = self.matrix
            pygame.display.update()
        #    time.sleep(0.1)

    def render(self, grid):
        X_COORD = 0
        Y_COORD = 0
        for y in grid:
            for x in y:
                if x == 1:                
                    pygame.draw.rect(self.window, WHITE, pygame.Rect(X_COORD, Y_COORD, BLOCK_SIZE, BLOCK_SIZE))
                X_COORD += BLOCK_SIZE
            Y_COORD += BLOCK_SIZE
            X_COORD = 0
            
    def get_grid_pos(self, grid, click_coords):
        X_COORD = 0
        Y_COORD = 0
        for y in range(1, len(grid)):
            for x in range(1, len(grid[0])):
                if (click_coords[1] >= Y_COORD and click_coords[1] < Y_COORD + BLOCK_SIZE) and (click_coords[0] >= X_COORD and click_coords[0] < X_COORD + BLOCK_SIZE):
                    return (y, x)
                X_COORD += BLOCK_SIZE
            Y_COORD += BLOCK_SIZE
            X_COORD = 0
            
    def draw_grid(self):
        for x in range(0, RES[0], BLOCK_SIZE):
            for y in range(0, RES[1], BLOCK_SIZE):
                pygame.draw.rect(self.window, GRAY, pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE), 1)

game = Game()
game.run()
