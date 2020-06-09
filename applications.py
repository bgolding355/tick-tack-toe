import os
from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO

app = Flask(__name__)
bootstrap = Bootstrap(app)
socketio=SocketIO(app)

#Default route
@app.route('/')
def index():
    return render_template('index.html')

#Route for singleplayer game
@app.route('/singleplayer')
def singleplayer():
    return render_template('single.html')