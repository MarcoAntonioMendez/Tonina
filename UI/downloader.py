import customtkinter as ctk
import PIL as pil
import subprocess
import logging

APPLICATION_NAME = "Toniná"

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540

FFMPEG_NOT_INSTALLED_MESSAGE = "Sorry, FFMPEG is not installed on your computer :( \
                                \nPlease close this window and install FFMPEG to use this software correctly."

class Downloader:
    def __init__(self):
        # Initializing the root to contain the main frame of the GUI application
        self.__root = ctk.CTk()


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
        try:
            icon_image = pil.Image.open("Images/flag.png")
            icon_photo_image = pil.ImageTk.PhotoImage(icon_image)
            self.__root.wm_iconphoto(True,icon_photo_image)
        except FileNotFoundError:
            logging.warning("Error, program icon was not found.")


        # Setting the application name
        self.__root.title(APPLICATION_NAME)


        # Setting the background image of the application
        try:
            background_image = pil.Image.open("Images/background.png")
            background_image = ctk.CTkImage(background_image, size=(WINDOW_WIDTH, WINDOW_HEIGHT))
            label = ctk.CTkLabel(master=self.__root, image=background_image, text="")
            label.place(x = 0, y = 0, relwidth = 1, relheight = 1)
        except FileNotFoundError:
            logging.warning("Error, program icon was not found.")


        # Checking if FFMPEG is installed in user's library
        self.check_if_ffmpeg_is_installed()


        # Starting the windows
        self.__root.mainloop()



    def check_if_ffmpeg_is_installed(self):
        # Checking if ffmpeg is installed
        self.__ffmpeg_installed = False
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, check=True)
            self.__ffmpeg_installed = True
        except FileNotFoundError:
            logging.warning("ffmpeg is not installed in this computer, please install ffmpeg.")


        # Depending of the ffmpeg status on the computer, the UI will change.
        # If ffmpeg is installed, then the normal interface will be shown and the program
        # will start withtou problems.

        # If ffmpeg is NOT installed, then a message will inform user to install ffmpeg for
        # the program to work.
        if(not self.__ffmpeg_installed):
            logging.warning("ffmpeg is not installed, impossible to continue.")
            label_ffmpeg_not_installed_warning = ctk.CTkLabel(master = self.__root,\
                                                        text = FFMPEG_NOT_INSTALLED_MESSAGE,\
                                                        justify = tk.LEFT,\
                                                        font=("Times New Roman", 30),)
            label_ffmpeg_not_installed_warning.pack()
            self.__root.update()
            label_ffmpeg_not_installed_warning.place(\
                x = (WINDOW_WIDTH-label_ffmpeg_not_installed_warning.winfo_width())/2,\
                y = (WINDOW_HEIGHT-label_ffmpeg_not_installed_warning.winfo_height())/2)
        else:
            logging.warning("ffmpeg is installed, continue.")




