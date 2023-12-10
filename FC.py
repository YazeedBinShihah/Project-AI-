
expanded_nodes = 0  # Initialize the counter for expanded nodes

def solve_sudoku(board):
    global expanded_nodes
    expanded_nodes = 0  # Reset counter when a new puzzle is solved
    domains = init_domains(board)
    return backtrack(board, domains)

def init_domains(board):
    domains = {}
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                domains[(i, j)] = set(range(1, 10))
    return domains

def backtrack(board, domains):
    global expanded_nodes

    if is_complete(board):
        return True

    row, col = select_unassigned_var(board, domains)
    original_domain = domains[(row, col)].copy()

    for value in list(original_domain):
        if is_consistent(board, row, col, value):
            board[row][col] = value
            updated_cells = update_domain(board, row, col, value, domains)
            
            expanded_nodes += 1  # Increment the counter here
           
            if backtrack(board, domains):
                return True

            board[row][col] = 0
            restore_domain(domains, updated_cells, original_domain)
    
    return False

   
def is_complete(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return False
    return True

def select_unassigned_var(board, domains):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j

def is_consistent(board, row, col, value):
    for i in range(9):
        if board[row][i] == value or board[i][col] == value:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == value:
                return False

    return True

def update_domain(board, row, col, value, domains):
    updated_cells = []

    for i in range(9):
        if board[row][i] == 0 and value in domains[(row, i)]:
            domains[(row, i)].remove(value)
            updated_cells.append((row, i))

        if board[i][col] == 0 and value in domains[(i, col)]:
            domains[(i, col)].remove(value)
            updated_cells.append((i, col))

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == 0 and value in domains[(i, j)]:
                domains[(i, j)].remove(value)
                updated_cells.append((i, j))

    return updated_cells

def restore_domain(domains, updated_cells, original_domain):
    for row, col in updated_cells:
        domains[(row, col)] = domains[(row, col)].union(original_domain)

# Example usage:
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









if solve_sudoku(board):
    for row in board:
        print(row)
    print(f"FC Board\nNumber of expanded nodes: {expanded_nodes}")  # Print the counter here
else:
    print("No solution exists.")
