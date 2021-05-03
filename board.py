import pygame
from itertools import chain

COLOUR_BACKGROUND = (15, 15, 20)
COLOUR_OUTLINE = (0, 0, 0)
COLOUR_CELL = (235, 137, 52)
COLOUR_TEXT = (255,255,255)

pygame.font.init()
clock = pygame.time.Clock()
    
class Board:
    def __init__(self, window, cell_size, fps) -> None:
        self._fps = fps
        self._cell_size = cell_size
        self._window = window
        self._display = pygame.display.set_mode(self._window, pygame.DOUBLEBUF | pygame.HWSURFACE)

        self.cols = int(self._display.get_width() / self._cell_size)
        self.rows = int(self._display.get_height() / self._cell_size)
        self.grid = [[Cell(col, row) for col in range(self.cols)] for row in range (self.rows)]
    
    def update(self):
        clock.tick(self._fps)
        self._display.fill((COLOUR_BACKGROUND))

        self._update_cells()
        self._draw_cells()
        self._draw_grid()
        self._draw_text()

    def _draw_grid(self) -> None:
        for col in range(self.cols):
            axes = col * self._cell_size

            pygame.draw.line(self._display, COLOUR_OUTLINE, (axes, 1), (axes, self._window[1]))
            pygame.draw.line(self._display, COLOUR_OUTLINE, (1, axes), (self._window[0], axes))
    
    def _draw_cells(self) -> None:
        for cell in chain.from_iterable(zip(*self.grid)):
            if cell.is_alive:
                pygame.draw.rect(self._display, COLOUR_CELL, (
                    self._cell_size *  cell.position[0],
                    self._cell_size *  cell.position[1], 
                    self._cell_size, 
                    self._cell_size)
                ) 
    
    @property                               
    def _live_grid_cells(self):
        return [col for col in self.grid for cell in col if cell.is_alive]

    def _draw_text(self) -> None:
        population_text = pygame.font.SysFont(None, 40).render(f'Population: {round(len(self._live_grid_cells))}', False, COLOUR_TEXT)
        self._display.blit(population_text,(0,0))
    
    def _update_cells(self):
        self.grid = [[cell.validate(self) for cell in col]
                      for col in self.grid]
    

from cell import Cell
        
