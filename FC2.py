class SudokuSolver:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.nodes_count = 0

    def is_valid(self, row, col, num):
        for i in range(9):
            if self.puzzle[row][i] == num or self.puzzle[i][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.puzzle[start_row + i][start_col + j] == num:
                    return False
        return True

    def is_valid_board(self):
        for i in range(9):
            for j in range(9):
                if self.puzzle[i][j] != 0:
                    num = self.puzzle[i][j]
                    self.puzzle[i][j] = 0
                    if not self.is_valid(i, j, num):
                        return False
                    self.puzzle[i][j] = num
        return True

    def solve_forward_checking(self):
        if not self.is_valid_board():
            return False

        if not self.find_empty():
            return True

        row, col = self.find_empty()
        valid_values = self.get_valid_values(row, col)

        if not valid_values:
            return False

        for num in valid_values:
            self.puzzle[row][col] = num
            self.nodes_count += 1
            if self.solve_forward_checking():
                return True

            self.puzzle[row][col] = 0

        return False

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.puzzle[i][j] == 0:
                    return i, j
        return None

    def get_valid_values(self, row, col):
        valid_values = []
        for num in range(1, 10):
            if self.is_valid(row, col, num):
                valid_values.append(num)
        return valid_values

    def solve(self, algorithm='forward_checking'):
        self.nodes_count = 0

        if algorithm == 'forward_checking':
            if self.solve_forward_checking():
                return self.puzzle, self.nodes_count
            else:
                return None, self.nodes_count

# مثال على لعبة Sudoku
sudoku_puzzle = [
    [0, 0, 5, 3, 0, 0, 0, 0, 0],
    [8, 0, 0, 0, 0, 0, 0, 2, 0],
    [0, 7, 0, 0, 1, 0, 5, 0, 0],
    [4, 0, 0, 0, 0, 5, 3, 0, 0],
    [0, 1, 0, 0, 7, 0, 0, 0, 6],
    [0, 0, 3, 2, 0, 0, 0, 8, 0],
    [0, 6, 0, 5, 0, 0, 0, 0, 9],
    [0, 0, 4, 0, 0, 0, 0, 3, 0],
    [0, 0, 0, 0, 0, 9, 7, 0, 0]
]

solver = SudokuSolver(sudoku_puzzle)
result, nodes_count = solver.solve('forward_checking')
if result:
    for row in result:
        print(row)
    print("Nodes branched:", nodes_count)
else:
    print("No valid solution found.")
