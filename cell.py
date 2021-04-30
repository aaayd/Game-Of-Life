import itertools, random
from board import Board

class Cell:
    def __init__(self, col, row):
        self._status = random.randint(0,1)
        self.position = (col, row)

    def set_dead(self):
        self._status = 0

    def set_alive(self):
        self._status = 1

    @property
    def is_alive(self):
        return bool(self._status)

    def _neighbour_count(self, board : Board):
        cell_col, cell_row = self.position

        count = sum(board.grid[(cell_row + j) % board.rows][(cell_col + i) % board.cols].is_alive for i, j in itertools.product(range(-1, 2), range(-1, 2)))
        return count - self.is_alive

    
    def validate(self, board : Board):
        neighbour_count = self._neighbour_count(board)

        newcell = Cell(*self.position)
        newcell._status = self._status

        if self.is_alive:
            if not (1 < neighbour_count < 4):
                newcell.set_dead()
        else:
            if neighbour_count == 3:
                newcell.set_alive()

        return newcell
