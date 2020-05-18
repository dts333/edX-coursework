import sys


class Constraint:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def check(self, sudoku):
        if sudoku.sudoku[x] == sudoku.sudoku[y]:
            return False
        else:
            return True


ROWS = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
SQUARES = [['A1', 'A2', 'A3', 'B1', 'B2']]
CONSTRAINTS = []
used_rows = []
for row in ROWS:
    used_rows.append(row)
    for i in range(1, 10):
        for j in range(i+1, 10):
            CONSTRAINTS.append(Constraint(f"{row}{i}", f"{row}{j}"))
        for r in ROWS:
            if r not in used_rows:
                CONSTRAINTS.append(Constraint(f"{row}{i}", f"{r}{i}"))
for s1 in range(3):
    for s2 in range(3):
        for i in range(1, 4):
            if i == 1:
                y = [2, 3]
            elif i == 2:
                y = [1, 3]
            else:
                y = [1, 2]
            CONSTRAINTS.append(Constraint(f"{ROW[3*s1]}{i+3*s2}", f"{ROW[3*s1+1]}{y[0]+3*s2}"))
            CONSTRAINTS.append(Constraint(f"{ROW[3*s1]}{i+3*s2}", f"{ROW[3*s1+1]}{y[1]+3*s2}"))
            CONSTRAINTS.append(Constraint(f"{ROW[3*s1]}{i+3*s2}", f"{ROW[3*s1+2]}{y[0]+3*s2}"))
            CONSTRAINTS.append(Constraint(f"{ROW[3*s1]}{i+3*s2}", f"{ROW[3*s1+2]}{y[1]+3*s2}"))
            CONSTRAINTS.append(Constraint(f"{ROW[3*s1+1]}{i+3*s2}", f"{ROW[3*s1+2]}{y[0]+3*s2}"))
            CONSTRAINTS.append(Constraint(f"{ROW[3*s1+1]}{i+3*s2}", f"{ROW[3*s1+2]}{y[1]+3*s2}"))


class Sudoku:
    def __init__(self, board):
        self.domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.sudoku = {}
        for i in range(9):
            for j in range(9):
                self.sudoku[f"{ROWS[i]}{j+1}"] = board[9 * i + j]
        self.D = {}
        for key in self.sudoku.keys():
            if self.sudoku[key] == 0:
                self.D[key] = [i for i in self.domain]
            else:
                self.D[key] = [self.sudoku[key]]
    

    def arc_reduce(self, x, y):
        change = False
        for vx in self.D[x]:
            prob = True
            for vy in self.D[y]:
                if vx != vy:
                    prob = False
                    break
            if prob:
                self.D[x].remove(vx)
                change = True

        return change

def ac3(sudoku):
    q = queue.SimpleQueue()
    for c in CONSTRAINTS:
        q.put(c)
    while not q.empty():
        c = q.get()
        if sudoku.arc_reduce(c.x, c.y):
            if len[sudoku.D[c.x]] == 0:
                return False
            for c2 in CONSTRAINTS:
                if (c.x == c2.x) or (c.x == c2.y):
                    if not (c.y == c2.y):
                        q.put(c2)
    
    return True

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
