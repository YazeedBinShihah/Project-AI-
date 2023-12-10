def solve_sudoku_mac(board):
    def is_valid_assignment(board, row, col, num):

    # Check validity of assignment implementation

    def backtrack(row, col, counter):
        if row == 9:
            return True

        if col == 9:
            return backtrack(row + 1, 0, counter)

        if board[row][col] != 0:
            return backtrack(row, col + 1, counter)

        for num in range(1, 10):
            if is_valid_assignment(board, row, col, num):
                board[row][col] = num
                counter[0] += 1  # Increment counter here
                if backtrack(row, col + 1, counter):
                    return True
                board[row][col] = 0

        return False

    counter = [0]
    if backtrack(0, 0, counter):
        return counter[0]
    else:
        return -1  # No solution found


# Example Sudoku board
board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

counter = solve_sudoku_mac(board)
print("Number of expanded nodes:", counter)
print("Solved board:")
for row in board:
    print(row)