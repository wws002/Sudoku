import pygame

width = 650
grid_width = 540
height = 540
blockSize = int(grid_width / 9)
black = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

def drawGrid():
    for x in range(0, grid_width, blockSize):
        for y in range(0, height, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, black, rect, 1)

while running: 
    screen.fill('white')
    drawGrid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    
    pygame.display.flip()
