from typing import Dict

# class Sudoku:
#     def __init__(self):
#         self.grid = [[0 for _ in range(1, 9 + 1)] for _ in range(9)]
#         self.dgrid = [None] * 81
#         empty_indices = []
#
#     def get_empty_indices(self):
#         empty_indices = []
#         for i, value in enumerate(self.grid):
#             empty_indices.append(i)
#
#     def is_valid(self, value) -> bool:
#         # if value exists in row, column or subgrid then it is not allowed
#         # if value in row or value in column or value in box:
#         #     return False
#         return True
#
#     def solve_cell(self, index):
#         # assign value if possible, else backtrack
#         for value in range(1, 9 + 1):
#             if self.is_valid(value):
#                 self.grid[index] = value
#                 return
#
#         # backtrack()
#
#     def solve(self):
#         ''' implementing backtracking algorithm with constraint based approach '''
#         for i, cell_value in enumerate(self.grid):
#             if cell_value is None:
#                 continue
#             else:
#                 self.solve_cell(i)
#
#     def display(self):
#         # print 9 rows
#         for row in self.grid:
#             print(*row)
#


class SudokuGame:
    def __init__(self, grid: Dict = None) -> None:
        self.grid: Dict = grid

        # if grid is not provided
        if self.grid is None:
            self.initialize_grid()

    def initialize_grid(self):
        # declaration of the sudoku grid filled with zeros
        self.grid = {
            'A': None,
            'B': None,
            'C': None,
            'D': None,
            'E': None,
            'F': None,
            'G': None,
            'H': None,
            'I': None
        }

        # initialization of the sudoku grid, 9 * 9 zeros
        for key in self.grid.keys():
            # for each row, create a list of nine zeros.
            self.grid[key] = [0] * 9
            # self.grid[key] = [0 for _ in range(9)]


    def display(self) -> None:
        # print 9 rows
        for row in self.grid.values():
            print(*row)

    def solve(self):
        pass

    def is_valid(self, index: int) -> bool:
        # if the value doesn't exist in row, col, box then it is valid.
        pass


if __name__ == "__main__":
    sudoku = SudokuGame()
    sudoku.display()













