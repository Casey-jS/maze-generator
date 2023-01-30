import random as r
class Cell:
    def __init__(self, row, col):
        self.color = (0, 0, 0)
        self._row = row
        self._col = col

    def set_random(self):
        self.color = (r.randint(255), r.randint(255), r.randint(255))