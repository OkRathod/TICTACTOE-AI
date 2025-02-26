from flask import Flask, render_template, request, jsonify
import tictactoe as ttt
import os

app = Flask(__name__)

# Initialize game state
game_state = {
    "user": None,
    "board": ttt.initial_state(),
    "ai_turn": False,
    "game_over": False,
    "winner": None
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/choose', methods=['POST'])
def choose():
    data = request.json
    game_state["user"] = data.get("player")
    game_state["board"] = ttt.initial_state()
    game_state["game_over"] = False
    game_state["winner"] = None
    
    # If player chooses O, AI (X) goes first
    if game_state["user"] == ttt.O:
        ai_action = ttt.minimax(game_state["board"])
        if ai_action:
            game_state["board"] = ttt.result(game_state["board"], ai_action)
    
    return jsonify({
        "message": "Player chosen", 
        "user": game_state["user"],
        "board": game_state["board"]
    })

@app.route('/move', methods=['POST'])
def move():
    # Check if game is already over or player hasn't chosen X/O
    if game_state["game_over"] or game_state["user"] is None:
        return jsonify({"message": "Cannot make move"}), 400
    
    data = request.json
    row, col = data.get("row"), data.get("col")
    
    # Check if the move is valid
    if game_state["board"][row][col] == ttt.EMPTY:
        game_state["board"] = ttt.result(game_state["board"], (row, col))
        
        # Check if game is over after player's move
        game_state["winner"] = ttt.winner(game_state["board"])
        game_state["game_over"] = ttt.terminal(game_state["board"])
        
        return jsonify({
            "board": game_state["board"], 
            "message": "Move made",
            "game_over": game_state["game_over"],
            "winner": game_state["winner"]
        })
    
    return jsonify({"message": "Invalid move"}), 400

@app.route('/ai_move', methods=['POST'])
def ai_move():
    # Check if game is already over or player hasn't chosen X/O
    if game_state["game_over"] or game_state["user"] is None:
        return jsonify({"message": "Cannot make AI move"}), 400
    
    if not ttt.terminal(game_state["board"]):
        ai_action = ttt.minimax(game_state["board"])
        if ai_action:
            game_state["board"] = ttt.result(game_state["board"], ai_action)
            
            # Check if game is over after AI's move
            game_state["winner"] = ttt.winner(game_state["board"])
            game_state["game_over"] = ttt.terminal(game_state["board"])
            
            return jsonify({
                "board": game_state["board"], 
                "message": "AI move made",
                "game_over": game_state["game_over"],
                "winner": game_state["winner"]
            })
    
    return jsonify({"message": "Game over or invalid request"}), 400

@app.route('/restart', methods=['POST'])
def restart():
    game_state["user"] = None
    game_state["board"] = ttt.initial_state()
    game_state["ai_turn"] = False
    game_state["game_over"] = False
    game_state["winner"] = None
    
    return jsonify({"message": "Game restarted"})

@app.route('/game_state', methods=['GET'])
def get_game_state():
    return jsonify({
        "user": game_state["user"],
        "board": game_state["board"],
        "game_over": game_state["game_over"],
        "winner": game_state["winner"]
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
