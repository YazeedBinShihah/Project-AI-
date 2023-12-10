def initialize_domain(board):
    domain = {}
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                domain[(i, j)] = set(range(1, 10))
    return domain

def initial_domain_pruning(board, domain):
    for row in range(9):
        for col in range(9):
            if board[row][col] != 0:
                value = board[row][col]
                for i in range(9):
                    domain.get((row, i), set()).discard(value)
                    domain.get((i, col), set()).discard(value)
                row_start, col_start = 3 * (row // 3), 3 * (col // 3)
                for i in range(row_start, row_start + 3):
                    for j in range(col_start, col_start + 3):
                        domain.get((i, j), set()).discard(value)

from copy import deepcopy

def backtrack(board, domain, counter):
    if not domain:  # All cells are filled
        return True

    # Choose a variable with the smallest domain
    row, col = min(domain, key=lambda x: len(domain[x]))

    original_domain = deepcopy(domain[row, col])
    for value in original_domain:
        counter[0] += 1
        board[row][col] = value

        new_domain = deepcopy(domain)
        del new_domain[row, col]

        # Update the domain values based on the new value
        for i in range(9):
            new_domain.get((row, i), set()).discard(value)
            new_domain.get((i, col), set()).discard(value)

        row_start, col_start = 3 * (row // 3), 3 * (col // 3)
        for i in range(row_start, row_start + 3):
            for j in range(col_start, col_start + 3):
                new_domain.get((i, j), set()).discard(value)

        # If no domain is empty, proceed with this choice
        if all(len(new_domain[key]) > 0 for key in new_domain):
            if backtrack(board, new_domain, counter):
                return True

        # Undo the choice
        board[row][col] = 0

    return False

def solve_sudoku_mac(board):
    counter = [0]
    domain = initialize_domain(board)
    initial_domain_pruning(board, domain)
    backtrack(board, domain, counter)
    return counter[0]

# Example board
board = [
       [0, 0, 0, 0, 0, 2, 0, 3, 0],
    [6, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 7, 0, 9, 0, 0],
    [0, 0, 0, 0, 0, 4, 0, 0, 7],
    [0, 0, 0, 5, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 9, 0],
    [0, 0, 0, 0, 0, 0, 4, 0, 0],
    [0, 2, 0, 0, 8, 0, 0, 0, 0],
    [5, 0, 0, 0, 0, 0, 0, 0, 0]
]

# Solving Sudoku using MAC
expanded_nodes = solve_sudoku_mac(board)
print("MAC Board after solving:")
for row in board:
    print(row)
print("Number of expanded nodes:", expanded_nodes)
