let socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

let player_number = document.getElementById('player_number').innerText;
let locked = true //Player 1 moves first
if (player_number == 1) locked = false;
let game_id = document.getElementById('game_id').innerHTML;

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
    socket.on('new_gamestate_multiplayer', data => {
        for (i = 1; i<=27;i++) {
            //First updating lock

            //ADD ME IN HERE 

            //Now updating board
            if (data[i] == 'p') {
                document.getElementById(i).innerText='X';
            } else if (data[i] == 'c') {
                document.getElementById(i).innerText='O';
            }
        }
    });

    //Triggers Alert on Win
    socket.on('winner_multiplayer', data => {
        locked = true;
        if (data == 'p') { //player wins
            document.getElementById("player_win").style.display = 'block';
        } else if (data == 'c') { //Computer wins
            document.getElementById("computer_win").style.display = 'block';
        } else { //tie
            document.getElementById("tie").style.display = 'block';
        }
    });
});