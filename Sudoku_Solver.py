import numpy as np
import pygame
import time
import random

pygame.font.init()

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

    def delete(self):
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
            self.delete()
        else:
            for i in range(3):
                self.board[row[i]][col[i]] = prev_val[i]
            self.num_sol = 0
            return True

board_complete = Board(9, 9)

val_board = board_complete.create()

board_game = Board(9,9)
board_game.board = board_complete.board.copy()

board_game.delete()

print(board_complete.board)
print(board_game.board)

# https://github.com/techwithtim/Sudoku-GUI-Solver
