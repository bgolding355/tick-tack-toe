let socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

let locked = false; //locked == false when the player is allowed to make a move

//Refreshes page when the new_game anchor is clicked
function refreshPage() {
    location.reload();
}

//First connecting to socket
socket.on('connect', () => {
    //Detects when a square is clicked
    document.querySelectorAll('.grid-item').forEach(entry => {
        //Emits id for the square that is selected
        entry.onclick = () => {
            if (!(locked)) socket.emit('square_selection_singleplayer', {square: entry.id});
        }
    });
    
    //Updates board after each move
    socket.on('new_gamestate', data => {
        for (i = 1; i<=27;i++) {
            if (data[i] == 'p') {
                document.getElementById(i).innerText='X';
            } else if (data[i] == 'c') {
                document.getElementById(i).innerText='O';
            }
        }
    });

    //Triggers Alert on Win
    socket.on('winner', data => {
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