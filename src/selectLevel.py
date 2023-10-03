import tkinter as tk
from src.baseInterface import BaseInterface
from src.Minesweeper8UIdesign import MineSweeper


class SelectLevel(BaseInterface):
    def __init__(self):
        """
        initialize the main window
        """
        super().__init__()

        tk.Label(self.root, text="Select the level",
                 height=5, font=("Lucida Handwriting", 20), bg="light blue").pack(fill=tk.BOTH, expand=1)

        self.frame: tk.Frame = super().create_frame(self.root, 3, 2)

        self.buttons = [
            tk.Button(self.frame, text="Beginner", font=("Lucida Handwriting", 15), command=self.beginner),
            tk.Button(self.frame, text="Intermediate", font=("Lucida Handwriting", 15), command=self.intermediate),
            tk.Button(self.frame, text="Expert", font=("Lucida Handwriting", 15), command=self.expert)
        ]

        self.labels = [
            tk.Label(self.frame, text="8*8, 10 mines", height=3, font="bold"),
            tk.Label(self.frame, text="16*16, 40 mines", height=3, font="bold"),
            tk.Label(self.frame, text="24*24, 99 mines", height=3, font="bold")
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
        MineSweeper(8, 8, 10, "beginner", self.call).root.mainloop()

    def intermediate(self) -> None:
        """
        start the intermediate level game
        :return: None
        """
        self.root.destroy()
        MineSweeper(16, 16, 40, "intermediate", self.call).root.mainloop()

    def expert(self) -> None:
        """
        start the expert level game
        :return: None
        """
        self.root.destroy()
        MineSweeper(24, 24, 99, "expert", self.call).root.mainloop()

    def place_buttons_labels(self) -> None:
        """
        place the buttons and labels
        :return: None
        """
        for i in range(3):
            self.buttons[i].grid(row=0, column=i, sticky=tk.NSEW)  # sticky=tk.NSEW makes the buttons expand
            self.labels[i].grid(row=1, column=i, sticky=tk.NSEW)

    @staticmethod
    def call():
        SelectLevel().root.mainloop()  # can't use self.root.mainloop() here as self.root is destroyed
