from classes import Board
import pygame

pygame.init()
cell_size = 5
window = 700, 450

board = Board(window, cell_size)
while True:
    for event in pygame.event.get():
        if event.type ==pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
    
    board.update()
    
    