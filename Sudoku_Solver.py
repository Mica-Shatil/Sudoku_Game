import numpy as np
import pygame
import time

pygame.font.init()


class Board:

    def __init__(self, rows, columns):
        self.rows = rows
        self.cols = columns
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

    def solve(self):
        row, col, box_x, box_y = self.find(self.board)
        if (row == -1):
            return 1
        for i in range(1, 10):
            if (self.check_val(i, row, col, box_x, box_y)):
                self.board[row][col] = i
                if (self.solve() == 1):
                    return 1
                self.board[row][col] = 0
        return 2

    def randomize_grid(self):
        rand_r = [np.random.randint(0, 3), np.random.randint(
            3, 6), np.random.randint(6, 9)]
        rand_c = [np.random.randint(0, 3), np.random.randint(
            3, 6), np.random.randint(6, 9)]
        for cycle in range(2):
            if (cycle == 0):
                for i in range(3):
                    for j in range(9):
                        numbers_tried = {0}
                        temp = np.random.randint(1, 10)
                        while (self.check_val(temp, rand_r[i], j, rand_r[i] % 3, j % 3) == False and len(numbers_tried) < 9):
                            numbers_tried.add(temp)
                            temp = np.random.randint(1, 10)
                        if (self.check_val(temp, j, rand_c[i], j % 3, rand_c[i] % 3) == False):
                            return False
                        self.board[rand_r[i]][j]= temp
            else:
                for i in range(3):
                    for j in range(0, 9):
                        numbers_tried = {0}
                        if (self.board[j][rand_c[i]] == 0):
                            temp = np.random.randint(1, 10)
                            while (self.check_val(temp, j, rand_c[i], j % 3, rand_c[i] % 3) == False and len(numbers_tried) < 9):
                                numbers_tried.add(temp)
                                temp = np.random.randint(1, 10)
                            if (self.check_val(temp, j, rand_c[i], j % 3, rand_c[i] % 3) == False):
                                return False
                            self.board[j][rand_c[i]] = temp
        return True


class Game:

    def __init__(self, rows, columns, width, height, board):
        self.rows = rows
        self.cols = columns
        self.board = board
        #self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        #self.width = width
        #self.height = height
        #self.model = None
        # self.update_model()
        #self.selected = None


board1 = Board(9, 9)

val_board = board1.randomize_grid()

if (val_board == True):
    print("There is a board")
else:
    print("The board was bad")


"""
game1 = Game(9, 9, 540, 540, board1.board)

x = game1.solve()
sol = 0

while (x != 2):
    sol += x
    x = game1.solve()

if (x == 1):
    print("there are thi many solutions: ")
    print(sol)
else:
    print("there is no solution")

"""

# https://github.com/techwithtim/Sudoku-GUI-Solver
