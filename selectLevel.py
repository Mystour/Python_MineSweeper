import tkinter as tk
from baseInterface import BaseInterface
from Minesweeper8UIdesign import MineSweeper


class SelectLevel(BaseInterface):
    def __init__(self, callback):
        """
        initialize the main window
        """
        super().__init__()

        self.callback = callback

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
        MineSweeper(8, 8, 10, "beginner", self.callback).root.mainloop()

    def intermediate(self) -> None:
        """
        start the intermediate level game
        :return: None
        """
        self.root.destroy()
        MineSweeper(16, 16, 40, "intermediate", self.callback).root.mainloop()

    def expert(self) -> None:
        """
        start the expert level game
        :return: None
        """
        self.root.destroy()
        MineSweeper(24, 24, 99, "expert", self.callback).root.mainloop()

    def place_buttons_labels(self) -> None:
        """
        place the buttons and labels
        :return: None
        """
        for i in range(3):
            self.buttons[i].grid(row=0, column=i, sticky=tk.NSEW)  # sticky=tk.NSEW makes the buttons expand
            self.labels[i].grid(row=1, column=i, sticky=tk.NSEW)
