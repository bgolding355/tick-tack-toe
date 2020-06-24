import os
from flask import Flask, render_template, session
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO

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
    
    #Now getting the computer response
    check_win(session['singleplayer'])

    print(session.get('singleplayer'))

#Takes session.get('singleplayer') as input, then outputs a gamestate with the appropriate computer response
def computer_response(board):
    return None

#Returns 'p' if the human player wins, 'c' if the computer wins, 't' if there is a tie, and '-' if there is no winner
def check_win(board):
    tie = False #tie is true when all board positions are filled and there is no winner
    for i in range (1,28):
        #First checking if there exists an empty space
        if game_state[i] == '':
            tie = True

        ## Now Checking potential win conditions ##
        #1) Checking for 3 in a ROW across across a flat plain
        if i%3==1: #This condition applies to 1,4,7,10,13,16,19,22,25
            #Single board conditions
            if board[i]==board[i+1] and board[i]==board[i+2]:
                if board[i]=='p':
                    #X player is winner by row across in single game
                    return 'p'
                else if (board[i]=='O')  
                    #O Player is winner by row across in single game
                    std::cout<<"The O player has won! Congradulations! Condition 2\n";
                    exit(0);
                  
              
            #Multi-Board Conditions - Diagonal across flat plain (relative to z) starting on Board1
            if (i == 1 || i == 4 || i == 7)  
                if (board[i] == board[i+10] && board[i] == board[i+20])  
                    if (board[i]=='X')  
                        #X player is winner by row across in multi-game, diagonal across flat plain
                        std::cout<<"The X player has won! Congradulations! Condition 3\n";
                        exit(0);
                       else if (board[i]=='O')  
                        #O Player is winner by row across in multi-game, diagonal across flat plain
                        std::cout<<"The O player has won! Congradulations! Condition 4\n";
                        exit(0);
                      
                  
              
            #Multi-Board Conditions - Diagonal across flat plain (relative to z) starting on Board3
            if (i==21 || i== 24 || i== 27)  
                if (board[i]==board[i-10] && board[i] == board[i-20])  
                    if (board[i]=='X')  
                        #X player is winner by row across in multi-game, diagonal across flat plain
                        std::cout<<"The X player has won! Congradulations! Condition 5\n";
                        exit(0);
                       else if (board[i]=='O')  
                        #O player is winner by row across in multi-game, diagonal across flat plain
                        std::cout<<"The O player has won! Congradulations! Condition 6\n";
                        exit(0);
                      
            #Multi-Board Conditions - Strait across x,z
            if (i<10)  
                if (board[i]==board[i+9] && board[i]==board[i+18])  
                    if (board[i]=='X')  
                        #X player is winner by row across in multi-game
                        std::cout<<"The X player has won! Congradulations! Condition 7\n";
                        exit(0);
                       else if (board[i]=='O')  
                        #O Player is winner by row across in multi-game
                        std::cout<<"The O player has won! Congradulations! Condition 8\n";
                        exit(0);
                      
                  
        //2) Checking for 3 in a row across across a vertical plain
        if (i==1||i==2||i==3||i==10||i==11||i==12||i==19||i==20||i==21) {
            //Checking for single game solutions
            if (board[i]==board[i+3] && board[i]==board[i+6]) {
                if (board[i]=='X') {
                    //X player is winner by column in single game
                    std::cout<<"The X player has won! Congradulations! This is win Condition 9\n";
                    exit(0);
                } else if (board[i]=='O') {
                    //O Player is winner by column in single game
                    std::cout<<"The O player has won! Congradulations! This is win Condition 10\n";
                    exit(0);
                }
            }
            //Checking for diagonal across a vertical plain starting at x>4
            if (i<4) {
                if (board[i]==board[i+12] && board[i]==board[i+24]) {
                    if (board[i]=='X') {
                        //X player is winner by column in multi-game
                        std::cout<<"The X player has won! Congradulations! This is win Condition 11\n";
                        exit(0);
                    } else if (board[i]=='O') {
                        //O Player is winner by column in multi-game
                        std::cout<<"The O player has won! Congradulations! This is win Condition 12\n";
                        exit(0);
                    }
                }
            }
            //Checking for diagonal across a vertical plain in 19<=x<=21
            if (i>=19 && i<=21) {
                if (board[i]==board[i-6] && board[i]==board[i-12]) {
                    if (board[i]=='X') {
                        //X player is winner by column in multi-game
                        std::cout<<"The X player has won! Congradulations! This is win Condition 13\n";
                        exit(0);
                    } else if (board[i]=='O') {
                        //O Player is winner by column in multi-game
                        std::cout<<"The O player has won! Congradulations! This is win Condition 14\n";
                        exit(0);
                    }
                }
            }
        }
        //3) Check Diagonal in single and multi game
        //3a) Checking single game wins L->R
        if (i==1||i==10||i==19) {
            if (board[i]==board[i+4]&&board[i]==board[i+8]) {
                if (board[i]=='X') {
                    //X player wins
                    std::cout<<"The X player has won! Congradulations! This is win Condition 15\n";
                    exit(0);
                } else if (board[i]=='O') {
                    //O player wins
                    std::cout<<"The O player has won! Congradulations! This is win Condition 16\n";
                    exit(0);
                }
            }
        }
        //3b) Checking single game wins R->L
        if (i == 3 || i == 12 || i == 21) {
            if (board[i]==board[i+2]&&board[i]==board[i+4]) {
                if (board[i]=='X') {
                    //X player wins
                    std::cout<<"The X player has won! Congradulations! This is win Condition 17\n";
                    exit(0);
                } else if (board[i]=='O') {
                    //O player wins
                    std::cout<<"The O player has won! Congradulations! This is win Condition 18\n";
                    exit(0);
                }
            }
        }
        //3c) Checking multi wins -> Diagonal across games, there are 4 possible wins in this scenario
        //If 1=14=27, If 7=14=21, If 19=14=9, If 25=14=3 (These indexs have been --'ed since x=i+1)
        if (board[0]==board[13]&&board[0]==board[26]) {
            if (board[0]=='X') {
                //X player wins
                std::cout<<"The X player has won! Congradulations! This is win Condition 19\n";
                exit(0);
            } else if (board[0]=='O') {
                //O player wins
                std::cout<<"The O player has won! Congradulations! This is win Condition 20\n";
                exit(0);
            }
        } else if (board[6]==board[13]&&board[6]==board[20]) {
            if (board[6]=='X') {
                //X player wins
                std::cout<<"The X player has won! Congradulations! This is win Condition 21\n";
                exit(0);
            } else if (board[6]=='O') {
                //O player wins
                std::cout<<"The O player has won! Congradulations! This is win Condition 22\n";
                exit(0);
            }
        } else if (board[18]==board[13]&&board[18]==board[8]) {
            if (board[18]=='X') {
                //X player wins
                std::cout<<"The X player has won! Congradulations! This is win Condition 23\n";
                exit(0);
            } else if (board[18]=='O') {
                //O player wins
                std::cout<<"The O player has won! Congradulations! This is win Condition 24\n";
                exit(0);
            }
        } else if (board[24]==board[13]&&board[24]==board[2]) {
            if (board[24]=='X') {
                //X player wins
                std::cout<<"The X player has won! Congradulations! This is win Condition 25\n";
                exit(0);
            } else if (board[24]=='O') {
                //O player wins
                std::cout<<"The O player has won! Congradulations! This is win Condition 26\n";
                exit(0);
            }
        }
    }
    //Checking the case of a tie using isTie
    if(!tie) {
        std::cout<<"The game has ended in a tie!\n";
        //exit(0);
    }
    //Returning false if there were no wins
    return false;
}
          