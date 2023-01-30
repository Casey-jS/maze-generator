import copy

class Board:
    def __init__(self, size = 20):
        self._board = []
        self.size = size

        for i in range(size):
            row = []
            for j in range(size):
                row.append((0, 0, 0))
            self._board.append(row)

        self.prev = copy.deepcopy(self._board)

    def update(self):

        self.prev = copy.deepcopy(self._board)

        for i in range(self.size):
            for j in range(self.size):
                count = self.get_neighbors(i, j)

                if self._board[i][j] == (0, 0, 0) and count == 3:
                    self._board[i][j] = (255, 255, 255) # set the cell to alive
                elif self._board[i][j]



    def get_neighbors(self, row, col) -> int:
        count = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i + row < self.size and j + col < self.size and row - i > 0 and col - j > 0:
                    if i == 0 and j == 0:
                        continue
                    neighbor = self.prev[i + row][j + col]
                    if neighbor != (0, 0, 0):
                        count += 1

        return count




