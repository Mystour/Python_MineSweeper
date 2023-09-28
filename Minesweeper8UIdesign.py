import random
import sys
import tkinter as tk
import time


class BaseInterface:
    def __init__(self):
        """
        initialize the main window
        """
        self.root = tk.Tk()
        self.root.title("Minesweeper")

    @staticmethod
    def center_window(root) -> None:
        """
        center the window
        :param root: the main window
        :return: None
        """
        # get the window dimension
        width: int = root.winfo_reqwidth()
        height: int = root.winfo_reqheight()

        # get the screen dimension
        screen_width: int = root.winfo_screenwidth()
        screen_height: int = root.winfo_screenheight()

        # calculate the position of the window
        position_top = int(screen_height / 2 - height / 2)
        position_right = int(screen_width / 2 - width / 2)
        root.geometry(f"{width}x{height}+{position_right}+{position_top}")


class SelectLevel(BaseInterface):
    def __init__(self):
        """
        initialize the main window
        """
        super().__init__()

        tk.Label(self.root, text="Select the level", height=5).pack()

        self.frame: tk.Frame = tk.Frame(self.root)
        self.frame.pack()

        self.buttons = [
            tk.Button(self.frame, text="Beginner", command=self.beginner),
            tk.Button(self.frame, text="Intermediate", command=self.intermediate),
            tk.Button(self.frame, text="Expert", command=self.expert)
        ]

        self.labels = [
            tk.Label(self.frame, text="8 * 8, 10 mines", height=3),
            tk.Label(self.frame, text="16 * 16, 40 mines", height=3),
            tk.Label(self.frame, text="24 * 24, 99 mines", height=3)
        ]

        self.main()

        self.root.update()
        super().center_window(self.root)

    def beginner(self) -> None:
        """
        start the beginner level game
        :return: None
        """
        self.root.destroy()
        MineSweeper(8, 8, 10).root.mainloop()

    def intermediate(self) -> None:
        """
        start the intermediate level game
        :return: None
        """
        self.root.destroy()
        MineSweeper(16, 16, 40).root.mainloop()

    def expert(self) -> None:
        """
        start the expert level game
        :return: None
        """
        self.root.destroy()
        MineSweeper(24, 24, 99).root.mainloop()

    def main(self):
        """
        place the buttons and labels and start the main event loop
        :return: None
        """
        for i in range(3):
            self.buttons[i].grid(row=0, column=i)
            self.labels[i].grid(row=1, column=i)
        self.root.mainloop()


