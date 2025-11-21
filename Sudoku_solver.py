"""
sudoku_solver.py
A simple backtracking Sudoku solver (9x9).
Input format (text file or built-in sample):
- 9 lines, each line 9 characters separated by spaces or concatenated.
- Use 0 or . for empty cells.

Example line: 5 3 0 0 7 0 0 0 0
or           530070000
"""

from typing import List, Optional, Tuple

Board = List[List[int]]


def parse_board_from_lines(lines: List[str]) -> Board:
    board: Board = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Accept space-separated or contiguous digits
        if " " in line:
            tokens = line.split()
        else:
            tokens = list(line)
        row = []
        for t in tokens:
            if t == ".":
                row.append(0)
            else:
                try:
                    row.append(int(t))
                except ValueError:
                    raise ValueError(f"Invalid token in board: {t}")
        if len(row) != 9:
            raise ValueError("Each row must have 9 entries.")
        board.append(row)
    if len(board) != 9:
        raise ValueError("Board must have 9 rows.")
    return board


def print_board(board: Board) -> None:
    for r in range(9):
        if r % 3 == 0 and r != 0:
            print("-" * 21)
        row = []
        for c in range(9):
            val = board[r][c]
            s = str(val) if val != 0 else "."
            row.append(s)
            if (c + 1) % 3 == 0 and c != 8:
                row.append("|")
        print(" ".join(row))
    print()


def find_empty(board: Board) -> Optional[Tuple[int, int]]:
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return (r, c)
    return None


def is_valid(board: Board, row: int, col: int, num: int) -> bool:
    # Check row
    if any(board[row][c] == num for c in range(9)):
        return False
    # Check column
    if any(board[r][col] == num for r in range(9)):
        return False
    # Check 3x3 box
    box_r = (row // 3) * 3
    box_c = (col // 3) * 3
    for r in range(box_r, box_r + 3):
        for c in range(box_c, box_c + 3):
            if board[r][c] == num:
                return False
    return True


def solve(board: Board) -> bool:
    empty = find_empty(board)
    if not empty:
        return True  # solved
    row, col = empty
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve(board):
                return True
            board[row][col] = 0  # backtrack
    return False


def read_board_from_file(path: str) -> Board:
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return parse_board_from_lines(lines)


def write_board_to_file(board: Board, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for r in board:
            f.write("".join(str(x) for x in r) + "\n")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Sudoku solver (9x9) using backtracking.")
    parser.add_argument("-i", "--input", help="Path to input puzzle text file (9 lines). If omitted uses sample puzzle.", default=None)
    parser.add_argument("-o", "--output", help="Path to write solved puzzle (optional).", default=None)
    args = parser.parse_args()

    if args.input:
        board = read_board_from_file(args.input)
    else:
        # sample puzzle (0 = empty)
        sample = [
            "530070000",
            "600195000",
            "098000060",
            "800060003",
            "400803001",
            "700020006",
            "060000280",
            "000419005",
            "000080079",
        ]
        board = parse_board_from_lines(sample)
        print("Using built-in sample puzzle:")

    print("Initial board:")
    print_board(board)

    solved = solve(board)
    if solved:
        print("Solved board:")
        print_board(board)
        if args.output:
            write_board_to_file(board, args.output)
            print(f"Solution written to {args.output}")
    else:
        print("No solution found for the provided puzzle.")


if __name__ == "__main__":
    main()
