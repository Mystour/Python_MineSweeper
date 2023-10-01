import tkinter as tk
from src.baseInterface import BaseInterface
from src.selectLevel import SelectLevel


class Menu(BaseInterface):
    def __init__(self):
        """
        initialize the main window
        """
        super().__init__()
        self.callback = self.call
        self.root.title("Minesweeper")

        # Define colors for different categories of labels
        colors = {'instructions': '#D5F5E3', 'click_actions': '#F5B041'}

        # Frame for Instructions
        self.instructions_frame = tk.Frame(self.root, bg=colors['instructions'])
        self.instructions_frame.pack(pady=10)

        # Frame for Click Actions
        self.clicks_frame = tk.Frame(self.root, bg=colors['click_actions'])
        self.clicks_frame.pack(pady=10)

        # Frame for Button
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        instructions = [
            """You can change the level of the game.
            The time will start when you click on a cell.
            Note: Once you click "show answer", your record will not be recorded."""
        ]

        for instruction in instructions:
            tk.Label(
                self.instructions_frame,
                text=instruction,
                font=("Helvetica", 16),
                width=50,  # specify appropriate value based on your need
                bg=colors['instructions']
            ).pack(pady=5)

        click_actions = [
            "Left click to reveal a cell.",
            "Right click to flag a cell.",
            "Re-right click to unflag a cell.",
        ]

        for action in click_actions:
            tk.Label(
                self.clicks_frame,
                text=action,
                font=("Helvetica", 16),
                width=50,  # specify appropriate value based on your need
                bg=colors['click_actions']
            ).pack(pady=5)

        tk.Button(
            self.button_frame,
            text="Start",
            font=("Helvetica", 30),
            command=lambda: self.start(self.callback)
        ).pack()

        # center the window
        self.root.update()
        super().center_window(self.root)

    def start(self, callback):
        """
        start the game
        :return: None
        """
        self.root.destroy()
        from src.selectLevel import SelectLevel
        SelectLevel(callback).root.mainloop()

    def call(self):
        SelectLevel(self.callback).root.mainloop()
