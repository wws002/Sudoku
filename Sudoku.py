import pygame
import requests

# initialize grid dimensions
width = 560
grid_width = 540
height = 650
grid_height = 540
sudokuBlockSize = int(grid_width / 9)

# define color scheme
black = (0, 0, 0)
red = (246, 159, 157)
grey = (128, 128, 128)
green = (130, 201, 36)
blue = (21, 92, 153)
background = (208, 244, 245)

# define variables
selected_rect = None
game_over = False
mark = False
highlight = False
clear = False
new_game = False
game_start = True
strikes = 0

# initialize pygame
pygame.init()
small_font = pygame.font.SysFont(None, 25)
font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 60)
marked_font = pygame.font.SysFont(None, 18)
bold_marked_font = pygame.font.SysFont(None, 22, True)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sudoku")

# initialize rects
new_game_button_rect = pygame.Rect(10, 5, 120, 30)
mark_button_rect = pygame.Rect(10, height - 65, 90, 60)
highlight_current_row_column_button_rect = pygame.Rect(110, height - 65, 340, 60)
clear_cell_button_rect = pygame.Rect(460, height - 65, 90, 60)
easy_button_rect = pygame.Rect(width // 5, height // 2, 90, 60)
medium_button_rect = pygame.Rect(width // 2 - 45, height // 2, 90, 60)
hard_button_rect = pygame.Rect(width - width // 5 - 90, height // 2, 90, 60)
rect_list = []
for x in range(10, grid_width + 10, sudokuBlockSize):
    for y in range(40, grid_height + 40, sudokuBlockSize):
        rect = pygame.Rect(x, y, sudokuBlockSize, sudokuBlockSize)
        rect_list.append(rect)

# define indices for rows, columns, and quadrants
rows = [
    [0,  9, 18, 27, 36, 45, 54, 63, 72],
    [1, 10, 19, 28, 37, 46, 55, 64, 73],
    [2, 11, 20, 29, 38, 47, 56, 65, 74],
    [3, 12, 21, 30, 39, 48, 57, 66, 75],
    [4, 13, 22, 31, 40, 49, 58, 67, 76],
    [5, 14, 23, 32, 41, 50, 59, 68, 77],
    [6, 15, 24, 33, 42, 51, 60, 69, 78],
    [7, 16, 25, 34, 43, 52, 61, 70, 79],
    [8, 17, 26, 35, 44, 53, 62, 71, 80]
]

columns = [
    [ 0,  1,  2,  3,  4,  5,  6,  7,  8],
    [ 9, 10, 11, 12, 13, 14, 15, 16, 17],
    [18, 19, 20, 21, 22, 23, 24, 25, 26],
    [27, 28, 29, 30, 31, 32, 33, 34, 35],
    [36, 37, 38, 39, 40, 41, 42, 43, 44],
    [45, 46, 47, 48, 49, 50, 51, 52, 53],
    [54, 55, 56, 57, 58, 59, 60, 61, 62],
    [63, 64, 65, 66, 67, 68, 69, 70, 71],
    [72, 73, 74, 75, 76, 77, 78, 79, 80]
]

quadrants = [
    [ 0,  1,  2,  9, 10, 11, 18, 19, 20],
    [ 3,  4,  5, 12, 13, 14, 21, 22, 23],
    [ 6,  7,  8, 15, 16, 17, 24, 25, 26],
    [27, 28, 29, 36, 37, 38, 45, 46, 47],
    [30, 31, 32, 39, 40, 41, 48, 49, 50],
    [33, 34, 35, 42, 43, 44, 51, 52, 53],
    [54, 55, 56, 63, 64, 65, 72, 73, 74],
    [57, 58, 59, 66, 67, 68, 75, 76, 77],
    [60, 61, 62, 69, 70, 71, 78, 79, 80]
]

# functions
def generatePuzzle(difficulty):
    api_url = f'https://api.api-ninjas.com/v1/sudokugenerate?difficulty={difficulty}'
    response = requests.get(api_url, headers={'X-Api-Key': 'd+raljYygqWEImdv++PFMg==R0f8jFUTLXMey3oM'})
    values = response.json()['puzzle']
    solutions = response.json()['solution']
    nums_list = []
    solved_list = []
    marked_list = [[0, 0, 0, 0, 0, 0, 0, 0, 0] for _ in range(81)]

    for inner_list in values:
        nums_list.extend(inner_list)

    for index in range(len(nums_list)):
        if not nums_list[index]:
            nums_list[index] = 0

    for inner_list in solutions:
        solved_list.extend(inner_list)

    return nums_list, solved_list, marked_list

def drawSudokuGrid(selected_rect):
    for x in range(10, grid_width + 10, sudokuBlockSize * 3):
        for y in range(40, grid_height + 40, sudokuBlockSize * 3):
            rect = pygame.Rect(x, y, sudokuBlockSize * 3, sudokuBlockSize * 3)
            pygame.draw.rect(screen, black, rect, 3)

    if selected_rect:
        current_row = getCurrentRow()
        current_column = getCurrentColumn()

        for rect in rect_list:
            if rect == selected_rect:
                if not nums_list[rect_list.index(selected_rect)]:
                    pygame.draw.rect(screen, grey, rect, 6)
                elif nums_list[rect_list.index(selected_rect)] == solved_list[rect_list.index(selected_rect)]:
                    pygame.draw.rect(screen, green, rect, 6)
                    for index in range(len(nums_list)):
                        if nums_list[index] == nums_list[rect_list.index(selected_rect)] and rect_list[index] != selected_rect:
                            pygame.draw.rect(screen, black, rect_list[index], 6)
                else:
                    pygame.draw.rect(screen, red, rect, 6)
            elif (rect_list.index(rect) in current_column or rect_list.index(rect) in current_row) and highlight:
                pygame.draw.rect(screen, blue, rect, 6)
            else:
                pygame.draw.rect(screen, black, rect, 1)
    else:
        for rect in rect_list:
            pygame.draw.rect(screen, black, rect, 1)

    for index in range(len(rect_list)):
        if nums_list[index]:
            number_image = font.render(str(nums_list[index]), True, black, background)
            margin_x = (sudokuBlockSize-1 - number_image.get_width()) // 2
            margin_y = (sudokuBlockSize-1 - number_image.get_height()) // 2
            screen.blit(number_image, (rect_list[index].x + 2 + margin_x, rect_list[index].y + 2 + margin_y))
        else:
            for x in range(3):
                if selected_rect:
                    if marked_list[index][x] and marked_list[index][x] == nums_list[rect_list.index(selected_rect)]:
                        bold_marked_number_image = bold_marked_font.render(str(marked_list[index][x]), True, blue, background)
                        screen.blit(bold_marked_number_image, (rect_list[index].x + 5 + x * 20, rect_list[index].y + 5))
                    elif marked_list[index][x]:
                        marked_number_image = marked_font.render(str(marked_list[index][x]), True, black, background)
                        screen.blit(marked_number_image, (rect_list[index].x + 5 + x * 20, rect_list[index].y + 5))
                elif marked_list[index][x]:
                    marked_number_image = marked_font.render(str(marked_list[index][x]), True, black, background)
                    screen.blit(marked_number_image, (rect_list[index].x + 5 + x * 20, rect_list[index].y + 5))
            for x in range(3):
                if selected_rect:
                    if marked_list[index][x+3] and marked_list[index][x+3] == nums_list[rect_list.index(selected_rect)]:
                        bold_marked_number_image = bold_marked_font.render(str(marked_list[index][x+3]), True, blue, background)
                        screen.blit(bold_marked_number_image, (rect_list[index].x + 5 + x * 20, rect_list[index].y + 25))
                    elif marked_list[index][x+3]:
                        marked_number_image = marked_font.render(str(marked_list[index][x+3]), True, black, background)
                        screen.blit(marked_number_image, (rect_list[index].x + 5 + x * 20, rect_list[index].y + 25))
                elif marked_list[index][x+3]:
                    marked_number_image = marked_font.render(str(marked_list[index][x+3]), True, black, background)
                    screen.blit(marked_number_image, (rect_list[index].x + 5 + x * 20, rect_list[index].y + 25))
            for x in range(3):
                if selected_rect:
                    if marked_list[index][x+6] and marked_list[index][x+6] == nums_list[rect_list.index(selected_rect)]:
                        bold_marked_number_image = bold_marked_font.render(str(marked_list[index][x+6]), True, blue, background)
                        screen.blit(bold_marked_number_image, (rect_list[index].x + 5 + x * 20, rect_list[index].y + 45))
                    elif marked_list[index][x+6]:
                        marked_number_image = marked_font.render(str(marked_list[index][x+6]), True, black, background)
                        screen.blit(marked_number_image, (rect_list[index].x + 5 + x * 20, rect_list[index].y + 45))
                elif marked_list[index][x+6]:
                    marked_number_image = marked_font.render(str(marked_list[index][x+6]), True, black, background)
                    screen.blit(marked_number_image, (rect_list[index].x + 5 + x * 20, rect_list[index].y + 45))

def drawStrikes():
    strike_text_image = font.render(f"{strikes}/3 Errors", True, black)
    screen.blit(strike_text_image, (460, 10))

def drawWinMessage():
    win_text_image = big_font.render("You Win!", True, black, background)
    screen.blit(win_text_image, (width // 2 - win_text_image.get_width() // 2, height //2))

def drawLoseMessage():
    lose_text_image = big_font.render("You lost", True, black, background)
    screen.blit(lose_text_image, (width // 2 - lose_text_image.get_width() // 2, height // 2))

def drawMarkButton():
    mark_button_text_image = font.render("Mark", True, black, background)
    if mark:
        pygame.draw.rect(screen, red, mark_button_rect, 6)
        screen.blit(mark_button_text_image, (mark_button_rect.x + 20, mark_button_rect.y + 20))
    else:
        pygame.draw.rect(screen, black, mark_button_rect, 3)
        screen.blit(mark_button_text_image, (mark_button_rect.x + 20, mark_button_rect.y + 20))

def drawHighlightCurrentRowColumnButton():
    highlight_current_row_column_text_image = small_font.render("Highlight Current Row and Column", True, black, background)
    if highlight:
        pygame.draw.rect(screen, red, highlight_current_row_column_button_rect, 6)
        screen.blit(highlight_current_row_column_text_image, (highlight_current_row_column_button_rect.x + 30, highlight_current_row_column_button_rect.y + 20))
    else:
        pygame.draw.rect(screen, black, highlight_current_row_column_button_rect, 3)
        screen.blit(highlight_current_row_column_text_image, (highlight_current_row_column_button_rect.x + 30, highlight_current_row_column_button_rect.y + 20))

def drawClearCellButton(clear):
    clear_cell_button_text_image = font.render("Clear", True, black, background)

    if clear:
        pygame.draw.rect(screen, red, clear_cell_button_rect, 6)
        screen.blit(clear_cell_button_text_image, (clear_cell_button_rect.x + 20, clear_cell_button_rect.y + 20))
        pygame.display.flip()
        pygame.time.wait(300)
    else:
        pygame.draw.rect(screen, black, clear_cell_button_rect, 3)
        screen.blit(clear_cell_button_text_image, (clear_cell_button_rect.x + 20, clear_cell_button_rect.y + 20))

    return False

def drawEasyButton():
    easy_button_text_image = font.render("Easy", True, black, background)
    pygame.draw.rect(screen, black, easy_button_rect, 1)
    screen.blit(easy_button_text_image, (easy_button_rect.x + 20, easy_button_rect.y + 20))

def drawMediumButton():
    medium_button_text_image = font.render("Medium", True, black, background)
    pygame.draw.rect(screen, black, medium_button_rect, 1)
    screen.blit(medium_button_text_image, (medium_button_rect.x + 8, medium_button_rect.y + 20))

def drawHardButton():
    hard_button_text_image = font.render("Hard", True, black, background)
    pygame.draw.rect(screen, black, hard_button_rect, 1)
    screen.blit(hard_button_text_image, (hard_button_rect.x + 20, hard_button_rect.y + 20))

def drawNewGameButton(new_game):
    new_game_button_text_image = font.render("New Game", True, black, background)

    if new_game:
        pygame.draw.rect(screen, red, new_game_button_rect, 6)
        screen.blit(new_game_button_text_image, (new_game_button_rect.x + 10, new_game_button_rect.y + 5))
        drawClearCellButton(False)
        pygame.display.flip()
        pygame.time.wait(300)
    else: 
        pygame.draw.rect(screen, black, new_game_button_rect, 3)
        screen.blit(new_game_button_text_image, (new_game_button_rect.x + 10, new_game_button_rect.y + 5))
    
    return False

def getCurrentRow():
    for row in rows:
        if rect_list.index(selected_rect) in row:
            return row

def getCurrentColumn():
    for column in columns:
        if rect_list.index(selected_rect) in column:
            return column
        
def getCurrentQuadrant():
    for quadrant in quadrants:
        if rect_list.index(selected_rect) in quadrant:
            return quadrant

def cleanMarksList(number):
    current_quadrant = getCurrentQuadrant()
    current_row = getCurrentRow()
    current_column = getCurrentColumn()

    for index in current_quadrant:
        for index2 in range(len(marked_list[index])):
            if marked_list[index][index2] == number:
                marked_list[index][index2] = 0

    for index in current_row:
        for index2 in range(len(marked_list[index])):
            if marked_list[index][index2] == number:
                marked_list[index][index2] = 0

    for index in current_column:
        for index2 in range(len(marked_list[index])):
            if marked_list[index][index2] == number:
                marked_list[index][index2] = 0

def resetGame():
    game_start = True
    game_over = False
    strikes = 0
    selected_rect = None
    marked_list = [[0, 0, 0, 0, 0, 0, 0, 0, 0] for _ in range(81)]

    return game_start, game_over, strikes, selected_rect, marked_list

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
    elif solved_list[rect_list.index(selected_rect)] != number and nums_list[rect_list.index(selected_rect)] != number:
        strikes += 1
        nums_list[rect_list.index(selected_rect)] = number
    else:
        nums_list[rect_list.index(selected_rect)] = number
        cleanMarksList(number)

    return strikes

# main loop
while True: 
    screen.fill(background)

    # loop for start of game
    while game_start:
        welcome_text_image = big_font.render("Let's play Sudoku!", True, black, background)
        difficulty_select_text_image = font.render("Choose difficulty", True, black, background)
        screen.blit(welcome_text_image, (width // 2 - welcome_text_image.get_width() // 2, height // 6))
        screen.blit(difficulty_select_text_image, (width // 2 - difficulty_select_text_image.get_width() // 2, height // 3))
        drawEasyButton()
        drawMediumButton()
        drawHardButton()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button_rect.collidepoint(event.pos):
                    nums_list, solved_list, marked_list = generatePuzzle("easy")
                    game_start = False
                if medium_button_rect.collidepoint(event.pos):
                    nums_list, solved_list, marked_list = generatePuzzle("medium")
                    game_start = False
                if hard_button_rect.collidepoint(event.pos):
                    nums_list, solved_list, marked_list = generatePuzzle("hard")
                    game_start = False

    # loop for end of game
    while game_over:
        if strikes > 2:
            drawLoseMessage()
        else:
            drawWinMessage()
        restart_message_image = font.render("Enter 'p' to play again", True, black, background)
        screen.blit(restart_message_image, (width // 2 - restart_message_image.get_width() // 2, 10))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_start, game_over, strikes, selected_rect, marked_list = resetGame()
                    break

    # main event detection loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mark_button_rect.collidepoint(event.pos):
                mark = not mark
            if highlight_current_row_column_button_rect.collidepoint(event.pos):
                highlight = not highlight
            if new_game_button_rect.collidepoint(event.pos):
                new_game = True
                game_start, game_over, strikes, selected_rect, marked_list = resetGame()
            if clear_cell_button_rect.collidepoint(event.pos):
                clear = True
                if selected_rect:
                    for index in range(len(marked_list[rect_list.index(selected_rect)])):
                        marked_list[rect_list.index(selected_rect)][index] = 0
            for rect in rect_list:
                if rect.collidepoint(event.pos):
                    if rect != selected_rect:
                        selected_rect = rect
                    else:
                        selected_rect = None
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                selected_rect = None
            if event.key == pygame.K_m:
                mark = not mark
            if event.key == pygame.K_h:
                highlight = not highlight
            if event.key == pygame.K_c:
                clear = True
                if selected_rect:
                    for index in range(len(marked_list[rect_list.index(selected_rect)])):
                        marked_list[rect_list.index(selected_rect)][index] = 0
            if event.key == pygame.K_UP:
                if not selected_rect:
                    selected_rect = rect_list[0]
                elif rect_list.index(selected_rect) not in rows[0]:
                    selected_rect = rect_list[rect_list.index(selected_rect) - 1]
            if event.key == pygame.K_DOWN:
                if not selected_rect:
                    selected_rect = rect_list[0]
                elif rect_list.index(selected_rect) not in rows[8]:
                    selected_rect = rect_list[rect_list.index(selected_rect) + 1]
            if event.key == pygame.K_RIGHT:
                if not selected_rect:
                    selected_rect = rect_list[0]
                elif rect_list.index(selected_rect) not in columns[8]:
                    selected_rect = rect_list[rect_list.index(selected_rect) + 9]
            if event.key == pygame.K_LEFT:
                if not selected_rect:
                    selected_rect = rect_list[0]
                elif rect_list.index(selected_rect) not in columns[0]:
                    selected_rect = rect_list[rect_list.index(selected_rect) - 9]
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

    # draw grid, strikes, and buttons
    drawSudokuGrid(selected_rect)
    drawMarkButton()
    drawHighlightCurrentRowColumnButton()
    drawStrikes()
    new_game = drawNewGameButton(new_game)
    clear = drawClearCellButton(clear)

    # check for win-lose conditions
    if strikes > 2:
        game_over = True

    if nums_list == solved_list and not game_start:
        game_over = True

    # update display
    pygame.display.flip()