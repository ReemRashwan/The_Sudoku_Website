from flask import Flask
from flask import request, render_template, redirect, session
from sudoku import SudokuGame

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = "OlayOlayHoHo"


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
        sudoku_dict = to_dict(sudoku_values)
        session['sudoku_dict'] = sudoku_dict
        return redirect("sudoku_solver_result")


@app.route("/sudoku_solver_result")
def sudoku_solver_result():
    sudoku_dict = session['sudoku_dict']
    return render_template("sudoku_solver_result.html", sudoku_values=sudoku_dict)


def to_dict(sudoku_values):
    sudoku_dict = {
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

    for i, key in enumerate(sudoku_dict):
        sudoku_dict[key] = sudoku_values[i*9: i*9+9]

    return sudoku_dict


if __name__ == "__main__":
    app.run(debug=True)
