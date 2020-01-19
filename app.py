from flask import Flask
from flask import request, render_template, redirect, session
from sudoku import SudokuGame

app = Flask(__name__)

# reloading templates without restarting the server.
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = "TFIOSEKAE"


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

        # solve the sudoku
        sudoku = SudokuGame(sudoku_values)
        sudoku.solve()

        # save in session so other routes can see this sudoku grid.
        session['sudoku_dict'] = sudoku.grid

        if sudoku.is_solved():
            return redirect("sudoku_solver_result")
        else:
            # TODO create a route for sudokus that can't be solved.
            pass


@app.route("/sudoku_solver_result")
def sudoku_solver_result():
    sudoku_dict = session['sudoku_dict']
    return render_template("sudoku_solver_result.html", sudoku_values=sudoku_dict)


if __name__ == "__main__":
    # TODO: TURN OFF DEBUGGING MODE
    app.run(debug=True)
