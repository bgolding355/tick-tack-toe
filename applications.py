import os
from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
from static.python import game_resources
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
socketio=SocketIO(app)

#Default route
@app.route('/')
def index():
    return render_template('index.html')

#Route for singleplayer game
@app.route('/singleplayer')
def singleplayer():
    return render_template('single.html')

#Triggers when a new square is selected
@socketio.on('square_selection')
def square_selection(data):
    #First adding square to the session, initializing it if it DNE
    if session.get('singleplayer') is None: 
        session['singleplayer'] = ['', '', '', '', '', '', '', '', '', '', '', '',  \
            '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''] #28 empty strings coresponding with each square, extra string
                                                                            #Added to prevent potential off by 1 errors
    session['singleplayer'][int(data['square'])]='p'
    win = game_resources.check_win(session['singleplayer'])
    if win != 'c' or win!='p': #Computer makes move if there is no winner
        session['singleplayer'][game_resources.computer_move(session['singleplayer'])]='c'
        emit('new_gamestate', session['singleplayer'], win)
    else:
        emit('winner',win)
