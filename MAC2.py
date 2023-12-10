class SudokuCSP:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.branch_counter = 0

    def is_valid(self, board, row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True

    def find_empty_cell(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def revise(self, board, i, j, x, y):
        revised = False
        for a in range(1, 10):
            if a != board[i][j]:
                continue
            consistent = False
            for b in range(1, 10):
                if b != board[x][y]:
                    consistent = True
                    break
            if not consistent:
                board[i][j] = 0
                revised = True
        return revised

    def ac3(self, board):
        queue = []
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    continue
                for x in range(9):
                    if x == i:
                        continue
                    queue.append((i, j, x, j))
                for y in range(9):
                    if y == j:
                        continue
                    queue.append((i, j, i, y))
        while queue:
            i, j, x, y = queue.pop(0)
            if self.revise(board, i, j, x, y):
                if not any(cell[0] == x and cell[1] == y for cell in queue):
                    queue.append((x, y, x, y))

    def _solve_maintaining_arc_consistency(self, board):
        empty_cell = self.find_empty_cell(board)
        if not empty_cell:
            return True
        row, col = empty_cell
        for num in range(1, 10):
            if self.is_valid(board, row, col, num):
                board[row][col] = num
                self.ac3(board)
                if self._solve_maintaining_arc_consistency(board):
                    self.branch_counter += 1
                    return True
                board[row][col] = 0
        return False

    def solve_maintaining_arc_consistency(self):
        board = [row[:] for row in self.puzzle]
        if not self._solve_maintaining_arc_consistency(board):
            return None
        return board


def is_valid_sudoku(board):
    # التحقق من الصفوف والأعمدة
    for i in range(9):
        row_set = set()
        col_set = set()
        for j in range(9):
            # التحقق من الصف
            if board[i][j] != 0:
                if board[i][j] in row_set:
                    return False
                row_set.add(board[i][j])
            # التحقق من العمود
            if board[j][i] != 0:
                if board[j][i] in col_set:
                    return False
                col_set.add(board[j][i])

    # التحقق من القطاعات الصغيرة (3x3)
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            sector_set = set()
            for x in range(3):
                for y in range(3):
                    if board[i + x][j + y] != 0:
                        if board[i + x][j + y] in sector_set:
                            return False
                        sector_set.add(board[i + x][j + y])

    return True


def print_sudoku(grid):
    for row in grid:
        print(row)


def solve_sudoku_puzzle(puzzle):
    if not is_valid_sudoku(puzzle):
        print("No solution found.")
        return

    sudoku_csp = SudokuCSP(puzzle)
    solved_arc_consistency = sudoku_csp.solve_maintaining_arc_consistency()
    if solved_arc_consistency is None:
        print("لا يوجد حل لهذه اللوحة.")
    else:
        print("Original Sudoku:")
        print_sudoku(puzzle)
        print("\nSolved Sudoku using Maintaining Arc-Consistency:")
        print_sudoku(solved_arc_consistency)
        print("Expanded Nodes:", sudoku_csp.branch_counter)

# استخدم اللوحة الأصلية هنا
board = [
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

solve_sudoku_puzzle(board)
