from boggle import Boggle
from flask import Flask, render_template, request, session, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'

boggle_game = Boggle()

@app.route('/')
def display_board():
    """SHOW BOARD"""
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    return render_template('base.html', board=board, highscore=highscore, nplays=nplays)

@app.route('/check-word')
def check_word():
    """CHECK FOR WORD IN DICTIONARY"""
    word = request.args['word']
    board = session['board']
    res = boggle_game.check_valid_word(board, word)

    return jsonify({'result': res})

@app.route('/post-score', methods=["POST"])
def post_score():
    """SCORE++, PLAYS++, HIGHSCORE++ (if necessary)"""
    score = request.json['score']
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    session["nplays"] = nplays + 1
    session["highscore"] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)