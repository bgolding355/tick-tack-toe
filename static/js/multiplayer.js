let socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

let player_number = document.getElementById('player_number').innerText;
let locked = true //Player 1 moves first
if (player_number == 1) locked = false;
let game_id = document.getElementById('game_id').innerHTML;

// Asking flask for the board when page is loaded
socket.emit('board_update_request', {'game_id':game_id});

//First connecting to socket
socket.on('connect', () => {
    //Detects when a square is clicked
    document.querySelectorAll('.grid-item').forEach(entry => {
        //Emits id for the square that is selected
        entry.onclick = () => {
            if (!(locked)) socket.emit('square_selection_multiplayer', {'square': entry.id, 'game_id': game_id, 
                                                                        'player_number': player_number});
        }
    });
    
    //Updates board after each move
    socket.on('update_multiplayer_board', data => {
        for (i = 1; i<=27;i++) {
            //First updating lock if turn != -1
            if (data.turn != "-1") {
                if (data.turn == player_number.toString()) {
                    locked = false;
                } else {
                    locked = true
                }
            } 

            //Now updating board
            if (data.game_state[i] == player_number.toString()) {
                document.getElementById(i).innerText='X';
            } else if (data.game_state[i] == (player_number%2+1).toString()) {
                document.getElementById(i).innerText='O';
            }
        }
    });

    //Triggers Alert on Win
    socket.on('winner_multiplayer', data => {
        locked = true;
        if (data.winner == player_number) { //You have won
            document.getElementById("win").style.display = 'block';
        } else if (data.winner == (player_number%2+1)) { //Opponent wins
            document.getElementById("loss").style.display = 'block';
        } else { //tie
            document.getElementById("tie").style.display = 'block';
        }
    });
});