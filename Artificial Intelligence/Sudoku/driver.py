import sys


class Sudoku:
    def __init__(self, board):
        rows = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
        self.domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.sudoku = {}
        for i in range(9):
            for j in range(9):
                self.sudoku[f"{rows[i]}{j+1}"] = board[9 * i + j]

def ac3(sudoku):
    #To-do

def bts(sudoku):
    #To-do

def solved(board):
    if '0' in board:
        return False
    else:
        return True


if __name__ == "__main__":
    board = sys.argv[1]
    sudoku = Sudoku(board)
    assignment = ac3(sudoku)
    if solved(assignment):
        assignment += ' AC3'
    else:
        sudoku = Sudoku(board)
        assignment = bts(sudoku)
        assignment += ' BTS'
