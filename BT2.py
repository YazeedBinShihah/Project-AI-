class SudokuSolver:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.nodes_count = 0  # العداد لعدد العقد

    def solve_backtracking(self):
        if not self.find_empty():
            return True

        row, col = self.find_empty()

        for num in range(1, 10):
            self.nodes_count += 1  # زيادة العداد بعد مراجعة جميع الأرقام
            if self.is_valid(row, col, num):
                self.puzzle[row][col] = num
                if self.solve_backtracking():
                    return True
                self.puzzle[row][col] = 0

        return False

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.puzzle[i][j] == 0:
                    return i, j
        return None

    def is_valid(self, row, col, num):
        for i in range(9):
            if self.puzzle[row][i] == num or self.puzzle[i][col] == num:
                self.nodes_count += 1  # زيادة العداد لفحص الصفوف والأعمدة
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.puzzle[start_row + i][start_col + j] == num:
                    self.nodes_count += 1  # زيادة العداد لفحص المربعات الصغيرة
                    return False

        return True

    def is_valid_board(self):
        # التحقق من صحة اللوحة المدخلة
        for i in range(9):
            for j in range(9):
                if self.puzzle[i][j] != 0:
                    num = self.puzzle[i][j]
                    self.puzzle[i][j] = 0
                    if not self.is_valid(i, j, num):
                        return False
                    self.puzzle[i][j] = num
        return True


# مثال على لغز Sudoku
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

if solver.is_valid_board() and solver.solve_backtracking():
    for row in solver.puzzle:
        print(row)
    print("Nodes branched:", solver.nodes_count)
else:
    print("No solution found.")
