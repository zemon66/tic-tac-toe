from flask import Flask, render_template, request, jsonify
import random

# Create the Flask app instance
app = Flask(__name__)

# Constants for players
HUMAN = -1
COMP = +1

# Global board initialization
board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

def reset_board():
    """Resets the board to start a new game."""
    global board
    board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

def make_move(x, y, symbol):
    """Make a move on the board."""
    if board[x][y] == 0:  # Check if the cell is empty
        board[x][y] = symbol
        return True
    return False

def game_over(board):
    """Check if the game is over due to a win or a draw."""
    for row in board:
        if all(cell == HUMAN for cell in row) or all(cell == COMP for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == HUMAN for row in range(3)) or all(board[row][col] == COMP for row in range(3)):
            return True
    if (board[0][0] == board[1][1] == board[2][2] != 0) or (board[0][2] == board[1][1] == board[2][0] != 0):
        return True
    return not any(0 in row for row in board)  # Check for draw

def available_moves(board):
    """Return a list of available moves."""
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == 0]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def play_move():
    global board
    try:
        data = request.json
        x, y = data['x'], data['y']
        hChoice = data['hChoice']
        
        hSymbol = HUMAN if hChoice == 'X' else COMP
        cSymbol = COMP if hChoice == 'X' else HUMAN

        if make_move(x, y, hSymbol):
            if game_over(board):
                result = {"status": "win", "message": "You win!"}
                reset_board()
                return jsonify(result)
            else:
                if len(available_moves(board)) > 0:
                    move = random.choice(available_moves(board))
                    make_move(move[0], move[1], cSymbol)
                    if game_over(board):
                        result = {"status": "loss", "message": "You lose!"}
                        reset_board()
                        return jsonify(result)
                    return jsonify({"status": "continue", "board": board})
                else:
                    return jsonify({"status": "draw", "message": "It's a draw!"})

        return jsonify({"status": "invalid", "message": "Invalid move."})
    except Exception as e:
        print(f"Error: {e}")  # Log the error
        return jsonify({"status": "error", "message": "An error occurred."}), 500

@app.route('/computer-move', methods=['POST'])
def computer_move():
    global board
    data = request.json
    cChoice = data['cChoice']
    cSymbol = COMP if cChoice == 'O' else HUMAN
    
    if len(available_moves(board)) > 0:
        move = random.choice(available_moves(board))
        make_move(move[0], move[1], cSymbol)
        return jsonify({"status": "continue", "board": board})
    return jsonify({"status": "draw", "message": "It's a draw!"})

if __name__ == '__main__':
    app.run(debug=True)
