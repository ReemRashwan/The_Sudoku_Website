from flask import Flask
from flask import request, render_template
from sudoku import SudokuGame

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route("/")
def index():
    return render_template("index.html")


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

        render_template("sudoku_solver.html", sudoku_values=sudoku_values)



