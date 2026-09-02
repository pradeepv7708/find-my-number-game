from flask import Flask, render_template, request

app = Flask(__name__)

# ==========================================
# GAME VARIABLES
# ==========================================

secret_number = 0
attempts = 0
game_over = False
winner = ""


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# PLAYER 1 SETS SECRET NUMBER
# ==========================================

@app.route("/start_game", methods=["POST"])
def start_game():

    global secret_number
    global attempts
    global game_over
    global winner

    try:
        data = request.json
        number = int(data["number"])

        if number < 1 or number > 100:
            return {
                "success": False,
                "message": "Please choose a number between 1 and 100."
            }

        secret_number = number
        attempts = 0
        game_over = False
        winner = ""

        return {
            "success": True,
            "message": "Player 1 has selected the number!"
        }

    except (TypeError, ValueError, KeyError):

        return {
            "success": False,
            "message": "Invalid number."
        }


# ==========================================
# PLAYER 2 MAKES GUESS
# ==========================================

@app.route("/guess", methods=["POST"])
def guess():

    global attempts
    global game_over
    global winner

    if game_over:
        return {
            "correct": False,
            "game_over": True,
            "message": "Game Over! Please start a new game.",
            "winner": winner,
            "attempts": attempts
        }

    try:
        data = request.json
        number = int(data["guess"])

    except (TypeError, ValueError, KeyError):

        return {
            "correct": False,
            "game_over": False,
            "message": "Please enter a valid number.",
            "attempts": attempts
        }

    if number < 1 or number > 100:

        return {
            "correct": False,
            "game_over": False,
            "message": "Please enter a number between 1 and 100.",
            "attempts": attempts
        }

    attempts += 1

    # Player 2 wins
    if number == secret_number:

        game_over = True
        winner = "Player 2"

        return {
            "correct": True,
            "game_over": True,
            "winner": "Player 2",
            "message": "🎉 Correct! Player 2 wins!",
            "attempts": attempts
        }

    # Player 1 wins
    if attempts >= 10:

        game_over = True
        winner = "Player 1"

        return {
            "correct": False,
            "game_over": True,
            "winner": "Player 1",
            "message": "😢 Player 2 used all 10 attempts! Player 1 wins!",
            "attempts": attempts,
            "secret_number": secret_number
        }

    # Guess is too low
    if number < secret_number:

        return {
            "correct": False,
            "game_over": False,
            "message": "📈 Too Low! Try again.",
            "attempts": attempts
        }

    # Guess is too high
    else:

        return {
            "correct": False,
            "game_over": False,
            "message": "📉 Too High! Try again.",
            "attempts": attempts
        }


# ==========================================
# NEW GAME
# ==========================================

@app.route("/new_game", methods=["POST"])
def new_game():

    global secret_number
    global attempts
    global game_over
    global winner

    secret_number = 0
    attempts = 0
    game_over = False
    winner = ""

    return {
        "success": True,
        "message": "New game started!"
    }


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )