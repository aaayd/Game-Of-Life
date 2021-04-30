from classes import Board
import pygame


pygame.init()
pygame.event.set_allowed([pygame.KEYDOWN])
cell_size = 12
window = 1920,1080
fps = 30

board = Board(window, cell_size, fps)
while True:
    for event in pygame.event.get():
        if event.type ==pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit() 

    board.update()
    pygame.display.update() 
    
