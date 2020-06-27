# Flask imports
from flask import Flask, render_template, session, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
# non-Flask imports
from static.python import game_resources
import os
import random

#Basic setup
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)
socketio=SocketIO(app)

#Model for a game
class Game(db.Model):
    game_id = db.Column(db.String(8), primary_key=True)
    player1 = db.Column(db.String(20))
    player2 = db.Column(db.String(20))
    game_data = db.Column(db.String(28))

@app.route('/debug')
def debug():
    return None


#Default route
@app.route('/')
def index():
    return render_template('index.html')

#Route for singleplayer game
@app.route('/singleplayer')
def singleplayer():
    return render_template('single.html')

#Route for multiplayer game
@app.route('/multiplayer')
def new_multiplayer_game():
    #Generates random alphanumeric string for the game
    random_string = ''.join(random.choice('0123456789ABCDEF') for i in range(8))

    #Creates entry for game in SQL database

    #Redirects them to /multiplayer/random_string
    return redirect(url_for('multiplayer', game_id=random_string), code=302)

#route for specific game
@app.route('/multiplayer/<string:game_id>')
def multiplayer(game_id):
    return render_template('multiplayer.html', game_id=game_id)


#Triggers when a new square is selected (singleplayer)
@socketio.on('square_selection')
def square_selection(data):
    #First adding square to the session, initializing it if it DNE
    if session.get('singleplayer') is None: 
        session['singleplayer'] = ['', '', '', '', '', '', '', '', '', '', '', '',  \
            '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''] #28 empty strings coresponding with each square, extra string
                                                                            #Added to prevent potential off by 1 errors

    if session['singleplayer'][int(data['square'])] == '': #First checking if square is unfilled
        session['singleplayer'][int(data['square'])]='p'
        win = game_resources.check_win(session['singleplayer'])

        if win == '-': #Computer makes move
            computer_move = game_resources.computer_move(session['singleplayer'])
            session['singleplayer'][computer_move[0]]='c'
            if computer_move[1]: #Is true when that move results in a win
                emit('new_gamestate', session['singleplayer']) #Update Board
                emit('winner','c') #Declare computer as winner
            else:
                emit('new_gamestate', session['singleplayer'])
        else: #There is a tie and/or win
            emit('new_gamestate', session['singleplayer']) #Update Board
            emit('winner',win) #Declare Winner