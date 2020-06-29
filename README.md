# Final Project

### Ben Golding - benjamin.golding@mail.mcgill.ca

This is a 3D version of the classic Tick-Tack-Toe game, there are three boards of 3x3 cells each. To win, a player must must have a series of 3 consecutive cells marked with the same symbol either within the same board or across the 3 boards. Users can play in either multiplayer or singleplayer modes.



This project utilizes Flask, JavaScript, and SQL

## Explanation of Files
**Static/css/grid.css:** Contains CSS necessary to create the grids

**Static/images/\*.png:** Contains images for logo as well as examples of wins

**Static/js/index.js:** Contains javascript for the index page

**Static/js/multiplayer.js:** Contains javascript for multiplayer mode

**Static/js/single.js:** Contains javascript for singleplayer mode

**Static/python/game_resources.py:** Contains function for determining the computers move in singleplayer mode as well as a function for determining if there is a winner given some board

**templates/base.html:** Base template for the 3 pages, it is very similar to [this](https://bootstrap-flask.readthedocs.io/en/latest/basic.html#starter-template) template from Bootstrap-Flask. For more details see the comments at the top of the file

**templates/index.html:** HTML for starting page

**templates/single.html:** HTML for singleplayer page

**templates/multiplayer.html:** HTML for multiplayer page

**applications.py:** Python Functions for routing + backend logic not in _Static/python/game_resources.py_