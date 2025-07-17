import tkinter as tk


WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540

class Downloader:
    def __init__(self):
        # Initializing the root to contain the main frame of the GUI application
        self.__root = tk.Tk()


    def start(self):
        # Calculating some coordinates to center the window frame in the middle of computer screen
        self.__root.minsize(WINDOW_WIDTH,WINDOW_HEIGHT)
        self.__root.maxsize(WINDOW_WIDTH,WINDOW_HEIGHT)
        screen_width = self.__root.winfo_screenwidth()
        screen_height = self.__root.winfo_screenheight()
        x_pos = int((screen_width - WINDOW_WIDTH)/2)
        y_pos = int((screen_height - WINDOW_HEIGHT)/2)
        self.__root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x_pos}+{y_pos}")


        # Starting the windows
        self.__root.mainloop()
