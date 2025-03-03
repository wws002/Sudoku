import pygame

width = 810
grid_width = 540
height = 580
grid_height = 540
sudokuBlockSize = int(grid_width / 9)
numberSelectBlockSize = 70
black = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

def drawSudokuGrid():
    for x in range(10, grid_width + 10, sudokuBlockSize):
        for y in range(10, grid_height + 10, sudokuBlockSize):
            rect = pygame.Rect(x, y, sudokuBlockSize, sudokuBlockSize)
            pygame.draw.rect(screen, black, rect, 1)

def drawNumberSelectionGrid():
    for x in range(grid_width + 50, grid_width + numberSelectBlockSize * 3 + 50, numberSelectBlockSize):
        for y in range(10, numberSelectBlockSize * 3 + 10, numberSelectBlockSize):
            rect = pygame.Rect(x, y, numberSelectBlockSize, numberSelectBlockSize)
            pygame.draw.rect(screen, black, rect, 1)

while running: 
    screen.fill('white')
    drawSudokuGrid()
    drawNumberSelectionGrid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    
    pygame.display.flip()
