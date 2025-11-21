"""
sudoku_gui.py
A simple Tkinter GUI to input a Sudoku puzzle and solve it
Requires tkinter (builtin).
"""

import tkinter as tk
from tkinter import messagebox
from typing import List

# Import solver functions from sudoku_solver (assuming it's in same folder)
from sudoku_solver import parse_board_from_lines, solve, print_board

class SudokuGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku Solver - SkillCraft Task 03")
        self.cells = [[None]*9 for _ in range(9)]
        self._build_grid()
        self._build_buttons()

    def _build_grid(self):
        frame = tk.Frame(self)
        frame.pack(padx=10, pady=10)
        for r in range(9):
            for c in range(9):
                e = tk.Entry(frame, width=2, justify='center', font=('Helvetica', 16))
                e.grid(row=r, column=c, padx=(0 if c % 3 else 4, 0), pady=(0 if r % 3 else 4, 0))
                self.cells[r][c] = e

    def _build_buttons(self):
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Solve", command=self.on_solve).pack(side='left', padx=4)
        tk.Button(btn_frame, text="Clear", command=self.on_clear).pack(side='left', padx=4)
        tk.Button(btn_frame, text="Load Sample", command=self.load_sample).pack(side='left', padx=4)

    def load_sample(self):
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
        for r in range(9):
            for c in range(9):
                ch = sample[r][c]
                self.cells[r][c].delete(0, tk.END)
                if ch != '0':
                    self.cells[r][c].insert(0, ch)

    def on_clear(self):
        for r in range(9):
            for c in range(9):
                self.cells[r][c].delete(0, tk.END)

    def on_solve(self):
        lines = []
        for r in range(9):
            row_chars = []
            for c in range(9):
                v = self.cells[r][c].get().strip()
                if v == "":
                    row_chars.append("0")
                else:
                    row_chars.append(v[0])
            lines.append("".join(row_chars))
        try:
            board = parse_board_from_lines(lines)
        except Exception as e:
            messagebox.showerror("Invalid input", str(e))
            return
        solved = solve(board)
        if not solved:
            messagebox.showinfo("No solution", "No valid solution for the given puzzle.")
            return
        # fill in GUI
        for r in range(9):
            for c in range(9):
                self.cells[r][c].delete(0, tk.END)
                self.cells[r][c].insert(0, str(board[r][c]))
        messagebox.showinfo("Solved", "Puzzle solved! ✅")


if __name__ == "__main__":
    app = SudokuGUI()
    app.mainloop()
