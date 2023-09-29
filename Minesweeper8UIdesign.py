import random
import sys
import tkinter as tk
import tkinter.messagebox
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

    @staticmethod
    def create_frame(root, width, height) -> tk.Frame:
        """
        create a frame
        :param root: the main window
        :param width: the width of the frame
        :param height: the height of the frame
        :return: the frame
        """
        frame = tk.Frame(root, width=width, height=height)
        frame.pack(fill='both', expand=True)

        # make all rows and columns in the frame expand with the frame
        for i in range(height):
            frame.rowconfigure(i, weight=1)
        for i in range(width):
            frame.columnconfigure(i, weight=1)

        return frame


class SelectLevel(BaseInterface):
    def __init__(self):
        """
        initialize the main window
        """
        super().__init__()

        tk.Label(self.root, text="Select the level",
                 height=5, font=("Lucida Handwriting", 15), bg="light blue").pack(fill=tk.BOTH, expand=1)

        self.frame: tk.Frame = super().create_frame(self.root, 3, 2)

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

        self.place_buttons_labels()

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

    def place_buttons_labels(self) -> None:
        """
        place the buttons and labels
        :return: None
        """
        for i in range(3):
            self.buttons[i].grid(row=0, column=i, sticky=tk.NSEW)  # sticky=tk.NSEW makes the buttons expand
            self.labels[i].grid(row=1, column=i, sticky=tk.NSEW)


