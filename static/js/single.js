let socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

//First connecting to socket
socket.on('connect', () => {
    //Detects when a square is clicked
    document.querySelectorAll('.grid-item').forEach(entry => {
        //Emits id for the square that is selected
        entry.onclick = () => {
            socket.emit('square_selection', {square: entry.id})
        }
    });
});