import numpy as np
import pygame
from pygame.locals import *
import time
import random

class Board:

    def __init__(self, rows, columns):
        self.rows = rows
        self.cols = columns
        self.num_sol = 0
        self.board = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ])

    def find(self, brd):
        for i in range(np.shape(brd)[0]):
            for j in range(np.shape(brd)[1]):
                if (brd[i][j] == 0):
                    return i, j, i % 3, j % 3

        return -1, 0, 0, 0

    def check_val(self, val, row, col, box_row, box_col):

        # check row
        for i in range(len(self.board[row])):
            if (val == self.board[row][i]):
                return False

        # check column
        for i in range(len(self.board[:, col])):
            if (val == self.board[:, col][i]):
                return False

        # checks local box
        if (box_row == 0 and box_col == 0):
            for i in range(row, row+3):
                for j in range(col, col+3):
                    if (val == self.board[i][j]):
                        return False
        elif (box_row == 0 and box_col == 1):
            for i in range(row, row+3):
                for j in range(col-1, col+2):
                    if (val == self.board[i][j]):
                        return False
        elif (box_row == 0 and box_col == 2):
            for i in range(row, row+3):
                for j in range(col-2, col+1):
                    if (val == self.board[i][j]):
                        return False
        elif (box_row == 1 and box_col == 0):
            for i in range(row-1, row+2):
                for j in range(col, col+3):
                    if (val == self.board[i][j]):
                        return False
        elif (box_row == 1 and box_col == 1):
            for i in range(row-1, row+2):
                for j in range(col-1, col+2):
                    if (val == self.board[i][j]):
                        return False
        elif (box_row == 1 and col == 2):
            for i in range(row-1, row+2):
                for j in range(col-2, col+1):
                    if (val == self.board[i][j]):
                        return False
        elif (box_row == 2 and box_col == 0):
            for i in range(row-2, row+1):
                for j in range(col, col+3):
                    if (val == self.board[i][j]):
                        return False
        elif (box_row == 2 and box_col == 1):
            for i in range(row-2, row+1):
                for j in range(col-1, col+2):
                    if (val == self.board[i][j]):
                        return False
        elif (box_row == 2 and box_col == 2):
            for i in range(row-2, row+1):
                for j in range(col-2, col+1):
                    if (val == self.board[i][j]):
                        return False

        return True

    def create(self):
        row, col, box_x, box_y = self.find(self.board)
        if (row == -1):
            return 1
        rand_num = np.array([1,2,3,4,5,6,7,8,9])
        random.shuffle(rand_num)
        for i in range(9):
            if (self.check_val(rand_num[i], row, col, box_x, box_y)):
                self.board[row][col] = rand_num[i]
                if (self.create() == 1):
                    return 1
                self.board[row][col] = 0
        return 2

    def solve(self):
        row, col, box_x, box_y = self.find(self.board)
        if (row == -1):
            return 3
        for i in range(1, 10):
            if (self.check_val(i, row, col, box_x, box_y)):
                self.board[row][col] = i
                if (self.solve() == 3):
                    self.num_sol += 1
                self.board[row][col] = 0
        return 2

    def delete_num(self):
        row = [0,0,0]
        col = [0,0,0]
        prev_val = [0,0,0]
        for i in range(3):
            while (True):
                row[i] = np.random.randint(0,9)
                col[i] = np.random.randint(0,9)
                if (self.board[row[i]][col[i]] != 0):
                    prev_val[i] = self.board[row[i]][col[i]]
                    self.board[row[i]][col[i]] = 0
                    break

        self.solve()

        if (self.num_sol == 1):
            self.num_sol = 0
            self.delete_num()
        else:
            for i in range(3):
                self.board[row[i]][col[i]] = prev_val[i]
            self.num_sol = 0
            return True

