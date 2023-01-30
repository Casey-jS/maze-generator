import pygame
import Board
import random

class Game:
    def __init__(self, fps=60):
        self.board = Board(20)
        self.finished = False
        self.running = False
        self.fps = fps


    def loop(self):
        clock = pygame.time.Clock()

        while not self.finished:
            delta = clock.tick(self.fps) / 1000.0 # set fps

            for event in pygame.event.get():
                # if the user hits the X
                if event.type == pygame.QUIT:
                    self._finished = True
    
    def start_random(self):
        for i in range(self.board.size):
            for j in range(self.board.size):
                num = random.randint(1, 100)
                if num < 16:
                    self.board[i][j] = (255, 255, 255)




def main():
    pygame.init()
    size = (800, 800)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Maze Generator")
    square_size = 40
    square_color = (0, 0, 255)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((255, 255, 255))

        for x in range(0, 800, square_size):
            for y in range(0, 800, square_size):
                pygame.draw.rect(screen, square_color, (x, y, square_size, square_size))
        pygame.display.update()




