from flask import Flask
from flask import render_template, redirect

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World!"

@app.route("/sudoku")
def s():
    return render_template("sudoku.html")

