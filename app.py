from flask import Flask
from flask import request, render_template, redirect
from sudoku import SudokuGame

app = Flask(__name__)


@app.route("/")
def index():
    return "Welcome to Our Sudoku"


@app.route("/sudoku_solver", methods=["GET", "POST"])
def sudoku_solver():
    if request.method == "GET":
        return render_template("sudoku_solver.html")
    else:
        sudoku_values = []
        for key in request.form:
            sudoku_values.append(request.form.get(key, 0, type=int))

        # check number of cells
        assert len(sudoku_values) == 81, f"Expected 81 values, got {len(sudoku_values)} instead."

        sudoku = SudokuGame(sudoku_values)
        sudoku.solve_sudoku()

        render_template("sudoku_solver", sudoku_values=sudoku_values)



