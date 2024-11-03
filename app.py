from flask import Flask, render_template, request, jsonify
import random
import platform
from os import system

app = Flask(__name__)


HUMAN = -1
COMP = +1

board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
NODES = 0

def evaluate(state):
    """Evaluates the board state and returns the score."""
    if check_win(state, COMP):
        return +1
    elif check_win(state, HUMAN):
        return -1
    return 0

def check_win(state, player):
    """Checks if the specified player has won."""
    win_patterns = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    return [player, player, player] in win_patterns

def game_over(state):
    """Checks if the game is over."""
    return check_win(state, HUMAN) or check_win(state, COMP)

def available_moves(state):
    """Returns a list of available moves."""
    moves = []
    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                moves.append([x, y])
    return moves

def make_move(x, y, player):
    """Makes a move on the board if valid."""
    if [x, y] in available_moves(board):
        board[x][y] = player
        return True
    return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def play_move():
    data = request.json
    x, y = data['x'], data['y']
    if make_move(x, y, HUMAN):
        if game_over(board):
            return jsonify({"status": "win", "message": "You win!"})
        else:
            move = random.choice(available_moves(board))
            make_move(move[0], move[1], COMP)
            if game_over(board):
                return jsonify({"status": "loss", "message": "You lose!"})
            return jsonify({"status": "continue", "board": board})
    return jsonify({"status": "invalid", "message": "Invalid move."})

if __name__ == '__main__':
    app.run(debug=True)
