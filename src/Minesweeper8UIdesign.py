import random
import sys
import tkinter as tk
import tkinter.messagebox
import time
import sqlite3

from src.baseInterface import BaseInterface
from src.buttons import Buttons


class MineSweeper(BaseInterface, Buttons):
    def __init__(self, width: int, height: int, num_of_mines: int, level: str, callback) -> None:
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
        self.level = level
        self.callback = callback

        # create the main window
        BaseInterface.__init__(self)

        # initialize the game state
        self.over = False
        self.is_show_answer = False
        self.show_answer_done = False
        self.first_click_done = False

        # create the timer
        self.time_label = tk.Label(self.root, text="0 s")
        self.time_label.pack()

        # create the game area
        self.frame = BaseInterface.create_frame(self.root, width, height)

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
        self.button_show_records = tk.Button(self.root, text="show records", command=self.show_records, width=15)
        self.button_show_records.pack(side=tk.LEFT)

        # initialize the game
        self.correct_flags_count = 0
        self.flags_count = 0
        Buttons.__init__(self, self.frame, width, height)
        self.buttons = self.place_buttons(self.width, self.height)

        # bind the button click event
        self.bind_buttons(self.width, self.height, self.game_label)

        # center the window
        self.root.update()
        BaseInterface.center_window(self.root)

        # start the timer
        self.start_time = time.time()
        self.update_timer(self.time_label)

        # connect to the database
        self.conn = sqlite3.connect("records.db")  # connect to the database.
        self.cur = self.conn.cursor()  # create a cursor
        self.cur.execute("CREATE TABLE IF NOT EXISTS records (level TEXT, time INTEGER)")  # create a table
        self.conn.commit()  # commit the changes

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
                self.buttons[i0][j0].bind("<Button-3>",
                                          lambda event, i=i0, j=j0: self.place_remove_flag(i, j, label))

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
            buttons[i][j].config(text="*", background="#FF8080", state="disabled")  # light red
            self.turn_off_buttons(buttons)
            label.config(text="Game Over")
            self.change_mine_color(buttons, self.mines)
            self.over = True
            return None
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

    # change the number of flags label
    def check_flag(self, i, j, mines, num_of_change) -> None:
        """
        check if the flag is placed correctly
        :param num_of_change: the number of change
        :param i: the x coordinate
        :param j: the y coordinate
        :param mines: the list of mines
        :return: None
        """
        if (i, j) in mines:
            self.correct_flags_count += num_of_change

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
        self.check_flag(i, j, self.mines, num_of_change)
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
            self.check_record(int(time.time() - self.start_time))

    # check if it is a new record
    def check_record(self, elapsed_time) -> None:
        """
        check if it is a new record
        :param elapsed_time: the time elapsed
        :return: None
        """
        self.cur.execute(f"SELECT * FROM records WHERE level = '{self.level}'")
        records = self.cur.fetchall()
        if (len(records) == 0 or elapsed_time < records[0][1]) and not self.show_answer_done:
            self.cur.execute(f"DELETE FROM records WHERE level = '{self.level}'")
            self.cur.execute(f"INSERT INTO records VALUES ('{self.level}', {elapsed_time})")
            self.conn.commit()
            tk.messagebox.showinfo("New Record", f"Congratulations! You set a new record: {elapsed_time} s")

    def show_records(self) -> None:
        """
        show the records
        :return: None
        """
        self.cur.execute(f"SELECT * FROM records WHERE level = '{self.level}'")
        records = self.cur.fetchall()
        if len(records) == 0:
            tk.messagebox.showinfo("No Record", "No record yet")
        else:
            tk.messagebox.showinfo("Record", f"Current record: {records[0][1]} s")

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
                buttons[mine[0]][mine[1]].config(text="*", background="#FF8080")  # light red
            else:
                buttons[mine[0]][mine[1]].config(background="light green")

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
            self.show_answer_done = True
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
        self.callback()
