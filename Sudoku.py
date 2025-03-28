import pygame
import requests

width = 560
grid_width = 540
height = 650
grid_height = 540
sudokuBlockSize = int(grid_width / 9)

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
grey = (128, 128, 128)
green = (0, 255, 0)

selected_rect = None
running = True
game_over = False
mark = False
game_start = True
strikes = 0

pygame.init()
font = pygame.font.SysFont(None, 30)
marked_font = pygame.font.SysFont(None, 18)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sudoku")

rect_list = []
mark_button_rect = pygame.Rect(width/2 - 45, height - 65, 90, 60)
easy_button_rect = pygame.Rect(10, 200, 90, 60)
medium_button_rect = pygame.Rect(200, 200, 90, 60)
hard_button_rect = pygame.Rect(400, 200, 90, 60)
marked_list = [[0, 0, 0, 0, 0, 0, 0, 0, 0] for _ in range(81)]
for x in range(10, grid_width + 10, sudokuBlockSize):
    for y in range(40, grid_height + 40, sudokuBlockSize):
        rect = pygame.Rect(x, y, sudokuBlockSize, sudokuBlockSize)
        rect_list.append(rect)

def generatePuzzle(difficulty):
    api_url = f'https://api.api-ninjas.com/v1/sudokugenerate?difficulty={difficulty}'
    response = requests.get(api_url, headers={'X-Api-Key': 'd+raljYygqWEImdv++PFMg==R0f8jFUTLXMey3oM'})
    values = response.json()['puzzle']
    solutions = response.json()['solution']
    nums_list = []
    solved_list = []

    for inner_list in values:
        nums_list.extend(inner_list)

    for index in range(len(nums_list)):
        if not nums_list[index]:
            nums_list[index] = 0

    for inner_list in solutions:
        solved_list.extend(inner_list)

    return nums_list, solved_list

def drawSudokuGrid(selected_rect):
    for x in range(10, grid_width + 10, sudokuBlockSize * 3):
        for y in range(40, grid_height + 40, sudokuBlockSize * 3):
            rect = pygame.Rect(x, y, sudokuBlockSize * 3, sudokuBlockSize * 3)
            pygame.draw.rect(screen, black, rect, 3)

    if selected_rect:
        for rect in rect_list:
            if rect == selected_rect:
                if not nums_list[rect_list.index(selected_rect)]:
                    pygame.draw.rect(screen, grey, rect, 6)
                elif nums_list[rect_list.index(selected_rect)] == solved_list[rect_list.index(selected_rect)]:
                    pygame.draw.rect(screen, green, rect, 6)
                    for index in range(len(nums_list)):
                        if nums_list[index] == nums_list[rect_list.index(selected_rect)] and rect_list[index] != selected_rect:
                            pygame.draw.rect(screen, grey, rect_list[index], 6)
                else:
                    pygame.draw.rect(screen, red, rect, 6)
            else:
                pygame.draw.rect(screen, black, rect, 1)
    else:
        for rect in rect_list:
            pygame.draw.rect(screen, black, rect, 1)

    for index in range(len(rect_list)):
        if nums_list[index]:
            number_image = font.render(str(nums_list[index]), True, black, white)
            margin_x = (sudokuBlockSize-1 - number_image.get_width()) // 2
            margin_y = (sudokuBlockSize-1 - number_image.get_height()) // 2
            screen.blit(number_image, (rect_list[index].x + 2 + margin_x, rect_list[index].y + 2 + margin_y))
        else:
            for x in range(3):
                if marked_list[index][x]:
                    marked_number_image = marked_font.render(str(marked_list[index][x]), True, black, white)
                    screen.blit(marked_number_image, (rect_list[index].x + 5 + x * 20, rect_list[index].y + 5))
            for x in range(3):
                if marked_list[index][x+3]:
                    marked_number_image = marked_font.render(str(marked_list[index][x+3]), True, black, white)
                    screen.blit(marked_number_image, (rect_list[index].x + 5 + x * 20, rect_list[index].y + 25))
            for x in range(3):
                if marked_list[index][x+6]:
                    marked_number_image = marked_font.render(str(marked_list[index][x+6]), True, black, white)
                    screen.blit(marked_number_image, (rect_list[index].x + 5 + x * 20, rect_list[index].y + 45))

