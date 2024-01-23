from flask import Flask, render_template
from models import Board

app = Flask(__name__)

board = None

@app.route('/', methods=['GET'])
def index():
    return render_template('game.html')

@app.route('/board/<int:difficulty>', methods=['GET'])
def board(difficulty):
    global board
    board = Board(difficulty)
    board.generate_grid()
    board.place_bombs()
    return board.to_json()

@app.route('/move/<int:row>/<int:col>', methods=['GET'])
def move(row, col):
    global board
    board.click(col, row)
    return board.to_json()

@app.route('/flag/<int:row>/<int:col>', methods=['GET'])
def flag(row, col):
    global board
    board.flag(col, row)
    return board.to_json()