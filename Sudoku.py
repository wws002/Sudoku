import pygame

width = 560
grid_width = 540
height = 620
grid_height = 540
sudokuBlockSize = int(grid_width / 9)

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
grey = (128, 128, 128)
green = (0, 255, 0)

rect_list = []
original_display_list = [False, True, True, True, True, True, True, True, True, True, True, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
current_display_list = [False, True, True, True, True, True, True, True, True, True, True, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
nums_list = [4, 3, 5, 2, 6, 9, 7, 8, 1, 6, 8, 2, 5, 7, 1, 4, 9, 3, 1, 9, 7, 8, 3, 4, 5, 6, 2, 8, 2, 6, 1, 9, 5, 3, 4, 7, 3, 7, 4, 6, 8, 2, 9, 1, 5, 9, 5, 1, 7, 4, 3, 6, 2, 8, 5, 1, 9, 3, 2, 6, 8, 7, 4, 2, 4, 8, 9, 5, 7, 1, 3, 6, 7, 6, 3, 4, 1, 8, 2, 5, 9]
solved_list = [4, 3, 5, 2, 6, 9, 7, 8, 1, 6, 8, 2, 5, 7, 1, 4, 9, 3, 1, 9, 7, 8, 3, 4, 5, 6, 2, 8, 2, 6, 1, 9, 5, 3, 4, 7, 3, 7, 4, 6, 8, 2, 9, 1, 5, 9, 5, 1, 7, 4, 3, 6, 2, 8, 5, 1, 9, 3, 2, 6, 8, 7, 4, 2, 4, 8, 9, 5, 7, 1, 3, 6, 7, 6, 3, 4, 1, 8, 2, 5, 9]

selected_rect = None
running = True
game_over = False
strikes = 0

pygame.init()
font = pygame.font.SysFont(None, 26)
screen = pygame.display.set_mode((width, height))

for x in range(10, grid_width + 10, sudokuBlockSize):
    for y in range(40, grid_height + 40, sudokuBlockSize):
        rect = pygame.Rect(x, y, sudokuBlockSize, sudokuBlockSize)
        rect_list.append(rect)

def drawSudokuGrid(selected_rect):
    for x in range(10, grid_width + 10, sudokuBlockSize * 3):
        for y in range(40, grid_height + 40, sudokuBlockSize * 3):
            rect = pygame.Rect(x, y, sudokuBlockSize * 3, sudokuBlockSize * 3)
            pygame.draw.rect(screen, black, rect, 3)

    if selected_rect:
        for rect in rect_list:
            if rect == selected_rect:
                if not current_display_list[rect_list.index(selected_rect)]:
                    pygame.draw.rect(screen, grey, rect)
                elif nums_list[rect_list.index(selected_rect)] == solved_list[rect_list.index(selected_rect)]:
                    pygame.draw.rect(screen, green, rect)
                else:
                    pygame.draw.rect(screen, red, rect)
            else:
                pygame.draw.rect(screen, black, rect, 1)
    else:
        for rect in rect_list:
            pygame.draw.rect(screen, black, rect, 1)

    for index in range(len(rect_list)):
        if current_display_list[index]:
            number_image = font.render(str(nums_list[index]), True, black, white)
            margin_x = (sudokuBlockSize-1 - number_image.get_width()) // 2
            margin_y = (sudokuBlockSize-1 - number_image.get_height()) // 2
            screen.blit(number_image, (rect_list[index].x + 2 + margin_x, rect_list[index].y + 2 + margin_y))

def drawStrikes():
    strike_text_image = font.render(f"{strikes}/3 Errors", True, black, white)
    screen.blit(strike_text_image, (460, 10))

def drawWinMessage():
    win_text_image = font.render("You Win!", True, black, white)
    screen.blit(win_text_image, (10, 10))

def drawLoseMessage():
    lose_text_image = font.render("You lost", True, black, white)
    screen.blit(lose_text_image, (10, 10))

def number_input(number, strikes):
    if solved_list[rect_list.index(selected_rect)] != number and nums_list[rect_list.index(selected_rect)] != number:
        strikes += 1
    nums_list[rect_list.index(selected_rect)] = number
    return strikes

while running: 
    while game_over:
        restart_message = font.render("Enter 'p' to play again", True, black, white)
        screen.blit(restart_message, (200, 10))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    nums_list = solved_list.copy()
                    current_display_list = original_display_list.copy()
                    strikes = 0
                    selected_rect = None
                    game_over = False
                    break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for rect in rect_list:
                if rect.collidepoint(event.pos):
                    selected_rect = rect
        if event.type == pygame.KEYDOWN:
            if selected_rect:
                if event.key == pygame.K_1:
                    strikes = number_input(1, strikes)
                if event.key == pygame.K_2:
                    strikes = number_input(2, strikes)
                if event.key == pygame.K_3:
                    strikes = number_input(3, strikes)
                if event.key == pygame.K_4:
                    strikes = number_input(4, strikes)
                if event.key == pygame.K_5:
                    strikes = number_input(5, strikes)
                if event.key == pygame.K_6:
                    strikes = number_input(6, strikes)
                if event.key == pygame.K_7:
                    strikes = number_input(7, strikes)
                if event.key == pygame.K_8:
                    strikes = number_input(8, strikes)
                if event.key == pygame.K_9:
                    strikes = number_input(9, strikes)

                current_display_list[rect_list.index(selected_rect)] = True

    screen.fill(white)
    drawSudokuGrid(selected_rect)
    drawStrikes()

    if strikes > 2:
        drawLoseMessage()
        game_over = True

    if current_display_list.count(False) == 0 and nums_list == solved_list:
        drawWinMessage()
        game_over = True

    pygame.display.flip()