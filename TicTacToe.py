import pygame
import sys
import time

pygame.init()
font = pygame.font.Font(None, 72)

# CONSTANTS
WIDTH = HEIGHT = 600            # Window
LINE_WIDTH = 30                 # Grid
WIN_LINE_WIDTH = 30             # Winning Line
BOARD_ROWS = BOARD_COLS = 3     # Rows and cols
SQUARE_SIZE = WIDTH // BOARD_COLS   # Size of square
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 30
CROSS_WIDTH = 50
SPACE = SQUARE_SIZE // 4        # Space around cross/circle

# RGB COLORS
BG_COLOR = (217, 240, 255)
LINE_COLOR = (0, 124, 190)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# Set up window display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE')
screen.fill(BG_COLOR)

# Board
board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Pygame has a different coordinate system
def draw_lines():
    # 1st horizontal
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    # 2nd horizontal
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)

    # 1st vertical
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    # 2nd vertical
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)


def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)


def mark_square(row, col, player):
    board[row][col] = player


def available_square(row, col):
    return board[row][col] is None


def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                return False
    return True


def check_win(player):
    # vertical win check
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True
    # horizontal win check
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True
    # asc diagonal win check
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        return True
    # desc diagonal win check
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True

def restart():
    screen.fill(BG_COLOR)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = None

draw_lines()

# Game variables
player = 'X'
game_over = False

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:

            mouseX = event.pos[0] # X
            mouseY = event.pos[1] # Y

            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE

            if available_square(clicked_row, clicked_col):

                if player == 'X':
                    mark_square(clicked_row, clicked_col, 'X')
                    if check_win(player):
                        game_over = True
                    player = 'O'

                elif player == 'O':
                    mark_square(clicked_row, clicked_col, 'O')
                    if check_win(player):
                        game_over = True
                        win_text = font.render('Player O wins!', True, (255, 255, 255), (0, 0, 255))
                        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))
                    player = 'X'

                draw_figures()

                if game_over:
                    if player == 'O':
                        win_text = font.render('Player X wins!', True, (255, 255, 255), (0, 0, 255))
                    else:
                        win_text = font.render('Player O wins!', True, (255, 255, 255), (0, 0, 255))
                    screen.blit(win_text,
                                (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                player = 'X'
                game_over = False

    pygame.display.flip()
