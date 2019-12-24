from typing import List, Optional


class SudokuGame:
    def __init__(self, sudoku_values: list) -> None:
        self.grid: List = sudoku_values
        self.empty_cells_indices: List = []

        # check size, 81 elements, and get empty indices
        self.check_grid_size()
        self.get_empty_cells_indices()

    def display(self) -> None:
        # print each row in a separate line
        for index in range(0, 73, 9):
            print(*self.grid[index: index + 9])

    def check_grid_size(self):
        sudoku_length = len(self.grid)
        assert sudoku_length == 81, f"sudoku list should be of length 81, got {sudoku_length} instead"

    def get_empty_cells_indices(self) -> None:
        for index, value in enumerate(self.grid):
            if value == 0:
                self.empty_cells_indices.append(index)

    def get_next_unsolved(self, current_unsolved_index: int = None) -> Optional[int]:
        # if this is the first call to the function, return first index
        if current_unsolved_index is None:
            return self.empty_cells_indices[0] if len(self.empty_cells_indices) > 0 else None

        # else, get index of next empty cell
        try:
            next_unresolved = self.empty_cells_indices[self.empty_cells_indices.index(current_unsolved_index) + 1]
        except IndexError:
            # if current is the last index - no more empty cells
            return None

        return next_unresolved

    def solve_sudoku(self) -> bool:
        self.solve(self.empty_cells_indices[0])
        # if all cells are filled, success
        if 0 not in self.grid:
            return True
        else:
            return False

    def solve(self, current_index: int) -> None:
        # Get the first unsolved cell (contains 0)
        next_index = self.get_next_unsolved(current_index)

        # if all cells are filled
        if current_index is None:
            return

        for value in range(1, 10):
            if self.is_valid(current_index, value):
                self.grid[current_index] = value
                self.solve(next_index)

        # if reached here without finding a valid number, reset cell value
        # only if we didn't found a solution
        if 0 in self.grid:
            self.grid[current_index] = 0

        return

    def is_valid(self, index: int, value: int) -> bool:
        # if the value doesn't exist in row, col, box then it is valid.

        # get row number, and offset from the start of the row
        row_start_index = (index // 9) * 9
        cell_offset = index - row_start_index

        def is_valid_row() -> bool:
            # find the first index in the row except for current cell
            row_values = self.grid[row_start_index: row_start_index + 9]

            # remove current cell from list
            # del(row_values[cell_offset])

            if value in row_values:
                return False

            # if no duplicates
            return True

        def is_valid_col() -> bool:
            # rows starting indices
            for i in range(0, 81, 9):
                # if i == row_start_index:
                    # continue
                if value == self.grid[i + cell_offset]:
                    return False
            # if no duplicates
            return True

        def is_valid_box() -> bool:
            def get_box_values() -> List:
                # get the index of the first cell in the same box in the same row
                # we can use this offset to get the first item in each row that
                # belongs to the box we are in
                horizontal_box_start_offset = cell_offset - (cell_offset % 3)

                # starting indices
                top_boxes_rows = [0, 9, 18]
                middle_boxes_rows = [27, 36, 45]
                bottom_boxes_rows = [54, 63, 72]

                box_indices = []
                box_values = []

                # adjust the starting index in the three rows of the box
                if row_start_index in top_boxes_rows:
                    box_rows_start_indices = [item + horizontal_box_start_offset for item in top_boxes_rows]
                elif row_start_index in middle_boxes_rows:
                    box_rows_start_indices = [item + horizontal_box_start_offset for item in middle_boxes_rows]
                else:
                    box_rows_start_indices = [item + horizontal_box_start_offset for item in bottom_boxes_rows]

                # get the next two indices after the starting index in each row
                for item in box_rows_start_indices:
                    box_indices.extend([item, item + 1, item + 2])

                # delete current cell index from list
                # del(box_indices[box_indices.index(index)])

                # get box values
                for i in box_indices:
                    box_values.append(self.grid[i])

                return box_values

            sub_grid_values = get_box_values()
            # if duplicate value
            if value in sub_grid_values:
                return False
            # if unique in box
            return True

        if is_valid_row() and is_valid_col() and is_valid_box():
            return True

        # if any condition is violated
        return False

    def check_solution(self, sudoku_solution):
        sudoku_solution_length = len(sudoku_solution)
        if sudoku_solution_length != 81:
            print(f"sudoku solution list should be of length 81, got {sudoku_solution_length} instead")
        return self.grid == sudoku_solution


def read_sudokus_from_file(file_path: str) -> List[List[int]]:
    # list of sudokus
    sudokus = []

    # open the file
    try:
        file = open(file_path, 'r')
    except FileNotFoundError as e:
        raise e

    # read the file line by line.
    with file:
        for line in file:
            sudokus.append([int(number) for number in line.strip()])  # each sudoku is a list of numbers

    # list of sudokus lists
    return sudokus


if __name__ == "__main__":
    sudokus = read_sudokus_from_file("sudoku.txt")
    sudoku = SudokuGame(sudokus[0])
    sudoku.solve_sudoku()
    if sudoku.check_solution(read_sudokus_from_file("sudoku_solution.txt")[0]):
        print("Yaaaaaaaaaay")
    else:
        print("No Match")
