import pygame
from copy import deepcopy

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 800
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Example Sudoku board (0 represents empty cells)
default_sudoku = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Initialize the pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SUDOKU")

pygame.font.init() 
my_font = pygame.font.SysFont('New York Times', 30)

def find_space(sudoku):
    for row in range(9):
        for column in range(9):
            if sudoku[row][column] == 0:
                return row, column
    return False

def is_in_row(sudoku, num_to_check, row, column): #checks the row whether the number is already used or not
    for i in range(9):
        if sudoku[row][i] == num_to_check and i != column:
            return True
    return False

def is_in_column(sudoku, num_to_check, row, column): #checks the column whether the number is already used or not
    for i in range(9):
        if sudoku[i][column] == num_to_check and i != row:
            return True
    return False

def is_in_group(sudoku, num_to_check, row, column): #checks the group whether the number is already used or not
    for i in range((column // 3) * 3,  (column // 3) * 3 + 3 ):
        for j in range((row // 3) * 3, (row // 3) * 3 + 3 ):
            if sudoku[j][i] == num_to_check and (i, j) != (column, row):
                return True
    return False

def is_it_valid(sudoku, num_to_check, row, column): #uses the three methods above and returns a boolen whether the number is usable or not
    in_column = is_in_column(sudoku, num_to_check, row, column)
    in_row = is_in_row(sudoku, num_to_check, row, column)
    in_group = is_in_group(sudoku, num_to_check, row, column)
    if not (in_column or in_row or in_group):
        return True
    return False

def solve(sudoku):
    global solved_sudoku
    solved_sudoku = deepcopy(sudoku)
    space = find_space(solved_sudoku)
    if not space :
        return True
    else:
        row, column = space

    for num_to_check in range(1,10):
        if is_it_valid(solved_sudoku, num_to_check, row, column):
            solved_sudoku[row][column] = num_to_check
            
            if solve(solved_sudoku):
                return True
            solved_sudoku[row][column] = 0
    return False

def draw_grid():
    for i in range(1, GRID_SIZE): 
        thickness = 4 if i % 3 == 0 else 1
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH), thickness)
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), thickness)
    pygame.draw.line(screen, BLACK, (0, GRID_SIZE * CELL_SIZE+4), (WIDTH, GRID_SIZE * CELL_SIZE+4), 4)

def draw_numbers(board):
    font = pygame.font.Font(None, 36)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] != 0:
                text = font.render(str(board[row][col]), True, BLACK)
                text_rect = text.get_rect(center=(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text, text_rect)

def draw_buttons(screen):
    # clean button
    global sudoku_clean_button
    sudoku_clean_button = pygame.Rect((WIDTH//4 -75), (WIDTH + (HEIGHT - WIDTH) // 2-20), WIDTH//4, 50)
    sudoku_clean = my_font.render('Clean Sudoku', True, WHITE)
    sudoku_clean_Rect = sudoku_clean.get_rect()
    sudoku_clean_Rect.center = sudoku_clean_button.center
    pygame.draw.rect(screen, BLACK, sudoku_clean_button)
    screen.blit(sudoku_clean, sudoku_clean_Rect)

    # solve button
    global sudoku_solve_button
    sudoku_solve_button = pygame.Rect((3*WIDTH//4 - 75), (WIDTH + (HEIGHT - WIDTH) // 2-20), WIDTH//4, 50)
    sudoku_solve = my_font.render('Solve Sudoku', True, WHITE)
    sudoku_solve_Rect = sudoku_solve.get_rect()
    sudoku_solve_Rect.center = sudoku_solve_button.center
    pygame.draw.rect(screen, BLACK, sudoku_solve_button)
    screen.blit(sudoku_solve, sudoku_solve_Rect)

def main():
    global default_sudoku
    button_clicked = None
    running = True

    screen.fill(WHITE)
    draw_grid()
    draw_numbers(default_sudoku)
    draw_buttons(screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if sudoku_clean_button.collidepoint(mouse):
                    button_clicked = 'clean'
                elif sudoku_solve_button.collidepoint(mouse):
                    button_clicked = 'solve'
                else:
                    mouse_x, mouse_y = mouse
                    clicked_col = mouse_x // CELL_SIZE
                    clicked_row = mouse_y // CELL_SIZE

                    # if the mouse click is inside the sudoku
                    if clicked_col <= 9 and clicked_row <= 9:
                        waiting_for_key = True

                    while waiting_for_key:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                
                                # if an integer between 0 and 9 is pressed
                                if event.unicode.isdigit() and 0 <= int(event.unicode) <= 9:
                                    default_sudoku[clicked_row][clicked_col] = int(event.unicode)
                                    draw_numbers(default_sudoku)

                                waiting_for_key = False


        

        if button_clicked == 'solve':
            if solve(default_sudoku):
                default_sudoku = deepcopy(solved_sudoku)
                draw_numbers(solved_sudoku)
                print("Solved")
            button_clicked = None
        elif button_clicked == 'clean':
            default_sudoku = [[0 for _ in range(9)] for _ in range(9)]
            button_clicked = None

        screen.fill(WHITE)
        draw_grid()
        draw_numbers(default_sudoku)
        draw_buttons(screen)
        pygame.display.flip()
        pygame.display.update()

if __name__ == "__main__":
    main()