class Game():
    board_dim_x = [10, 77, 144, 211, 278, 345, 412, 479, 546, 613]
    board_dim_y = [60, 127, 194, 261, 328, 395, 462, 529, 596, 663]
    board_width = 603
    board_height = 603
    width_shift = 10
    height_shift = 60
    BLACK = (0,0,0)
    BLUE = (0, 160, 210)
    pygame.font.init()
    font_game = pygame.font.Font('freesansbold.ttf', 40)

    def __init__(self, board, game_board):
        self.rows = 9
        self.cols = 9
        self.mistakes = 0
        self.cubes = [[Tile(board[i][j], i, j, Game.board_width, Game.board_height) for j in range(9)] for i in range(9)]
        self.selected = None
        self.cubes_left = self.find_empties()
        self.complete_board = game_board
        self.game_screen = pygame.display.set_mode((623,673))
        pygame.display.set_caption("Random Board Sudoku Game")
        self.game_screen.fill(Game.BLUE)
        pygame.display.update()

    def find_empties(self):
        x = 0
        for i in range(9):
            for j in range(9):
                if self.cubes[i][j].value == 0:
                    x += 1
        
        return x

    def draw_grid(self, start_time):
        self.game_screen.fill(Game.BLUE)

        text = self.font_game.render("Errors: " + str(self.mistakes), 1, (0, 0, 0))
        self.game_screen.blit(text, (10, 10))
        
        for i in range(10):
            if i ==3 or i == 6:
                pygame.draw.lines(self.game_screen, Game.BLACK, False, [(self.board_dim_x[0], self.board_dim_y[i]), (self.board_dim_x[9], self.board_dim_y[i])], 8)
                pygame.draw.lines(self.game_screen, Game.BLACK, False, [(self.board_dim_x[i], self.board_dim_y[0]), (self.board_dim_x[i], self.board_dim_y[9])], 8)
            pygame.draw.lines(self.game_screen, Game.BLACK, False, [(self.board_dim_x[0], self.board_dim_y[i]), (self.board_dim_x[9], self.board_dim_y[i])], 5)
            pygame.draw.lines(self.game_screen, Game.BLACK, False, [(self.board_dim_x[i], self.board_dim_y[0]), (self.board_dim_x[i], self.board_dim_y[9])], 5)

        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.game_screen)

        time_text = self.font_game.render(get_time(round(time.time() - start_time)), 1, (0, 0, 0))
        self.game_screen.blit(time_text, (500, 10))

        pygame.display.update()

    def click_loc(self, pos):
        if pos[0] < 613 and pos[1] < 663:
            gap = Game.board_width / 9
            x = (pos[0] - self.width_shift) // gap
            y = (pos[1] - self.height_shift) // gap
            return (int(y),int(x))
        else:
            return None

    def select(self, row, col):
        if self.cubes[row][col].value == 0:
            for i in range(self.rows):
                for j in range(self.cols):
                    self.cubes[i][j].selected = False
            
            self.cubes[row][col].selected = True
            self.selected = (row, col)

    def check_num (self, key):
        if (self.complete_board[self.selected[0]][self.selected[1]] == key):
            self.cubes_left -= 1
            return True
            
        return False
    
    def update_cube (self, key):
        self.cubes[self.selected[0]][self.selected[1]].value = key
        self.cubes[self.selected[0]][self.selected[1]].selected = False
        self.selected = None

    def update_display(self, scrn):
        text = self.font_game.render(str(self.mistakes), 1, (0, 0, 0))
        scrn.blit(text, (10, 0))

    def fail (self):
        self.mistakes += 1

class Tile():
    rows = 9
    columns = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        font = pygame.font.Font('freesansbold.ttf', 40)

        gap = self.width / 9
        x = (self.col * gap) + 10
        y = (self.row * gap) + 60

        if not(self.value == 0):
            text = font.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val

def get_time(secs):
    sec = secs%60
    minute = secs//60

    mat = str(minute) + ":" + str(sec)
    return mat

def board_completed(game1, start_time):
    endgame = False
    game1.game_screen.fill(Game.BLUE)
    text1 = game1.font_game.render("You Win With " + str(game1.mistakes) + " Mistakes", 1, (0, 0, 0))
    game1.game_screen.blit(text1, (10, 200))
    text2 = game1.font_game.render("And In " + get_time(round (time.time() - start_time)) + " Time", 1, (0, 0, 0))
    game1.game_screen.blit(text2, (10, 250))
    pygame.display.update()

    while not endgame:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == QUIT:
                endgame = True

def main():
    pygame.init()
    pygame.font.init()
    board1 = Board(9, 9)
    val_board = board1.create()
    board_game = Board(9,9)
    board_game.board = board1.board.copy()
    board_game.delete_num()
    game1 = Game(board_game.board.copy(), board1.board.copy())
    end_game = False
    key = None
    start = time.time()
    game1.draw_grid(start)
    game1.update_display(game1.game_screen)
    
    while not end_game:
        if game1.cubes_left == 0:
            board_completed(game1, start)
            end_game = True
        
        pygame.time.delay(100)
        game1.draw_grid(start)

        key = None
        
        for event in pygame.event.get():
            if event.type == QUIT:
                end_game = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                elif event.key == pygame.K_2:
                    key = 2
                elif event.key == pygame.K_3:
                    key = 3
                elif event.key == pygame.K_4:
                    key = 4
                elif event.key == pygame.K_5:
                    key = 5
                elif event.key == pygame.K_6:
                    key = 6
                elif event.key == pygame.K_7:
                    key = 7
                elif event.key == pygame.K_8:
                    key = 8
                elif event.key == pygame.K_9:
                    key = 9
                elif event.key == pygame.K_KP1:
                    key = 1
                elif event.key == pygame.K_KP2:
                    key = 2
                elif event.key == pygame.K_KP3:
                    key = 3
                elif event.key == pygame.K_KP4:
                    key = 4
                elif event.key == pygame.K_KP5:
                    key = 5
                elif event.key == pygame.K_KP6:
                    key = 6
                elif event.key == pygame.K_KP7:
                    key = 7
                elif event.key == pygame.K_KP8:
                    key = 8
                elif event.key == pygame.K_KP9:
                    key = 9
            
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = Game.click_loc(game1, pos)
                if clicked:
                    game1.select(clicked[0], clicked[1])
            elif key != None and game1.selected != None:
                if game1.check_num(key):
                    game1.update_cube(key)
                else:
                    game1.fail()
                
                key = None 
        pygame.display.update()

main()
pygame.quit()

# Initial idea and GUI Inspiration From:
# https://github.com/techwithtim/Sudoku-GUI-Solver
