import pygame

width = 560
grid_width = 540
height = 580
grid_height = 540
sudokuBlockSize = int(grid_width / 9)
black = (0, 0, 0)
red = (255, 0, 0)
rect_list = []
selected_rect = None

pygame.init()
screen = pygame.display.set_mode((width, height))
running = True

for x in range(10, grid_width + 10, sudokuBlockSize):
    for y in range(10, grid_height + 10, sudokuBlockSize):
        rect = pygame.Rect(x, y, sudokuBlockSize, sudokuBlockSize)
        rect_list.append(rect)

def drawSudokuGrid(selected_rect):
    if selected_rect:
        for rect in rect_list:
            if rect.x == selected_rect.x and rect.y == selected_rect.y:
                pygame.draw.rect(screen, red, rect)
            else:
                pygame.draw.rect(screen, black, rect, 1)
    else:
        for rect in rect_list:
            pygame.draw.rect(screen, black, rect, 1)

while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for rect in rect_list:
                if rect.collidepoint(event.pos):
                    selected_rect = rect
    
    screen.fill('white')
    drawSudokuGrid(selected_rect)
    pygame.display.flip()