class MineSweeper(BaseInterface):
    def __init__(self, width: int, height: int, num_of_mines: int) -> None:
        """
        initialize the MineSweeper game
        :param width: the width of the board
        :param height: the height of the board
        :param num_of_mines: the number of mines
        """
        # initialize the game constants
        self.width: int = width
        self.height: int = height
        self.num_of_mines: int = num_of_mines

        # create the main window
        super().__init__()

        # initialize the game state
        self.over = False

        # create the timer
        self.start_time = time.time()
        self.time_label = tk.Label(self.root, text="0 s")
        self.time_label.pack()
        self.update_timer(self.time_label)

        # create the game area
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        # create the number of mines label and the number of flags label
        self.mines_label = tk.Label(self.root, text=f"{num_of_mines} mines")
        self.mines_label.pack(side=tk.RIGHT)
        self.flags_label = tk.Label(self.root, text="0 flags")
        self.flags_label.pack(side=tk.RIGHT)

        # create the game label
        self.game_label = tk.Label(self.root, text="")
        self.game_label.pack()

        # create the game buttons
        self.button_quit = tk.Button(self.root, text="quit", command=self.quit, width=10)
        self.button_quit.pack(side=tk.LEFT)
        self.button_restart = tk.Button(self.root, text="restart", command=self.restart, width=10)
        self.button_restart.pack(side=tk.LEFT)

        # initialize the game
        self.correct_flags_count = 0
        self.flags_count = 0
        self.mines = self.random_mines(self.width, self.height, self.num_of_mines)
        self.buttons = self.create_buttons(self.width, self.height, self.frame)

        # bind the button click event
        self.bind_buttons(self.width, self.height, self.buttons, num_of_mines, self.mines, self.game_label)

        # center the window
        self.root.update()
        super().center_window(self.root)

    # create a 2D list to store the buttons
    def create_buttons(self, h, w, frame) -> list:
        """
        create a 2D list to store the buttons
        :param h: the height of the board
        :param w: the width of the board
        :param frame: the frame to place the buttons
        :return: the 2D list of buttons
        """
        return [[self.place_button(i, j, frame) for j in range(h)] for i in range(w)]

    # place a button
    @staticmethod
    def place_button(i, j, frame) -> tk.Button:
        """
        place a button
        :param i: the x coordinate
        :param j: the y coordinate
        :param frame: the frame to place the buttons
        :return: the button
        """
        button = tk.Button(frame, width=2, height=1)
        button.grid(row=i, column=j)
        return button

    # randomly generate the positions of mines
    @staticmethod
    def random_mines(w, h, m) -> list:
        """
        randomly generate the positions of mines
        :param w: the width of the board
        :param h: the height of the board
        :param m: the number of mines
        :return: the list of mines
        """
        mines = []
        while len(mines) < m:
            mine = (random.randint(0, w - 1), random.randint(0, h - 1))
            if mine not in mines:
                mines.append(mine)
        return mines

    # count the number of mines around (i, j)
    @staticmethod
    def count_mines(i, j, w, h, mines) -> int:
        """
        count the number of mines around (i, j)
        :param i: the x coordinate
        :param j: the y coordinate
        :param w: the width of the board
        :param h: the height of the board
        :param mines: the list of mines
        :return: the number of mines around (i, j)
        """
        count = 0
        for x in range(max(0, i - 1), min(w, i + 2)):
            for y in range(max(0, j - 1), min(h, j + 2)):
                if (x, y) in mines:
                    count += 1
        return count

    # bind the button click event
    def bind_buttons(self, w, h, buttons, num_of_mines, mines, label) -> None:
        """
        bind the button click event
        :param w: the width of the board
        :param h: the height of the board
        :param buttons: the list of buttons
        :param num_of_mines: the number of mines
        :param mines: the list of mines
        :param label: the label to display the result
        :return: None
        """
        for i0 in range(w):
            for j0 in range(h):
                buttons[i0][j0].config(command=lambda i=i0, j=j0: self.reveal(i, j, w, h, buttons, mines, label))
                buttons[i0][j0].bind("<Button-3>",
                                     lambda event, i=i0, j=j0:
                                     self.place_flag(i, j, buttons, num_of_mines, mines, label))
                buttons[i0][j0].bind("<Button-2>", lambda event, i=i0, j=j0: self.remove_flag(i, j, buttons,
                                                                                              num_of_mines, mines,
                                                                                              label))

    # define the left click event
    def reveal(self, i, j, w, h, buttons, mines, label) -> None:
        """
        the left click event -> reveal the button
        :param label: the label to display the result
        :param i: the x coordinate
        :param j: the y coordinate
        :param w: the width of the board
        :param h: the height of the board
        :param buttons: the list of buttons
        :param mines: the list of mines
        :return: None
        """
        if (i, j) in mines:
            buttons[i][j].config(text="*", background="red", state="disabled")
            self.turn_off_buttons(buttons)
            label.config(text="Game Over")
            self.change_mine_color(buttons, mines)
            self.over = True
        else:
            count = self.count_mines(i, j, w, h, mines)
            buttons[i][j].config(text=str(count), state="disabled")
            if count == 0:
                for x in range(max(0, i - 1), min(w, i + 2)):
                    for y in range(max(0, j - 1), min(h, j + 2)):
                        if buttons[x][y]["state"] == "normal":
                            self.reveal(x, y, w, h, buttons, mines, label)

    # define the right click event
    def place_flag(self, i, j, buttons, num_of_mines, mines, label) -> None:
        """
        the right click event -> place the flag
        :param i: the x coordinate
        :param j: the y coordinate
        :param buttons: the list of buttons
        :param num_of_mines: the number of mines
        :param mines: the list of mines
        :param label: the label to display the result
        :return: None
        """
        if buttons[i][j]["state"] == "normal":
            buttons[i][j].config(text="F", state="disabled")
            self.change_flags_label(i, j, buttons, num_of_mines, mines, label, 1)
            self.check_win(buttons, num_of_mines, label)

    # define the middle click event

    def remove_flag(self, i, j, buttons, num_of_mines, mines, label) -> None:
        """
        the middle click event -> remove the flag
        :param i: the x coordinate
        :param j: the y coordinate
        :param buttons: the list of buttons
        :param num_of_mines: the number of mines
        :param mines: the list of mines
        :param label: the label to display the result
        :return: None
        """
        if buttons[i][j]["state"] == "disabled" and buttons[i][j]["text"] == "F":
            buttons[i][j].config(text="", state="normal")
            self.change_flags_label(i, j, buttons, num_of_mines, mines, label, -1)

    # change the number of flags label
    def check_flag(self, i, j, mines) -> None:
        """
        check if the flag is placed correctly
        :param i: the x coordinate
        :param j: the y coordinate
        :param mines: the list of mines
        :return: None
        """
        if (i, j) in mines:
            self.correct_flags_count += 1

    # check if the flag is placed correctly
    def change_flags_label(self, i, j, buttons, num_of_mines, mines, label, num_of_change) -> None:
        """
        change the number of flags label
        :param i: the x coordinate
        :param j: the y coordinate
        :param buttons: the list of buttons
        :param num_of_mines: the number of mines
        :param mines: the list of mines
        :param label: the label to display the result
        :param num_of_change: the number of change
        :return: None
        """
        self.flags_count += num_of_change
        self.check_flag(i, j, mines)
        self.flags_label.config(text=f"{self.flags_count} flags")
        self.check_win(buttons, num_of_mines, label)

    # check if the game is over
    def check_win(self, buttons, num_of_mines, label) -> None:
        """
        check if the game is over
        :param buttons: the list of buttons
        :param num_of_mines: the number of mines
        :param label: the label to display the result
        :return: the number of mines around (i, j)
        """
        if self.correct_flags_count == num_of_mines == self.flags_count:
            self.turn_off_buttons(buttons)
            label.config(text="You Win")
            self.change_mine_color(buttons, self.mines)
            self.over = True

    # change the color of the mine when the game is over
    @staticmethod
    def change_mine_color(buttons, mines) -> None:
        """
        change the color of the mine when the game is over
        :param buttons: the list of buttons
        :param mines: the list of mines
        :return: None
        """
        for mine in mines:
            if buttons[mine[0]][mine[1]]["text"] != "F":
                buttons[mine[0]][mine[1]].config(text="*", background="red")
            else:
                buttons[mine[0]][mine[1]].config(background="green")

    # disable all buttons
    @staticmethod
    def turn_off_buttons(buttons) -> None:
        """
        disable all buttons
        :param buttons: the list of buttons
        :return: None
        """
        for row in buttons:
            for button in row:
                button.config(state="disabled")

    def update_timer(self, label) -> None:
        """
        update the timer
        :param label: the label to display the timer
        :return: None
        """
        if self.root.winfo_exists():
            if self.over:
                return
            # calculate the time elapsed (in seconds), and update the label text
            elapsed_time = int(time.time() - self.start_time)
            label.config(text=f"{elapsed_time: >3} s")

            # call itself again after 1000ms to implement the timer
            label.after(1000, self.update_timer, label)

    def quit(self) -> None:
        """
        quit the game
        :return: None
        """
        self.root.destroy()
        sys.exit()

    def restart(self) -> None:
        """
        restart the game
        :return: None
        """
        self.root.destroy()
        main()


def main():
    # create the MineSweeper object
    game = SelectLevel()

    # start the main event loop
    game.root.mainloop()


if __name__ == '__main__':
    main()
