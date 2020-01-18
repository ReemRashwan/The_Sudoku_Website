from typing import Dict, List, Tuple, Optional


class SudokuGame:
    def __init__(self, sudoku_values: Dict) -> None:
        """ Initialize a sudoku grid """
        self.grid: Dict = sudoku_values
        self.empty_cells_indices: List[str] = []
        self.filled_cells_indices: List[str] = []

        # check size, 81 elements, and get empty indices
        self.check_grid_size()
        self.classify_cells_as_filled_or_empty()

    def display(self) -> None:
        """ Display the sudoku as a grid"""
        # print each row in a separate line
        for key in self.grid:
            print(*self.grid[key])

    def check_grid_size(self):
        """ Check the number of sudoku values, if not 81, terminate """
        sudoku_values = self.get_flattened_sudoku_values()
        sudoku_length = len(sudoku_values)
        if sudoku_length != 81:
            raise AssertionError(f"sudoku list should be of length 81, got {sudoku_length} instead")

    def get_flattened_sudoku_values(self) -> List[int]:
        """ Get sudoku values in a list """
        sudoku_values = [number for row in self.grid.values() for number in row]
        return sudoku_values

    def classify_cells_as_filled_or_empty(self) -> None:
        """ Save filled cells and empty cells keys and indices """
        for key, row in self.grid.items():
            for index in range(len(row)):
                if row[index] == 0:
                    self.empty_cells_indices.append(f"{key}{index}")
                else:
                    self.filled_cells_indices.append(f"{key}{index}")

    def solve_and_check_solution(self) -> bool:
        """ Solve sudoku and return true if a solution is found. """
        first_unsolved_key, first_unsolved_index = self.get_first_unsolved() or (None, None)
        self.solve_cell(first_unsolved_key, first_unsolved_index)
        return self.is_solved()

    def get_first_unsolved(self) -> Optional[Tuple[str, int]]:
        """ Get first empty cell key and index """
        # if nothing is empty
        if len(self.empty_cells_indices) == 0:
            return None
        # return key, index of first item, Example: "A3" -> 'A', 3
        return self.empty_cells_indices[0][0], int(self.empty_cells_indices[0][1])

    def get_next_unsolved(self, current_key: str, current_index: int) -> Optional[Tuple[str, int]]:
        """ Get next cell key and index, if nothing left return None """
        # if the grid is full from the first time
        try:
            current_cell_order = self.empty_cells_indices.index(f"{current_key}{current_index}")
        except ValueError:
            return None

        # get next cell key and index, if nothing is left to be solved return None.
        try:
            next_unsolved = self.empty_cells_indices[current_cell_order + 1]
            # return key, index
            return next_unsolved[0], int(next_unsolved[1])
        except IndexError:
            # if no more empty cells, return None
            return None

    def solve_cell(self, current_key: str, current_index: int) -> None:
        """ Assign the current empty cell a valid value if possible """
        # if the grid is completely solved
        if current_key is None and current_index is None:
            return

        # find next cell key and index
        next_key, next_index = self.get_next_unsolved(current_key, current_index) or (None, None)

        # assign a valid value.
        for value in range(1, 10):
            if self.is_valid(current_key, current_index, value):
                self.grid[current_key][current_index] = value
                # solve the next cell
                self.solve_cell(next_key, next_index)

        # reset cell value if we didn't found a solution
        if not self.is_solved():
            self.grid[current_key][current_index] = 0

    def is_valid(self, key: str, index: int, value: int) -> bool:
        """ Value is valid if the value doesn't exist in row, col, box (subgrid)."""
        def is_valid_row() -> bool:
            """ Check if value already exists in the row """
            if value in self.grid[key]:
                return False
            return True

        def is_valid_col() -> bool:
            """ Check if value already exists in the column """
            # if value in column (different keys, same index)
            for row in self.grid.values():
                if value == row[index]:
                    return False
            return True

        def is_valid_box() -> bool:
            """ Check if value already exists in the box (subgrid) """
            # get the index of the first cell in the same box in the same row
            horizontal_box_start_index = index - (index % 3)

            # starting indices
            box_rows: List

            # groups of boxes vertically (top, middle, bottom)
            top_boxes_keys = ['A', 'B', 'C']
            middle_boxes_keys = ['D', 'E', 'F']
            bottom_boxes_keys = ['G', 'H', 'I']

            # assign box rows to the rows that the cell belongs to
            if key in top_boxes_keys:
                box_rows = top_boxes_keys
            elif key in middle_boxes_keys:
                box_rows = middle_boxes_keys
            else:
                box_rows = bottom_boxes_keys

            # iterate through each row values in the box.
            for row_key in box_rows:
                # values from first value in the row in the box to the third value
                box_row_values = self.grid[row_key][horizontal_box_start_index:horizontal_box_start_index + 3]
                if value in box_row_values:
                    return False

            # if the value doesn't exist in the box.
            return True

        # if value doesn't violate sudoku rules
        if is_valid_row() and is_valid_col() and is_valid_box():
            return True

        return False

    def is_solved(self) -> bool:
        """ check if the sudoku is solved (doesn't contain zeros) """
        sudoku_values = self.get_flattened_sudoku_values()
        # if there are still zeros in the grid
        if 0 in sudoku_values:
            return False
        return True

    def check_solution(self, actual_solution):
        """ check if actual solution matches ours """
        return self.grid == actual_solution


def read_sudokus_from_file(file_path: str) -> List[Dict]:
    # list of sudokus
    sudokus = []
    # read the file line by line.
    with open(file_path, 'r') as file:
        for line in file:
            sudokus.append(to_dict_sudoku(line.strip()))  # each sudoku is a list of numbers

    # list of sudokus lists
    return sudokus


def to_dict_sudoku(sudoku_values):
    sudoku = {}
    for i, key in enumerate("ABCDEFGHI"):
        # append nine values for each key
        sudoku[key] = [int(number) for number in sudoku_values[i*9: i*9 + 9]]
    return sudoku


if __name__ == "__main__":
    sudokus = read_sudokus_from_file("sudoku.txt")
    sudokus_solutions = read_sudokus_from_file("sudoku_solution.txt")

    sudoku = SudokuGame(sudokus[0])
    sudoku_solution = SudokuGame(sudokus_solutions[0])

    sudoku.display()
    print("====================")
    if sudoku.solve_and_check_solution():
        print("Solved")
    else:
        print("Couldn't solve the sudoku")
    sudoku.display()

    if sudoku.check_solution(sudoku_solution):
        print("Your solution matches ours")
    else:
        print("Wrong solution")
