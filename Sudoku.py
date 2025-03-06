import pygame

width = 560
grid_width = 540
height = 580
grid_height = 540
sudokuBlockSize = int(grid_width / 9)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
rect_list = []
nums_list = [4, 3, 5, 2, 6, 9, 7, 8, 1, 6, 8, 2, 5, 7, 1, 4, 9, 3, 1, 9, 7, 8, 3, 4, 5, 6, 2, 8, 2, 6, 1, 9, 5, 3, 4, 7, 3, 7, 4, 6, 8, 2, 9, 1, 5, 9, 5, 1, 7, 4, 3, 6, 2, 8, 5, 1, 9, 3, 2, 6, 8, 7, 4, 2, 4, 8, 9, 5, 7, 1, 3, 6, 7, 6, 3, 4, 1, 8, 2, 5, 9]
selected_rect = None
running = True

pygame.init()
font = pygame.font.SysFont(None, 26)
screen = pygame.display.set_mode((width, height))

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

    for index in range(len(rect_list)):
        number_image = font.render(str(nums_list[index]), True, black, white)
        margin_x = (sudokuBlockSize-1 - number_image.get_width()) // 2
        margin_y = (sudokuBlockSize-1 - number_image.get_height()) // 2
        screen.blit(number_image, (rect_list[index].x + 2 + margin_x, rect_list[index].y + 2 + margin_y))

while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for rect in rect_list:
                if rect.collidepoint(event.pos):
                    selected_rect = rect
        if event.type == pygame.KEYDOWN:
            if selected_rect:
                if event.key == pygame.K_1:
                    nums_list[rect_list.index(selected_rect)] = 1
                if event.key == pygame.K_2:
                    nums_list[rect_list.index(selected_rect)] = 2
                if event.key == pygame.K_3:
                    nums_list[rect_list.index(selected_rect)] = 3
                if event.key == pygame.K_4:
                    nums_list[rect_list.index(selected_rect)] = 4
                if event.key == pygame.K_5:
                    nums_list[rect_list.index(selected_rect)] = 5
                if event.key == pygame.K_6:
                    nums_list[rect_list.index(selected_rect)] = 6
                if event.key == pygame.K_7:
                    nums_list[rect_list.index(selected_rect)] = 7
                if event.key == pygame.K_8:
                    nums_list[rect_list.index(selected_rect)] = 8
                if event.key == pygame.K_9:
                    nums_list[rect_list.index(selected_rect)] = 9
            
    
    screen.fill('white')
    drawSudokuGrid(selected_rect)
    pygame.display.flip()
