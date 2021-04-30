import pygame, random

COLOUR_BACKGROUND = (15, 15, 20)
COLOUR_OUTLINE = (0, 0, 0)
COLOUR_CELL = (235, 137, 52)

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
clock = pygame.time.Clock()
class Board:
    def __init__(self, window, cell_size, fps) -> None:
        self._fps = fps
        self._cell_size = cell_size
        self._window = window
        self._display = pygame.display.set_mode(self._window, pygame.DOUBLEBUF | pygame.HWSURFACE, 4)

        self.cols = int(self._display.get_width() / self._cell_size + 2)
        self.rows = int(self._display.get_height() / self._cell_size + 2)
        self.grid = [[Cell(col, row) for col in range(self.cols)] for row in range (self.rows)]

    def _draw_grid(self) -> None:
        for col in range(self.cols):
            size = col * self._cell_size
            pygame.draw.line(self._display, COLOUR_OUTLINE, (size, 1), (size, self._window[0]))
            pygame.draw.line(self._display, COLOUR_OUTLINE, (1, size), (self._window[1] * 2, size))

    def _draw_cells(self) -> None:
        for col in self.grid:
            for cell in col:
                x = self._cell_size *  cell.position[0]
                y = self._cell_size *  cell.position[1]
                
                if cell.is_alive:
                    pygame.draw.rect(self._display, COLOUR_CELL, (
                        x, y, 
                        self._cell_size, 
                        self._cell_size)
                    )                    

    def _draw_text(self) -> None:
        pop = myfont.render(f'Population: {round(len([col for col in self.grid for cell in col if cell.is_alive]) / self._cell_size)}', False, (255, 255, 255))
        self._display.blit(pop,(0,0))
    
    def _update_cells(self):
        self.grid = [[cell.validate(self) for cell in col] for col in self.grid]
    
    def update(self):
        clock.tick(self._fps)
        self._display.fill((COLOUR_BACKGROUND))

        self._update_cells()
        self._draw_cells()
        self._draw_grid()
        self._draw_text()
        

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
        return self._status == 1

    def _neighbour_count(self, board : Board):
        cell_col, cell_row = self.position
        count = 0

        for i in range(-1, 2):
            col = (cell_col + i) % board.cols
            for j in range(-1, 2):                
                row = (cell_row + j) % board.rows
                count += board.grid[row][col].is_alive
        count -= board.grid[cell_row][cell_col].is_alive
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
