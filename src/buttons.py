import tkinter as tk


class Buttons:
    def __init__(self, frame, w, h):
        self.frame = frame
        self.buttons = self.place_buttons(w, h)

    # create a 2D list to store the buttons
    def place_buttons(self, h, w) -> list:
        """
        create a 2D list to store the buttons
        :param h: the height of the board
        :param w: the width of the board
        :return: the 2D list of buttons
        """
        return [[self.create_button(i, j) for j in range(h)] for i in range(w)]

    # create a button
    def create_button(self, i, j) -> tk.Button:
        """
        place a button
        :param i: the x coordinate
        :param j: the y coordinate
        :return: the button
        """
        button = tk.Button(self.frame, width=2, height=1, bg="light blue", relief=tk.GROOVE)
        button.grid(row=i, column=j, sticky=tk.NSEW)
        return button
