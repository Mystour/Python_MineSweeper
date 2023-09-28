# Python_MineSweeper
This Python script represents a classic Minesweeper game.  
The game initiates with the user deciding the difficulty level - Beginner, Intermediate, or Expert, with each level having preset numbers of mines.\\
The main game board is created as a matrix of buttons in tkinter GUI package. The game begins with a total count of mines and a timer starts to record the time.\\
For each square(cell), if it isn't a mine, on left-click it reveals the number of mines in the neighboring cells, and if it is a mine, the game ends.\\
Users can right-click to place a flag on cells that they suspect to contain a mine. If all mines are flagged correctly, the user wins the game.\\
The game provides options to quit or restart at any moment. The entire game restarts upon choosing to restart, bringing back the level choosing dialog.\\
This application demonstrates the use of Tkinter for GUI-based applications in Python. It includes event-driven programming concepts, as it makes use of mouse click events to interact with the user, and timer events to keep track of how long the user has been playing. It also uses grid layout to layout the 'game board'. The game logic, like checking for a game over condition, revealing cells, placing and removing flags, are also implemented in the application.\\
The main() function at the end is the main entry point of the application when it's running as a standalone script.\\
