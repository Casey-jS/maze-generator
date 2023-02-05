import random
import copy
import pygame as pg

DEAD = (255, 255, 255)
ALIVE = (0, 0, 0)
SIZE = 20

class Maze:

    def __init__(self):
        self.board = []
        for i in range(SIZE):
            row = []
            for j in range(SIZE):
                row.append(DEAD)
            self.board.append(row)

        self.prev = copy.deepcopy(self.board)

    def get_maze(self):
        self.create_maze()
        return self.board

    def start_random(self):
        for i in range(20):
            for j in range(20):
                num = random.randint(0, 1)
                if num == 0:
                    self.board[i][j] = DEAD
                else:
                    self.board[i][j] = ALIVE


    # updates the maze
    def update(self):
        self.prev = copy.deepcopy(self.board)
        for i in range(SIZE):
            for j in range(SIZE):
                count = self.get_neighbors(i, j)
                cell = self.board[i][j]
                if cell == DEAD and count == 3:
                    self.board[i][j] = ALIVE
                elif (count < 2 or count > 4) and cell == ALIVE:
                    self.board[i][j] = DEAD

    # returns the number of neighbors that are alive
    def get_neighbors(self, row, col) -> int:

        count = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i + row < SIZE and j + col < SIZE and row - i > 0 and col - j > 0:
                    if i == 0 and j == 0:
                        continue
                    neighbor = self.prev[i + row][j + col]
                    if neighbor != DEAD:
                        count += 1
        return count

    def create_maze(self):
        self.start_random()
        for _ in range(100):
            self.update()

        self.board[0][0] = DEAD
        self.board[19][19] = DEAD