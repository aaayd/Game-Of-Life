import pygame, random

COLOUR_BLACK = (0,0,0)
COLOUR_GREY = (20,20,20)
COLOUR_CELL = (100,70,30)

class Board:
    def __init__(self, window, cell_size, grid = None) -> None:
        self._cell_size = cell_size
        self._window = window
        self._display = pygame.display.set_mode(self._window)
        self._cols = int(self._display.get_width() / self._cell_size)
        self._rows = int(self._display.get_height() / self._cell_size)
        
        self._grid = [[Cell(col, row) for col in range(self._cols)] for row in range (self._rows)] if grid is None else grid

    def _draw_grid(self):
        for col in range(self._cols):
            for row in range(self._rows):
                x = col * self._cell_size
                y = row * self._cell_size

                pygame.draw.line(self._display, COLOUR_GREY, (x, y), (x, self._window[0]))
                pygame.draw.line(self._display, COLOUR_GREY, (x, y), (self._window[1], y))

    def _draw_cells(self):
        for col in self._grid:
            for cell in col:
                x,y = cell.position
                if cell.is_alive:
                    pygame.draw.rect(self._display, COLOUR_CELL, (x * self._cell_size, y * self._cell_size, self._cell_size, self._cell_size))
                else:
                    pygame.draw.rect(self._display, COLOUR_BLACK, (x * self._cell_size, y * self._cell_size, self._cell_size, self._cell_size))

    
    def _update_cells(self):
        self._grid = [[cell.validate(self) for cell in col] for col in self._grid]
    
    def update(self):
        self._update_cells()
        self._draw_cells()
        self._draw_grid()        
        pygame.display.update()

class Cell:
    def __init__(self, col, row):
        self._status = 1 if random.randint(1,5) == 1 else 0
        self.position = (col, row)

    def set_dead(self):
        self._status = 0

    def set_alive(self):
        self._status = 1

    @property
    def is_alive(self):
        return self._status == 1

    def _neighbour_count(self, board : Board):
        cell_col, cell_row = self.position
        count = 0
        for i in range(-1, 2):
            col = (cell_col + i) % board._cols
            for j in range(-1, 2):                
                row = (cell_row + j) % board._rows
                count += board._grid[row][col].is_alive
        count -= board._grid[cell_row][cell_col].is_alive
        return count

    
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

