from typing import Dict, List, Tuple, Optional


class SudokuGame:
    def __init__(self, sudoku_values: List = None, file_path: str = None) -> None:
        """ Initialize a sudoku grid with valid values """
        self.grid: Dict = {}
        self.is_filled_map: Dict = {}  # sudoku grid map with 1 as filled, 0 as empty cell for visualization.
        self.empty_cells_indices: List[str] = []

        # initialize grid and check if it has 81 values.
        self.initialize_grid(sudoku_values, file_path)
        self.check_grid_size()

        # store empty cells in separate groups.
        self.find_empty_cells()
        self.set_is_filled_map()

    def initialize_grid(self, sudoku_values: List = None, file_path: str = None) -> None:
        """ Initialize sudoku grid from a list or a file or fill with zeros """
        grid: Dict = {}
        # initialize from list or a file.
        if sudoku_values is not None:
            # initialize from list
            if isinstance(sudoku_values, list) and len(sudoku_values) == 81:
                # check every value to be in range(1-9)
                if self.is_values_in_valid_range(sudoku_values):
                    grid = self.to_dict_sudoku(sudoku_values)
        elif file_path is not None:
            grid = self.to_dict_sudoku(self.read_from_file(file_path))

        # if grid is empty, fill with zeros
        if not grid:
            grid = self.to_dict_sudoku([0 for _ in range(81)])

        self.grid = grid

    @staticmethod
    def read_from_file(file_path: str) -> List:
        """ Read values from file. """
        # read the file line by line.
        with open(file_path, 'r') as file:
            line = file.readline().strip()

        # store values in as numbers in a list
        sudoku_values = [int(number) for number in line.strip()]

        # check if each value in range (1-9)
        if SudokuGame.is_values_in_valid_range(sudoku_values):
            return sudoku_values  # each sudoku is a list of numbers

    @staticmethod
    def to_dict_sudoku(sudoku_values: List):
        """ Convert list of sudoku values to dict """
        sudoku_dict = {}
        for i, key in enumerate("ABCDEFGHI"):
            # append nine values for each key
            sudoku_dict[key] = [int(number) for number in sudoku_values[i * 9: i * 9 + 9]]
        return sudoku_dict

    @staticmethod
    def is_values_in_valid_range(sudoku_values: List) -> bool:
        """ Check that each value is in range from 0-9 (zero for empty cells)."""
        for number in sudoku_values:
            if not (0 <= number <= 9):
                raise ValueError(f"{number} is not in valid range (1-9).")
        return True

    def display(self, sudoku_grid: Dict = None) -> None:
        """ Display the sudoku as a grid, each row in a separate line """
        # if grid is not passed, print self.grid
        if sudoku_grid is None:
            for key in self.grid:
                print(*self.grid[key])
        else:
            for key in sudoku_grid:
                print(*sudoku_grid[key])

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

    def find_empty_cells(self) -> None:
        """ Save empty cells keys and indices """
        for key, row in self.grid.items():
            for index in range(len(row)):
                if row[index] == 0:
                    self.empty_cells_indices.append(f"{key}{index}")

    def set_is_filled_map(self) -> None:
        """ map sudoku values to 0 if empty, 1 if filled. Useful for visualization """
        # create a copy of the grid
        self.is_filled_map = self.grid.copy()
        for key, row in self.is_filled_map.items():
            self.is_filled_map[key] = list(map(lambda number: 0 if number == 0 else 1, row))

    def solve(self) -> bool:
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

    def check_solution(self, actual_solution: Dict) -> bool:
        """ check if actual solution matches ours """
        return self.grid == actual_solution


if __name__ == "__main__":
    sudoku = SudokuGame(file_path="sudoku.txt")
    sudoku_solution = SudokuGame(file_path="sudoku_solution.txt")

    print("====================")
    sudoku.display()
    print("====================")
    # sudoku.display(sudoku.is_filled_map)
    # print("====================")

    # solve the given sudoku
    sudoku.solve()

    if sudoku.is_solved():
        # display our solution
        print("Solved, Our Solution")
        sudoku.display()
        print("====================")
    else:
        print("Couldn't solve the sudoku")

    # display actual solution
    print("Actual Solution")
    sudoku_solution.display()
    print("====================")

    if sudoku.check_solution(sudoku_solution.grid):
        print("Our solution matches the actual one.")
    else:
        print("Wrong solution")
