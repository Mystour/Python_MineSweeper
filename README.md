# Python MineSweeper Game

## Getting Started

To run this game, you need to have Python installed on your computer. If you haven't installed it yet, you can download it from the [Python official website](https://www.python.org/downloads/).

You also need to have Tkinter for GUI. It comes pre-installed with standard Python distributions. 

## Downloading the Code

Once you have the necessary environment setup, download the Python script for the game. You can do this by cloning the repository from Github or any other source where the script is available.

## Game Setup

The game initiates with the user deciding their preferred difficulty level. The options include:

1. Beginner 
2. Intermediate
3. Expert

Each level comes with a preset number of mines.

## Gameplay

The main game utilizes a matrix of buttons, which is created using the Tkinter GUI package in Python. On starting the game, the total count of mines is displayed and a timer begins recording the playtime.

Each cell on the game board operates under two conditions. If a cell is mine-free, left-clicking will reveal the number of adjacent cells that contain mines. If the cell contains a mine and you left-click, the game ends.

A significant feature we've enacted is the ability to place and remove flags with only the right-click. Users can flag a suspected cell with a right-click and remove it with another right-click. This addition results in a seamless user experience.

The user's goal is to correctly flag all cells containing mines. If accomplished, the user wins the game!

## Game Settings

The game provides the option to quit or restart at any point in the game. The restart option resets the game from scratch, starting from the level selection dialog.

## Technical Aspects

This application showcases how Tkinter can be employed for GUI-based applications in Python. It integrates event-driven programming concepts as it uses mouse-click events for user interaction and timer events to keep track of playtime. 

The game concepts, such as checking for game-end conditions, revealing cells, placing and removing flags, are all embedded within the game logic.

The `main()` function, situated at the end of the script, serves as the primary entry point when running the application as a standalone script.