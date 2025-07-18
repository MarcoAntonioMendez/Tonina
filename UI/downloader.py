import customtkinter as ctk
import PIL as pil
import subprocess
import logging

APPLICATION_NAME = "Toniná"

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540

FFMPEG_NOT_INSTALLED_MESSAGE = "Sorry, FFMPEG is not installed on your computer :( \
                                \nPlease close this window and install FFMPEG to use this software correctly."
FFMPEG_NOT_INSTALLED_MESSAGE_X_POS = 100
FFMPEG_NOT_INSTALLED_MESSAGE_Y_POS = 10

class Downloader:
    def __init__(self):
        # Initializing the root to contain the main frame of the GUI application
        self.__root = ctk.CTk()

        # # Initializing canvas
        self.__canvas = ctk.CTkCanvas(self.__root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, highlightthickness=0)
        self.__canvas.pack(fill="both", expand=True)


    def start(self):
        # Calculating some coordinates to center the window frame in the middle of computer screen
        self.__root.minsize(WINDOW_WIDTH,WINDOW_HEIGHT)
        self.__root.maxsize(WINDOW_WIDTH,WINDOW_HEIGHT)
        screen_width = self.__root.winfo_screenwidth()
        screen_height = self.__root.winfo_screenheight()
        x_pos = int((screen_width - WINDOW_WIDTH)/2)
        y_pos = int((screen_height - WINDOW_HEIGHT)/2)
        self.__root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x_pos}+{y_pos}")


        # Setting the icon of the application
        icon_photo_image = pil.ImageTk.PhotoImage(pil.Image.open("Images/flag.png"))
        self.__root.wm_iconphoto(True,icon_photo_image)


        # Setting the application name
        self.__root.title(APPLICATION_NAME)


        # Setting the background image of the program
        background_image = pil.Image.open("Images/background.png").convert("RGBA")
        background = pil.ImageTk.PhotoImage(background_image)
        self.__canvas.create_image(0, 0, anchor="nw", image=background)


        # Checking if FFMPEG is installed in user's computer
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, check=True)
        except FileNotFoundError:
            logging.warning("ffmpeg is not installed in this computer, please install ffmpeg.")
            self.__canvas.create_text(FFMPEG_NOT_INSTALLED_MESSAGE_X_POS,\
                                    FFMPEG_NOT_INSTALLED_MESSAGE_Y_POS, anchor="nw",\
                                    text=FFMPEG_NOT_INSTALLED_MESSAGE, font=('Times New Roman',25),\
                                    fill="#eed6b7")


        # Starting the windows
        self.__root.mainloop()