def drawStrikes():
    strike_text_image = font.render(f"{strikes}/3 Errors", True, black)
    screen.blit(strike_text_image, (460, 10))

def drawWinMessage():
    win_text_image = font.render("You Win!", True, black, white)
    screen.blit(win_text_image, (10, 10))

def drawLoseMessage():
    lose_text_image = font.render("You lost", True, black, white)
    screen.blit(lose_text_image, (10, 10))

def drawMarkButton():
    mark_button_text_image = font.render("Mark", True, black, white)
    if mark:
        pygame.draw.rect(screen, red, mark_button_rect, 6)
        screen.blit(mark_button_text_image, (mark_button_rect.x + 20, mark_button_rect.y + 20))
    else:
        pygame.draw.rect(screen, black, mark_button_rect, 1)
        screen.blit(mark_button_text_image, (mark_button_rect.x + 20, mark_button_rect.y + 20))

def drawEasyButton():
    easy_button_text_image = font.render("Easy", True, black, white)
    pygame.draw.rect(screen, black, easy_button_rect, 1)
    screen.blit(easy_button_text_image, (easy_button_rect.x + 20, easy_button_rect.y + 20))

def drawMediumButton():
    medium_button_text_image = font.render("Medium", True, black, white)
    pygame.draw.rect(screen, black, medium_button_rect, 1)
    screen.blit(medium_button_text_image, (medium_button_rect.x + 8, medium_button_rect.y + 20))

def drawHardButton():
    hard_button_text_image = font.render("Hard", True, black, white)
    pygame.draw.rect(screen, black, hard_button_rect, 1)
    screen.blit(hard_button_text_image, (hard_button_rect.x + 20, hard_button_rect.y + 20))

def number_input(number, strikes):
    if mark:
        if marked_list[rect_list.index(selected_rect)][number - 1] == number:
            marked_list[rect_list.index(selected_rect)][number - 1] = 0
        else:
            marked_list[rect_list.index(selected_rect)][number - 1] = number
        return strikes
    
    if not number:
        nums_list[rect_list.index(selected_rect)] = 0
        return strikes
    if solved_list[rect_list.index(selected_rect)] != number and nums_list[rect_list.index(selected_rect)] != number:
        strikes += 1
    nums_list[rect_list.index(selected_rect)] = number
    return strikes

while running: 
    screen.fill(white)

    while game_start:
        difficulty_select_text_image = font.render("Choose difficulty", True, black, white)
        screen.blit(difficulty_select_text_image, (150, 40))
        drawEasyButton()
        drawMediumButton()
        drawHardButton()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button_rect.collidepoint(event.pos):
                    nums_list, solved_list = generatePuzzle("easy")
                    game_start = False
                if medium_button_rect.collidepoint(event.pos):
                    nums_list, solved_list = generatePuzzle("medium")
                    game_start = False
                if hard_button_rect.collidepoint(event.pos):
                    nums_list, solved_list = generatePuzzle("hard")
                    game_start = False

    while game_over:
        if strikes > 2:
            drawLoseMessage()
        else:
            drawWinMessage()
        restart_message = font.render("Enter 'p' to play again", True, black, white)
        screen.blit(restart_message, (190, 10))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_start = True
                    game_over = False

                    for index in range(len(marked_list)):
                        for index2 in range(len(marked_list[index])):
                            marked_list[index][index2] = 0

                    strikes = 0
                    selected_rect = None
                    break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mark_button_rect.collidepoint(event.pos):
                mark = not mark
            for rect in rect_list:
                if rect.collidepoint(event.pos):
                    selected_rect = rect
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                mark = not mark
            if selected_rect:
                if event.key == pygame.K_0:
                    strikes = number_input(0, strikes)
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

    drawSudokuGrid(selected_rect)
    drawMarkButton()
    drawStrikes()

    if strikes > 2:
        game_over = True

    if nums_list == solved_list and not game_start:
        game_over = True

    pygame.display.flip()