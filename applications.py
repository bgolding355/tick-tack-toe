# Flask imports
from flask import Flask, render_template, session, redirect, url_for, request
from flask_socketio import SocketIO, emit
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
# non-Flask imports
from static.python import game_resources
import os
import random
import uuid

# Basic setup
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)
socketio=SocketIO(app)

# Model for a game
class Game(db.Model):
    game_id = db.Column(db.String(8), primary_key=True)
    player1 = db.Column(db.String(20))
    player2 = db.Column(db.String(20))
    game_data = db.Column(db.String(28))

# Default route
@app.route('/')
def index():
    # Generates ID for the user. Since each game will be finished in one sitting, no username/password system is required
    if session.get('user_id') is None: 
        session['user_id'] = str(uuid.uuid4())
    return render_template('index.html')

# Route for singleplayer game
@app.route('/singleplayer')
def singleplayer():
    return render_template('single.html')

# Genaric route for multiplayer game
@app.route('/multiplayer')
def new_multiplayer_game():
    # Generates random alphanumeric string for the game
    random_string = ''.join(random.choice('0123456789ABCDEF') for i in range(8))

    # Creates entry for game in SQL database
    game_data = '----------------------------' #28 '-'s
    new_game = Game(game_id=random_string, player1=session.get('user_id'), player2 = '', game_data=game_data)
    db.session.add(new_game)
    db.session.commit()

    # Redirects them to /multiplayer/random_string
    return redirect(url_for('multiplayer', game_id=random_string), code=302)

# Route for specific multiplayer game
@app.route('/multiplayer/<string:game_id>')
def multiplayer(game_id):
    # If this is the second user to join this game, adding them to player2 and switching player_number = 2
    player_number = 1
    if Game.query.filter_by(game_id=game_id).first().player1 != session.get('user_id'):
        Game.query.filter_by(game_id=game_id).first().player2 = session.get('user_id')
        player_number = 2
        db.session.commit()
    return render_template('multiplayer.html', game_id=game_id, player_number=player_number)

# route for joining an existing game through the prompt on the index page
@app.route('/join_game', methods=['GET'])
def join_game():
    game_id = request.values['game_id']
    return redirect(url_for('multiplayer', game_id=game_id), code=302)

# Triggers when a new square is selected (singleplayer)
@socketio.on('square_selection_singleplayer')
def square_selection_singleplayer(data):
    # First adding square to the session, initializing it if it DNE
    if session.get('singleplayer') is None: 
        session['singleplayer'] = ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-',  \
            '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'] # 28 -'s coresponding with 
                                                                                            # each square, extra string
                                                                                            # Added to prevent potential 
                                                                                            # off by 1 errors

    if session['singleplayer'][int(data['square'])] == '-': # First checking if square is unfilled
        session['singleplayer'][int(data['square'])]='p'
        win = game_resources.check_win(session['singleplayer'])

        if win == '-':  # Computer makes move
            computer_move = game_resources.computer_move(session['singleplayer'])
            session['singleplayer'][computer_move[0]] = 'c'
            if computer_move[1]:  # Is true when that move results in a win
                emit('new_gamestate', session['singleplayer'])  # Update Board
                emit('winner', 'c')  # Declare computer as winner
            else:
                emit('new_gamestate', session['singleplayer'])
        else:  # There is a tie and/or win
            emit('new_gamestate', session['singleplayer'])  # Update Board
            emit('winner', win)  # Declare winner

# Triggers when a new square is selected (multiplayer). This differs from singleplayer as it
# keeps track of which player can move
@socketio.on('square_selection_multiplayer')
def square_selection_multiplayer(data):
    # First adding square to the session, initializing it if it DNE
    game_state = list(Game.query.filter_by(game_id=data['game_id']).first().game_data) #board as a char array

    if game_state[int(data['square'])] == '-': # First checking if square is unfilled
        # Adding the move
        if int(data['player_number']) == 1:
            game_state[int(data['square'])] = '1'
        else:
            game_state[int(data['square'])] = '2'
        # Committing the new board to SQL
        Game.query.filter_by(game_id=data['game_id']).first().game_data = ''.join(game_state)
        db.session.commit()
        win = game_resources.check_win(game_state)

        if win == '-': # There is no winner or a tie
            emit('update_multiplayer_board', {'turn': int(data['player_number'])%2+1, 'game_state': game_state}, broadcast=True)
        else:  # There is a tie and/or win
            emit('update_multiplayer_board', {'turn': int(data['player_number'])%2+1, 'game_state': game_state}, broadcast=True)
            emit('winner_multiplayer', {'winner': win}, broadcast=True)

# Triggers when page is refreshed (multiplayer), takes a game_id as input and returns the coresponding board
@socketio.on('board_update_request')
def board_update_request(data):
    board = list(Game.query.filter_by(game_id=data['game_id']).first().game_data)
    emit('update_multiplayer_board', {'turn': -1, 'game_state': board}, broadcast=True) # -1 coresponds to no change
