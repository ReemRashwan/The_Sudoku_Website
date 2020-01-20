import os
import json
from flask import Flask
from flask import request, render_template, redirect, session, url_for
from sudoku import SudokuGame

app = Flask(__name__)

# reloading templates without restarting the server.
app.config['TEMPLATES_AUTO_RELOAD'] = True

# clear all session variable before starting the app
app.secret_key = os.urandom(32)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sudoku_solver", methods=["GET", "POST"])
def sudoku_solver():
    if request.method == "GET":
        # if visiting for the first time or after coming from different page
        # empty sudoku grid.
        welcoming_message = "أهلا بك، رجاءً أدخل قيم السودوكو لنتمكن من حلها لك."
        return render_template("sudoku_solver.html", message=welcoming_message)

    elif request.method == "POST":
        # fetch sudoku values from the grid
        sudoku_values = []
        for key in request.form:
            # receive the inputs as ints, if can't cast (in case of None) fill with zero.
            sudoku_values.append(request.form.get(key, 0, type=int))

        # check number of cells
        assert len(sudoku_values) == 81, f"Expected 81 values, got {len(sudoku_values)} instead."

        # create a sudoku object
        sudoku = SudokuGame(sudoku_values)
        session['sudoku'] = json.dumps(sudoku.__dict__)

        # check if the grid doesn't violate the sudoku rules before solving
        is_valid_grid = sudoku.is_valid_grid()
        if not is_valid_grid:
            # prompting the user to enter a valid grid.
            message = "القيم التي أدخلتها يوجد بينها تعارض، " \
                      "رجاءً تأكد أن كل الصفوف والأعمدة والمربعات لا تحتوي على قيم مكررة."
            return render_template("sudoku_solver.html", sudoku=sudoku, message=message)

        # solve the sudoku
        is_solved = sudoku.solve()

        # save in session so other routes can see this sudoku grid.
        # save after solving
        session['sudoku'] = json.dumps(sudoku.__dict__)

        if is_solved:
            # display the results.
            return redirect(url_for("sudoku_solver_result"))
        else:
            # prompting the user that the sudoku doesn't have a solution and
            # to check the entered values.
            message = "لا يوجد حل لهذه السودوكو. هل أنت متأكد من القيم المدخلة؟"
            print("No Solution")
            return render_template("sudoku_solver.html", sudoku=sudoku, message=message)


@app.route("/sudoku_solver_result")
def sudoku_solver_result():
    # getting the sudoku object
    sudoku = session.get('sudoku', None)

    # double check that the sudoku object was passed.
    assert sudoku is not None, "Can't get the sudoku solution"

    # deserialize the object
    sudoku = json.loads(sudoku)
    session.clear()
    return render_template("sudoku_solver_result.html", sudoku=sudoku)


if __name__ == "__main__":
    # TODO: TURN OFF DEBUGGING MODE
    app.run(debug=True)
