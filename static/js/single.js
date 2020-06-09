//Detects when a square is clicked
document.querySelectorAll('.grid-item').forEach(entry => {
    entry.onclick = () => {
        alert(entry.id);
    }
});