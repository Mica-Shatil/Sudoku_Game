import numpy as np
import pygame
from pygame.locals import *
import time
import random

# class for boards
class Board:

    def __init__(self, rows, columns):
        self.rows = rows
        self.cols = columns
        self.num_sol = 0 # number of solutions to a board
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

    # finds next empty square
    def find(self, brd):
        for i in range(np.shape(brd)[0]):
            for j in range(np.shape(brd)[1]):
                if (brd[i][j] == 0):
                    return i, j, i % 3, j % 3

        return -1, 0, 0, 0

    # checks to see if val is a valid number in row position (row, col)
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

    # creates a full randomized board
    def create(self):
        row, col, box_x, box_y = self.find(self.board)
        if (row == -1):
            return 1
        rand_num = [1,2,3,4,5,6,7,8,9]
        random.shuffle(rand_num)
        for i in range(9):
            if (self.check_val(rand_num[i], row, col, box_x, box_y)):
                self.board[row][col] = rand_num[i]
                if (self.create() == 1):
                    return 1
                self.board[row][col] = 0
        return 2

    # will count the number of solutions to a baord
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

    # will delete tiles of a board to create a playable board with one solution
    def delete_num(self):
        row = 0
        col = 0
        prev_val = 0
        while (True):
            row = np.random.randint(0,9)
            col = np.random.randint(0,9)
            prev_val = self.board[row][col]
            if (self.board[row][col] != 0):
                self.board[row][col] = 0
                break

        self.solve()

        if (self.num_sol == 1):
            self.num_sol = 0
            self.delete_num()
        else:
            self.board[row][col] = prev_val
            self.num_sol = 0
            return True

# class for games
class Game():
    # points for display grid
    board_dim_x = [10, 77, 144, 211, 278, 345, 412, 479, 546, 613]
    board_dim_y = [60, 127, 194, 261, 328, 395, 462, 529, 596, 663]

    board_width = 603
    board_height = 603
    
    # distance form the end of the window and the start of the grid
    width_shift = 10 
    height_shift = 60
    
    BLACK = (0,0,0)
    BLUE = (0, 160, 210)
    pygame.font.init()
    font_game = pygame.font.Font('freesansbold.ttf', 40)

    def __init__(self, board, game_board):
        self.rows = 9
        self.cols = 9
        self.mistakes = 0 # stores number of mistakes made when trying to solve the board
        self.tiles = [[Tile(board[i][j], i, j, Game.board_width, Game.board_height) for j in range(9)] for i in range(9)] # initialzes and stores tiles
        self.selected = None # selected tile
        self.tiles_left = self.find_empties() # number of tiles that are still empty
        self.complete_board = game_board # stores the full board with the empty tiles filled in
        
        # initialize window
        self.game_screen = pygame.display.set_mode((623,673))
        pygame.display.set_caption("Random Board Sudoku Game")
        self.game_screen.fill(Game.BLUE)
        pygame.display.update()

    # counts the number of empy tiles left
    def find_empties(self):
        x = 0
        for i in range(9):
            for j in range(9):
                if self.tiles[i][j].value == 0:
                    x += 1
        
        return x

    # draws and fills in the grid
    def draw_grid(self, start_time):
        self.game_screen.fill(Game.BLUE)
        
        # draws grid
        for i in range(10):
            if i ==3 or i == 6:
                pygame.draw.lines(self.game_screen, Game.BLACK, False, [(self.board_dim_x[0], self.board_dim_y[i]), (self.board_dim_x[9], self.board_dim_y[i])], 8)
                pygame.draw.lines(self.game_screen, Game.BLACK, False, [(self.board_dim_x[i], self.board_dim_y[0]), (self.board_dim_x[i], self.board_dim_y[9])], 8)
            pygame.draw.lines(self.game_screen, Game.BLACK, False, [(self.board_dim_x[0], self.board_dim_y[i]), (self.board_dim_x[9], self.board_dim_y[i])], 5)
            pygame.draw.lines(self.game_screen, Game.BLACK, False, [(self.board_dim_x[i], self.board_dim_y[0]), (self.board_dim_x[i], self.board_dim_y[9])], 5)

        # fills tiles
        for i in range(self.rows):
            for j in range(self.cols):
                self.tiles[i][j].draw(self.game_screen)

        # writes headers
        text = self.font_game.render("Errors: " + str(self.mistakes), 1, (0, 0, 0))
        self.game_screen.blit(text, (10, 10))
        time_text = self.font_game.render(get_time(round(time.time() - start_time)), 1, (0, 0, 0))
        self.game_screen.blit(time_text, (500, 10))

        pygame.display.update()

    # identifies the tile that a click occurs on
    def click_loc(self, pos):
        if pos[0] < 613 and pos[1] < 663:
            gap = Game.board_width / 9
            x = (pos[0] - self.width_shift) // gap
            y = (pos[1] - self.height_shift) // gap
            return (int(y),int(x))
        else:
            return None

    # selects the tile clicked if the tile is empty
    def select(self, row, col):
        if self.tiles[row][col].value == 0:
            for i in range(self.rows):
                for j in range(self.cols):
                    self.tiles[i][j].selected = False
            
            self.tiles[row][col].selected = True
            self.selected = (row, col)

    # checks key is a valid value for the selected tile
    def check_num (self, key):
        if (self.complete_board[self.selected[0]][self.selected[1]] == key):
            self.tiles_left -= 1
            return True
            
        return False
    
    # updates selected tile to the correct value and deselects it
    def update_cube (self, key):
        self.tiles[self.selected[0]][self.selected[1]].value = key
        self.tiles[self.selected[0]][self.selected[1]].selected = False
        self.selected = None

    # increases mistakes count
    def fail (self):
        self.mistakes += 1

