from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

categories = {
    "Animals": ["kangaroo", "elephant", "giraffe", "tiger", "panda"],
    "Countries": ["australia", "canada", "brazil", "india", "france"],
    "Fruits": ["apple", "banana", "mango", "grape", "orange"]
}

def display_hangman(tries):
    stages = [
        # (Include ASCII art as in your original code)
    ]
    return stages[tries]

def select_word(category):
    return random.choice(categories[category])

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        category = request.form["category"]
        session["category"] = category
        session["word"] = select_word(category)
        session["tries"] = 6
        session["guessed_letters"] = []
        return redirect(url_for("play"))

    return render_template("index.html", categories=categories.keys())

@app.route("/play", methods=["GET", "POST"])
def play():
    word = session.get("word")
    guessed_letters = session.get("guessed_letters", [])
    tries = session.get("tries")

    if request.method == "POST":
        guess = request.form["guess"].lower()
        if guess not in guessed_letters:
            guessed_letters.append(guess)
            if guess not in word:
                session["tries"] = tries - 1
        session["guessed_letters"] = guessed_letters

    word_display = " ".join([letter if letter in guessed_letters else "_" for letter in word])
    return render_template("play.html", word_display=word_display, guessed_letters=guessed_letters,
                           hangman=display_hangman(session["tries"]), tries=session["tries"])

if __name__ == "__main__":
    app.run(debug=True)
