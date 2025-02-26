from flask import Flask, render_template, request, jsonify
import tictactoe as ttt

app = Flask(__name__)

# Initialize game state
game_state = {
    "user": None,
    "board": ttt.initial_state(),
    "ai_turn": False
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/choose', methods=['POST'])
def choose():
    data = request.json
    game_state["user"] = data.get("player")
    return jsonify({"message": "Player chosen", "user": game_state["user"]})

@app.route('/move', methods=['POST'])
def move():
    data = request.json
    row, col = data.get("row"), data.get("col")
    if game_state["board"][row][col] == ttt.EMPTY:
        game_state["board"] = ttt.result(game_state["board"], (row, col))
        return jsonify({"board": game_state["board"], "message": "Move made"})
    return jsonify({"message": "Invalid move"}), 400

@app.route('/ai_move', methods=['POST'])
def ai_move():
    if game_state["user"] and not ttt.terminal(game_state["board"]):
        move = ttt.minimax(game_state["board"])
        game_state["board"] = ttt.result(game_state["board"], move)
        return jsonify({"board": game_state["board"], "message": "AI move made"})
    return jsonify({"message": "Game over or invalid request"}), 400

@app.route('/restart', methods=['POST'])
def restart():
    game_state["user"] = None
    game_state["board"] = ttt.initial_state()
    game_state["ai_turn"] = False
    return jsonify({"message": "Game restarted"})

if __name__ == '__main__':
    app.run(debug=True)
