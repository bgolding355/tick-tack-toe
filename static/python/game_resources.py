
import random
## Module for check_win, computer_move 

# Returns the square in which the computer will move and whether or not that move will
# result in a win, returning -1 if there is no availible move. 
# If there is either a winning move, or move to prevent the player from winning it will be taken, 
# otherwise a random square will be selected
def computer_move(board):
    temp_board = board.copy()
    can_move=False
    for i in range (1,28):
        if temp_board[i]=='':
            can_move=True
            #Checking if player can win by moving at board[i]
            temp_board[i]='p'
            if check_win(temp_board) == 'p':
                return [i,False]
            #Checking if computer can win by moving at board[i]
            temp_board[i]='c'
            if check_win(temp_board) == 'c':
                return [i,True]
            temp_board[i]='' #Setting temp_board[i] back to its initial state if no winning move is found
    if not(can_move): #Game is a tie
        return [-1,False]
    else: #A random square is picked
        while True:
            r = random.randint(1,27)
            if temp_board[r] == '':
                return [r,False]

#Returns 'p' if the human player wins, 'c' if the computer wins, 't' if there is a tie, and '-' if there is no winner
def check_win(board):
    tie = True #tie is true when all board positions are filled and there is no winner
    for i in range (1,28):
        #First checking if there exists an empty space
        if board[i] == '':
            tie = False

        ## Now Checking potential win conditions ##
        #1) Checking for 3 in a ROW across across a flat plain
        if i%3==1: #This condition applies to 1,4,7,10,13,16,19,22,25
            #Single board conditions
            if board[i]==board[i+1] and board[i]==board[i+2]:
                #Winner by row across in single game
                if board[i]!='':
                    return board[i]
            #Multi-Board Conditions - Diagonal across flat plain (relative to z) starting on Board1
            if i == 1 or i == 4 or i == 7:
                if board[i] == board[i+10] and board[i] == board[i+20]:
                    #Winner by row across in multi-game, diagonal across flat plain  
                    if board[i]!='':
                        return board[i]
              
            #Multi-Board Conditions - Diagonal across flat plain (relative to z) starting on Board3
            if i==21 or i== 24 or i== 27:  
                if board[i]==board[i-10] and board[i] == board[i-20]:  
                    #Winner by row across in multi-game, diagonal across flat plain
                    if board[i]!='':
                        return board[i]
                      
            #Multi-Board Conditions - Strait across x,z
            if (i<10):
                if board[i]==board[i+9] and board[i]==board[i+18]:
                    #Winner by row across in multi-game
                    if board[i]!='':
                        return board[i]
                  
        #2) Checking for 3 in a row across across a VERTICAL plain
        if i==1 or i==2 or i==3 or i==10 or i==11 or i==12 or i==19 or i==20 or i==21:
            #Checking for single game solutions
            if board[i]==board[i+3] and board[i]==board[i+6]: 
                #Winner by column in single game
                if board[i]!='':
                        return board[i]
            
            #Checking for diagonal across a vertical plain starting at i>4
            if (i<4):
                if board[i]==board[i+12] and board[i]==board[i+24]:
                    #Winner by column in multi-game
                    if board[i]!='':
                        return board[i]

            #Checking for diagonal across a vertical plain in 19<=i<=21
            if i>=19 and i<=21:
                if board[i]==board[i-6] and board[i]==board[i-12]:
                    #Winner by column in multi-game
                    if board[i]!='':
                        return board[i]
                    
        #3) Check DIAGONAL in single and multi game
        #3a) Checking single game wins (from left to right)
        if i==1 or i==10 or i==19:
            if board[i]==board[i+4] and board[i]==board[i+8]:
                if board[i]!='':
                    return board[i]

        #3b) Checking single game wins (from right to left)
        if i == 3 or i == 12 or i == 21:
            if board[i]==board[i+2] and board[i]==board[i+4]:
                if board[i]!='':
                    return board[i]

        #3c) Checking multi wins -> Diagonal across games, there are 4 possible wins in this scenario
        #If 1=14=27, 7=14=21, 19=14=9, and 25=14=3
        if board[1] == board[14] and board[1]==board[27]: 
            if board[1]!='':
                return board[1]
        elif board[7]==board[14] and board[7]==board[21]: 
            if board[7]!='':
                return board[7]
        elif board[19]==board[14] and board[19]==board[9]:
            if board[19]!='':
                return board[19]
        elif board[25]==board[14] and board[24]==board[3]:
            if board[25]!='':
                return board[25]
    
    #If no winner has been selected, returning tie or no-winner
    if tie: 
        return 't'
    else:
        return '-'