class MineSweeper(BaseInterface):
    def __init__(self, width: int, height: int, num_of_mines: int) -> None:
        """
        initialize the MineSweeper game
        :param width: the width of the board
        :param height: the height of the board
        :param num_of_mines: the number of mines
        """
        # initialize the game constants
        self.mines = None
        self.width: int = width
        self.height: int = height
        self.num_of_mines: int = num_of_mines
        self.normal_color: str = "SystemButtonFace"

        # create the main window
        super().__init__()

        # initialize the game state
        self.over = False
        self.is_show_answer = False
        self.first_click_done = False

        # create the timer
        self.time_label = tk.Label(self.root, text="0 s")
        self.time_label.pack()

        # create the game area
        self.frame = super().create_frame(self.root, width, height)

        # make all rows and columns in the frame expand with the frame
        for i in range(height):
            self.frame.rowconfigure(i, weight=1)
        for i in range(width):
            self.frame.columnconfigure(i, weight=1)

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
        self.button_show_hide_answer = tk.Button(self.root, text="show answer",
                                                 command=lambda:
                                                 self.show_hide_answer(), width=15)
        self.button_show_hide_answer.pack(side=tk.LEFT)

        # initialize the game
        self.correct_flags_count = 0
        self.flags_count = 0
        self.buttons = self.place_buttons(self.width, self.height)

        # bind the button click event
        self.bind_buttons(self.width, self.height, self.game_label)

        # center the window
        self.root.update()
        super().center_window(self.root)

        # start the timer
        self.start_time = time.time()
        self.update_timer(self.time_label)

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

    # randomly generate the positions of mines
    def random_mines(self, i_first_click, j_first_click, w, h) -> tuple:
        """
        randomly generate the positions of mines
        :param i_first_click: the x coordinate of the first click
        :param j_first_click: the y coordinate of the first click
        :param w: the width of the board
        :param h: the height of the board
        :return: the list of mines
        """
        mines = []
        while len(mines) < self.num_of_mines:
            possible_mine = (random.randint(0, w - 1), random.randint(0, h - 1))
            if possible_mine != (i_first_click, j_first_click) and possible_mine not in mines:
                mines.append(possible_mine)
        return tuple(mines)

    # count the number of mines around (i, j)
    def count_mines(self, i, j, w, h) -> int:
        """
        count the number of mines around (i, j)
        :param i: the x coordinate
        :param j: the y coordinate
        :param w: the width of the board
        :param h: the height of the board
        :return: the number of mines around (i, j)
        """
        count = 0
        for x in range(max(0, i - 1), min(w, i + 2)):
            for y in range(max(0, j - 1), min(h, j + 2)):
                if (x, y) in self.mines:
                    count += 1
        return count

    # bind the button click event
    def bind_buttons(self, w, h, label) -> None:
        """
        bind the button click event
        :param w: the width of the board
        :param h: the height of the board
        :param label: the label to display the result
        :return: None
        """
        for i0 in range(w):
            for j0 in range(h):
                self.buttons[i0][j0].config(command=lambda i=i0, j=j0: self.reveal(i, j, w, h, self.buttons, label))
                self.buttons[i0][j0].bind("<Button-3>", lambda event, i=i0, j=j0: self.place_remove_flag(i, j, label))

    # define the left click event
    def reveal(self, i, j, w, h, buttons, label) -> None:
        """
        the left click event -> reveal the button
        :param label: the label to display the result
        :param i: the x coordinate
        :param j: the y coordinate
        :param w: the width of the board
        :param h: the height of the board
        :param buttons: the list of buttons. Keep the parameter to accelerate the program
        :return: None
        """
        if not self.first_click_done:
            self.first_click_done = True
            self.mines = self.random_mines(i, j, self.width, self.height)

        if (i, j) in self.mines:
            buttons[i][j].config(text="*", background="red", state="disabled")
            self.turn_off_buttons(buttons)
            label.config(text="Game Over")
            self.change_mine_color(buttons, self.mines)
            self.over = True
        else:
            count = self.count_mines(i, j, w, h)
            buttons[i][j].config(state="disabled", bg=self.normal_color)
            if count != 0:
                buttons[i][j].config(text=count)
            else:
                for x in range(max(0, i - 1), min(w, i + 2)):
                    for y in range(max(0, j - 1), min(h, j + 2)):
                        if buttons[x][y]["state"] == "normal":
                            self.reveal(x, y, w, h, buttons, label)

    def place_remove_flag(self, i, j, label) -> None:
        if self.buttons[i][j].cget("state") == "normal":
            self.place_flag(i, j, label)
        elif self.buttons[i][j].cget("state") == "disabled" and self.buttons[i][j].cget("text") == "🚩":
            self.remove_flag(i, j, label)
        self.check_win(label)

    def place_flag(self, i, j, label) -> None:
        """
        the right click event -> place the flag
        :param i: the x coordinate
        :param j: the y coordinate
        :param label: the label to display the result
        :return: None
        """
        self.buttons[i][j].config(text="🚩", state="disabled", bg="#00FFFF")
        self.change_flags_label(i, j, label, 1)

    # define the middle click event

    def remove_flag(self, i, j, label) -> None:
        """
        the right click event -> remove the flag
        the middle click event -> remove the flag
        :param i: the x coordinate
        :param j: the y coordinate
        :param label: the label to display the result
        :return: None
        """
        self.buttons[i][j].config(text="", state="normal", bg="light blue")
        self.change_flags_label(i, j, label, -1)
        self.check_win(label)

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
    def change_flags_label(self, i, j, label, num_of_change) -> None:
        """
        change the number of flags label
        :param i: the x coordinate
        :param j: the y coordinate
        :param label: the label to display the result
        :param num_of_change: the number of change
        :return: None
        """
        self.flags_count += num_of_change
        self.check_flag(i, j, self.mines)
        self.flags_label.config(text=f"{self.flags_count} flags")
        self.check_win(label)

    # check if the game is over
    def check_win(self, label) -> None:
        """
        check if the game is over
        :param label: the label to display the result
        :return: the number of mines around (i, j)
        """
        if self.correct_flags_count == self.num_of_mines == self.flags_count:
            self.turn_off_buttons(self.buttons)
            label.config(text="You Win")
            self.change_mine_color(self.buttons, self.mines)
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
            if buttons[mine[0]][mine[1]]["text"] != "🚩":
                buttons[mine[0]][mine[1]].config(text="*", background="red")
            else:
                buttons[mine[0]][mine[1]].config(background="green")

    def show_answer(self) -> None:
        """
        show the answer
        :return: None
        """
        for mine in self.mines:
            if self.buttons[mine[0]][mine[1]].cget("text") != "🚩":
                self.buttons[mine[0]][mine[1]].config(text="*")
        self.button_show_hide_answer.config(text="hide answer")

    def hide_answer(self) -> None:
        """
        hide the answer
        :return: None
        """
        for mine in self.mines:
            if self.buttons[mine[0]][mine[1]].cget("text") != "🚩":
                self.buttons[mine[0]][mine[1]].config(text="")
        self.button_show_hide_answer.config(text="show answer")

    def show_hide_answer(self) -> None:
        """
        show or hide the answer
        :return: None
        """
        if not self.first_click_done:
            tk.messagebox.showinfo("Error", "You can not use it until your first click")
            return None
        if self.is_show_answer:
            self.hide_answer()
            self.is_show_answer = False
        else:
            self.show_answer()
            self.is_show_answer = True

    # disable all buttons
    @staticmethod
    def turn_off_buttons(buttons) -> None:
        """
        disable all buttons
        :param buttons: the list of buttons, keep the parameter to accelerate the program
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
    # create the main window
    game = SelectLevel()

    # start the main event loop
    game.root.mainloop()


if __name__ == '__main__':
    main()
