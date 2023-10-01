import tkinter as tk


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