#class for tile
class Tile():
    rows = 9
    columns = 9

    def __init__(self, value, row, col, width, height):
        self.value = value # number value of the tile
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False # whether or not the tile is selected

    # draws the value of the tile and highligth if it is selected
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

# gets the current game time
def get_time(secs):
    sec = secs%60
    minute = secs//60

    mat = str(minute) + ":" + str(sec)
    return mat

# runs the victory sequence
def board_completed(game1, start_time):
    endgame = False
    game1.game_screen.fill(Game.BLUE)
    text1 = game1.font_game.render("You Win With " + str(game1.mistakes) + " Mistakes", 1, (0, 0, 0))
    game1.game_screen.blit(text1, (10, 200))
    text2 = game1.font_game.render("In " + get_time(round (time.time() - start_time)) + " Min", 1, (0, 0, 0))
    game1.game_screen.blit(text2, (10, 250))
    pygame.display.update()

    while not endgame:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == QUIT:
                endgame = True

def main():
    board1 = Board(9, 9) # the completed board
    board1.create()
    board_game = Board(9,9) # the part empty board
    board_game.board = board1.board.copy()
    board_game.delete_num()
    game1 = Game(board_game.board.copy(), board1.board.copy()) # creates game board
    end_game = False
    key = None # key pressed
    start = time.time() # start time
    game1.draw_grid(start)
    
    # main game loop
    while not end_game:
        # checks if the board is completed
        if game1.tiles_left == 0:
            board_completed(game1, start)
            end_game = True
        
        pygame.time.delay(100)
        game1.draw_grid(start)

        key = None # reset key
        
        # check for user interactions
        for event in pygame.event.get():
            if event.type == QUIT: # endgame
                end_game = True
            elif event.type == pygame.KEYDOWN: # key press
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
            
            if event.type == MOUSEBUTTONDOWN: # mouse press
                pos = pygame.mouse.get_pos()
                clicked = Game.click_loc(game1, pos)
                if clicked:
                    game1.select(clicked[0], clicked[1])
            elif key != None and game1.selected != None: # update tiles with key presses
                if game1.check_num(key):
                    game1.update_cube(key)
                else:
                    game1.fail()
                
                key = None 

        pygame.display.update() # update screen

main()
pygame.quit()
