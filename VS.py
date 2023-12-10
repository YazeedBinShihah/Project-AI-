import tkinter as tk
from tkinter import ttk
import threading

class SudokuVisualizer:
    def __init__(self, root, sudoku_board):
        self.root = root
        self.sudoku_board = sudoku_board
        self.text_objects = [[None for _ in range(9)] for _ in range(9)]
        self.bt_nodes_counter = 0
        self.ac3_nodes_counter = 0
        self.fc_nodes_counter = 0
        self.initial_board = [
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
        self.sudoku_board = [row[:] for row in self.initial_board]

        root.title("Sudoku Visualizer")

        root.canvas = tk.Canvas(root, width=450, height=450)
        root.canvas.pack()

        self.create_grid()
        self.draw_sudoku(sudoku_board)

        bt_button = ttk.Button(root, text="Solve BT", command=self.solve_bt)
        bt_button.pack(side="left")

        ac3_button = ttk.Button(root, text="Solve AC3", command=self.solve_ac3)
        ac3_button.pack(side="left")

        fc_button = ttk.Button(root, text="Solve FC", command=self.solve_fc)
        fc_button.pack(side="left")

        bt_counter_label = ttk.Label(root, text="BT Nodes Expanded: 0")
        bt_counter_label.pack(side="left")
        self.bt_counter_label = bt_counter_label

        ac3_counter_label = ttk.Label(root, text="AC3 Nodes Expanded: 0")
        ac3_counter_label.pack(side="left")
        self.ac3_counter_label = ac3_counter_label

        fc_counter_label = ttk.Label(root, text="FC Nodes Expanded: 0")
        fc_counter_label.pack(side="left")
        self.fc_counter_label = fc_counter_label

        reset_button = ttk.Button(root, text="Reset", command=self.reset_board)
        reset_button.pack(side="right")

    def create_grid(self):
        for i in range(10):
            self.root.canvas.create_line((i * 50, 0), (i * 50, 450), fill="#000000", width=1)
            self.root.canvas.create_line((0, i * 50), (450, i * 50), fill="#000000", width=1)

    def draw_sudoku(self, board):
        for row in range(9):
            for col in range(9):
                if board[row][col] != 0:
                    x, y = col * 50 + 25, row * 50 + 25
                    self.text_objects[row][col] = self.root.canvas.create_text(x, y, text=str(board[row][col]), font=("Arial", 24))

    def update_board_and_ui(self, board):
        for row in range(9):
            for col in range(9):
                if board[row][col] != 0:
                    x, y = col * 50 + 25, row * 50 + 25
                    self.root.canvas.delete(self.text_objects[row][col])
                    self.text_objects[row][col] = self.root.canvas.create_text(x, y, text=str(board[row][col]), font=("Arial", 24))
                self.root.update()

    def solve_bt(self):
        self.reset_board()
        self.bt_nodes_counter = 0
        self.solve_backtracking(self.sudoku_board)
        self.bt_counter_label.config(text="BT Nodes Expanded: " + str(self.bt_nodes_counter))

    def solve_ac3(self):
        self.reset_board()
        self.ac3_nodes_counter = 0
        self.ac3_thread = threading.Thread(target=self.ac3_thread_func)
        self.ac3_thread.start()

    def ac3_thread_func(self):
        csp = SudokuCSP(self.sudoku_board)
        solved_ac3 = csp.solve_maintaining_arc_consistency(self)
        if solved_ac3 is not None:
            self.ac3_nodes_counter = csp.branch_counter
            self.ac3_counter_label.config(text="AC3 Nodes Expanded: " + str(self.ac3_nodes_counter))
            self.update_board_and_ui(solved_ac3)

    def solve_fc(self):
        self.reset_board()
        self.fc_nodes_counter = 0
        self.fc_thread = threading.Thread(target=self.fc_thread_func)
        self.fc_thread.start()

    def fc_thread_func(self):
        solver = SudokuSolver(self.sudoku_board)

        result, self.fc_nodes_counter = solver.solve('forward_checking', self)

        if result:
            self.fc_counter_label.config(text="FC Nodes Expanded: " + str(self.fc_nodes_counter))
        else:
            print("No valid solution found.")

    def reset_board(self):
        self.root.canvas.delete("all")
        self.create_grid()

        # Reset the Sudoku board to the original state
        self.sudoku_board = [row[:] for row in self.initial_board]

        for row in range(9):
            for col in range(9):
                num = self.sudoku_board[row][col]
                if num != 0:
                    x, y = col * 50 + 25, row * 50 + 25
                    self.text_objects[row][col] = self.root.canvas.create_text(x, y, text=str(num), font=("Arial", 24))

    def is_valid(self, board, row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                self.bt_nodes_counter += 1
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    self.bt_nodes_counter += 1
                    return False
        return True

    def solve_backtracking(self, board):
        if not self.find_empty(board):
            return True

        row, col = self.find_empty(board)

        for num in range(1, 10):
            self.bt_nodes_counter += 1
            self.root.update()
            self.root.after(0)

            if self.is_valid(board, row, col, num):
                board[row][col] = num
                x, y = col * 50 + 25, row * 50 + 25
                self.text_objects[row][col] = self.root.canvas.create_text(x, y, text=str(num), font=("Arial", 24))
                if self.solve_backtracking(board):
                    return True
                self.root.canvas.delete(self.text_objects[row][col])
                board[row][col] = 0

        return False

    def find_empty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return i, j

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

    def _solve_maintaining_arc_consistency(self, board, visualizer):
        empty_cell = self.find_empty_cell(board)
        if not empty_cell:
            return True
        row, col = empty_cell
        for num in range(1, 10):
            if self.is_valid(board, row, col, num):
                board[row][col] = num
                self.ac3(board)
                if visualizer is not None:
                    visualizer.update_board_and_ui(board)
                if self._solve_maintaining_arc_consistency(board, visualizer):
                    self.branch_counter += 1
                    return True
                board[row][col] = 0
        return False

    def solve_maintaining_arc_consistency(self, visualizer):
        board = [row[:] for row in self.puzzle]
        if not self._solve_maintaining_arc_consistency(board, visualizer):
            return None
        return board

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

    def solve_forward_checking(self, visualizer):
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
            if visualizer is not None:
                visualizer.update_board_and_ui(self.puzzle)
            if self.solve_forward_checking(visualizer):
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

    def solve(self, algorithm='forward_checking', visualizer=None):
        self.nodes_count = 0

        if algorithm == 'forward_checking':
            if self.solve_forward_checking(visualizer):
                return self.puzzle, self.nodes_count
            else:
                return None, self.nodes_count

root = tk.Tk()
root.title("Sudoku Solver")

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

sudoku_visualizer = SudokuVisualizer(root, board)

root.mainloop()
